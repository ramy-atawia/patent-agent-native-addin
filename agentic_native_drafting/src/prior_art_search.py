#!/usr/bin/env python3
"""
Enhanced Patent Search Module with OpenAI 400 Error Fixes
Addresses common Azure OpenAI API issues causing 400 errors
"""

import os
import json
import logging
import httpx
import time
import asyncio
import re
import traceback
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
from dotenv import load_dotenv
from langfuse import observe

# Load environment variables
load_dotenv()

# Constants
DEFAULT_MIN_REQUEST_INTERVAL = 1.5
DEFAULT_RELEVANCE_THRESHOLD = 0.3
DEFAULT_MAX_RESULTS = 20
DEFAULT_BATCH_SIZE = 5
MAX_PROMPT_LENGTH = 50000  # Conservative limit for gpt-4o-mini compatibility
DEFAULT_TIMEOUT = 30.0
DEFAULT_REPORT_PATENT_LIMIT = 25  # Maximum patents to include in detailed reports

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PatentClaim:
    """Represents a patent claim with detailed information"""
    claim_number: str
    claim_text: str
    claim_type: str = "independent"  # independent or dependent
    dependency: Optional[str] = None
    is_exemplary: bool = False

@dataclass
class PatentAnalysis:
    """Comprehensive patent analysis results"""
    patent_id: str
    title: str
    abstract: str
    inventors: List[str]
    assignees: List[str]
    claims: List[PatentClaim]
    relevance_score: float
    risk_assessment: Dict[str, Any]
    technical_analysis: Dict[str, Any]
    competitive_insights: Dict[str, Any]
    source_strategy: Optional[str] = None
    publication_date: Optional[str] = None
    patent_year: Optional[int] = None

@dataclass
class SearchStrategy:
    """Represents a search strategy with enhanced metadata"""
    name: str
    description: str
    query: Dict[str, Any]
    expected_results: int = 10
    priority: int = 1  # 1=highest, 5=lowest
    technical_focus: Optional[str] = None
    coverage_scope: str = "MEDIUM"  # NARROW, MEDIUM, BROAD

@dataclass
class SearchResult:
    """Comprehensive search result with analysis"""
    query: str
    total_found: int
    patents: List[PatentAnalysis]
    search_strategies: List[SearchStrategy]
    technology_landscape: Dict[str, Any]
    competitive_analysis: Dict[str, Any]
    timestamp: str
    metadata: Dict[str, Any] = field(default_factory=dict)

class ConfigurationError(Exception):
    """Raised when configuration is invalid or missing"""
    pass

class APIError(Exception):
    """Raised when API calls fail"""
    pass

class PatentSearchConfig:
    """Configuration management for patent search"""
    
    def __init__(self):
        self.validate_environment()
        
        # API Configuration
        self.patentsview_api_key = os.getenv("PATENTSVIEW_API_KEY")
        self.patentsview_base_url = "https://search.patentsview.org/api/v1"
        
        # Azure OpenAI Configuration
        self.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4")
        # FIX 1: Use correct API version for Azure OpenAI
        self.azure_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
        
        # Search Parameters
        self.min_request_interval = float(os.getenv("MIN_REQUEST_INTERVAL", DEFAULT_MIN_REQUEST_INTERVAL))
        self.default_relevance_threshold = float(os.getenv("DEFAULT_RELEVANCE_THRESHOLD", DEFAULT_RELEVANCE_THRESHOLD))
        self.default_max_results = int(os.getenv("DEFAULT_MAX_RESULTS", DEFAULT_MAX_RESULTS))
        self.batch_size = int(os.getenv("BATCH_SIZE", DEFAULT_BATCH_SIZE))
        self.report_patent_limit = int(os.getenv("REPORT_PATENT_LIMIT", DEFAULT_REPORT_PATENT_LIMIT))
        
    def validate_environment(self) -> None:
        """Validate required environment variables"""
        required_vars = [
            "AZURE_OPENAI_ENDPOINT",
            "AZURE_OPENAI_API_KEY",
            "AZURE_OPENAI_DEPLOYMENT_NAME"
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        # Check PatentsView API key (warning only)
        if not os.getenv("PATENTSVIEW_API_KEY"):
            logger.warning("PATENTSVIEW_API_KEY not found. PatentsView API access may be limited.")
            logger.warning("Consider setting PATENTSVIEW_API_KEY for improved API access.")

class EnhancedPatentsViewAPI:
    """Enhanced PatentsView API client with improved error handling and architecture"""
    
    def __init__(self, config: PatentSearchConfig):
        self.config = config
        self.session = None  # Will be created async
        self.last_request_time = 0
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = httpx.AsyncClient(timeout=DEFAULT_TIMEOUT)
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
        
    def __enter__(self):
        """Legacy sync context manager for backward compatibility"""
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # We're in an async context, this should not be used
                logger.warning("Using sync context manager in async environment. Use 'async with' instead.")
        except RuntimeError:
            pass
        # Create sync client for legacy support
        self.session = httpx.Client(timeout=DEFAULT_TIMEOUT)
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Legacy sync context manager exit"""
        if hasattr(self, 'session') and self.session:
            self.session.close()
        
    async def close(self):
        """Close the HTTP session"""
        if hasattr(self, 'session') and self.session:
            await self.session.aclose()
    
    async def _rate_limit_async(self) -> None:
        """Async implementation of rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.config.min_request_interval:
            sleep_time = self.config.min_request_interval - time_since_last
            logger.debug(f"Async rate limiting: sleeping for {sleep_time:.2f}s")
            await asyncio.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _rate_limit(self) -> None:
        """Implement rate limiting with proper timing"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.config.min_request_interval:
            sleep_time = self.config.min_request_interval - time_since_last
            logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f}s")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    async def search_patents_async(self, strategy: SearchStrategy) -> List[Dict[str, Any]]:
        """Async version of patent search for parallel execution"""
        await self._rate_limit_async()
        
        if not strategy.query:
            logger.warning(f"Empty query in strategy: {strategy.name}")
            return []
        
        # Enhanced field selection for better results
        fields = [
            "patent_id",
            "patent_title", 
            "patent_abstract",
            "patent_date",
            "patent_year",
            "inventors",
            "assignees"
        ]
        
        payload = {
            "q": strategy.query,
            "f": fields,
            "s": [{"patent_date": "desc"}],
            "o": {"size": min(strategy.expected_results * 3, 100)}
        }
        
        headers = {"Content-Type": "application/json"}
        if self.config.patentsview_api_key:
            headers["X-Api-Key"] = self.config.patentsview_api_key
        
        try:
            logger.debug(f"Executing async strategy: {strategy.name}")
            response = await self._make_request_with_retry_async(
                f"{self.config.patentsview_base_url}/patent/",
                payload,
                headers
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("error", False):
                    logger.error(f"API error in strategy {strategy.name}: {data}")
                    return []
                
                patents = data.get("patents", [])
                total_hits = data.get("total_hits", len(patents))
                
                logger.debug(f"Strategy {strategy.name}: {len(patents)} patents, {total_hits} total matches")
                return self._process_patents(patents, strategy.name)
            else:
                logger.error(f"Strategy {strategy.name} failed with status {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Strategy {strategy.name} failed: {e}")
            return []

    def search_patents(self, strategy: SearchStrategy) -> List[Dict[str, Any]]:
        """Execute a patent search strategy with comprehensive error handling"""
        self._rate_limit()
        
        if not strategy.query:
            logger.warning(f"Empty query in strategy: {strategy.name}")
            return []
        
        # Enhanced field selection for better results
        fields = [
            "patent_id",
            "patent_title", 
            "patent_abstract",
            "patent_date",
            "patent_year",
            "inventors",
            "assignees"
        ]
        
        payload = {
            "q": strategy.query,
            "f": fields,
            "s": [{"patent_date": "desc"}],
            "o": {"size": min(strategy.expected_results * 3, 100)}
        }
        
        headers = {"Content-Type": "application/json"}
        if self.config.patentsview_api_key:
            headers["X-Api-Key"] = self.config.patentsview_api_key
        
        try:
            logger.info(f"Executing strategy: {strategy.name}")
            response = self._make_request_with_retry(
                f"{self.config.patentsview_base_url}/patent/",
                payload,
                headers
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("error", False):
                    logger.error(f"API error in strategy {strategy.name}: {data}")
                    return []
                
                patents = data.get("patents", [])
                total_hits = data.get("total_hits", len(patents))
                
                logger.info(f"Strategy {strategy.name}: {len(patents)} patents, {total_hits} total matches")
                return self._process_patents(patents, strategy.name)
            else:
                logger.error(f"Strategy {strategy.name} failed with status {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Strategy {strategy.name} failed: {e}")
            return []
    
    async def get_patent_claims_async(self, patent_id: str) -> List[PatentClaim]:
        """Async version of patent claims retrieval"""
        if not patent_id:
            return []
        
        await self._rate_limit_async()
        
        payload = {
            "f": [
                "patent_id",
                "claim_sequence", 
                "claim_text",
                "claim_number",
                "claim_dependent",
                "exemplary"
            ],
            "o": {"size": 100},
            "q": {"_and": [{"patent_id": patent_id}]},
            "s": [
                {"patent_id": "asc"}, 
                {"claim_sequence": "asc"}
            ]
        }
        
        headers = {"Content-Type": "application/json"}
        if self.config.patentsview_api_key:
            headers["X-Api-Key"] = self.config.patentsview_api_key
        
        try:
            logger.debug(f"Fetching claims async for patent: {patent_id}")
            
            response = await self.session.post(
                f"{self.config.patentsview_base_url}/g_claim/",
                json=payload,
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                claims_data = data.get("g_claims", [])
                
                return self._parse_claims(claims_data)
            else:
                logger.warning(f"Async claims request failed for {patent_id}: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Async claims retrieval failed for {patent_id}: {e}")
            return []

    def get_patent_claims(self, patent_id: str) -> List[PatentClaim]:
        """Retrieve patent claims with enhanced parsing"""
        self._rate_limit()
        
        if not patent_id:
            return []
        
        payload = {
            "f": [
                "patent_id",
                "claim_sequence", 
                "claim_text",
                "claim_number",
                "claim_dependent",
                "exemplary"
            ],
            "o": {"size": 100},
            "q": {"_and": [{"patent_id": patent_id}]},
            "s": [
                {"patent_id": "asc"}, 
                {"claim_sequence": "asc"}
            ]
        }
        
        headers = {"Content-Type": "application/json"}
        if self.config.patentsview_api_key:
            headers["X-Api-Key"] = self.config.patentsview_api_key
        
        try:
            logger.debug(f"Fetching claims for patent: {patent_id}")
            
            response = self.session.post(
                f"{self.config.patentsview_base_url}/g_claim/",
                json=payload,
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                claims_data = data.get("g_claims", [])
                
                return self._parse_claims(claims_data)
            else:
                logger.warning(f"Claims request failed for {patent_id}: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Claims retrieval failed for {patent_id}: {e}")
            return []
    
    async def _make_request_with_retry_async(self, url: str, payload: Dict, headers: Dict, max_retries: int = 3) -> httpx.Response:
        """Async HTTP request with exponential backoff retry logic"""
        for attempt in range(max_retries):
            try:
                response = await self.session.post(url, json=payload, headers=headers)
                return response
            except Exception as e:
                if attempt < max_retries - 1:
                    delay = 2 ** attempt
                    logger.warning(f"Async request attempt {attempt + 1} failed: {e}, retrying in {delay}s...")
                    await asyncio.sleep(delay)
                else:
                    raise APIError(f"All {max_retries} async request attempts failed: {e}")

    def _make_request_with_retry(self, url: str, payload: Dict, headers: Dict, max_retries: int = 3) -> httpx.Response:
        """Make HTTP request with exponential backoff retry logic"""
        for attempt in range(max_retries):
            try:
                response = self.session.post(url, json=payload, headers=headers)
                return response
            except Exception as e:
                if attempt < max_retries - 1:
                    delay = 2 ** attempt
                    logger.warning(f"Request attempt {attempt + 1} failed: {e}, retrying in {delay}s...")
                    time.sleep(delay)
                else:
                    raise APIError(f"All {max_retries} request attempts failed: {e}")
    
    def _process_patents(self, patents: List[Dict], strategy_name: str) -> List[Dict]:
        """Process raw patent data with enhanced metadata"""
        processed = []
        
        for patent in patents:
            try:
                # Safely extract data with defaults
                patent_data = {
                    "patent_id": patent.get("patent_id", ""),
                    "patent_title": patent.get("patent_title", ""),
                    "patent_abstract": patent.get("patent_abstract", ""),
                    "patent_date": patent.get("patent_date", ""),
                    "patent_year": patent.get("patent_year"),
                    "inventors": patent.get("inventors", []),
                    "assignees": patent.get("assignees", []),
                    "source_strategy": strategy_name,
                    "search_timestamp": time.time()
                }
                
                processed.append(patent_data)
                
            except Exception as e:
                logger.warning(f"Error processing patent: {e}")
                continue
                
        return processed
    
    def _parse_claims(self, claims_data: List[Dict]) -> List[PatentClaim]:
        """Parse claims data into structured PatentClaim objects"""
        claims = []
        
        for claim_info in claims_data:
            try:
                claim_text = claim_info.get("claim_text", "")
                if not claim_text:
                    continue
                
                claim_sequence = claim_info.get("claim_sequence", 0)
                claim_number = claim_info.get("claim_number", "")
                claim_dependent = claim_info.get("claim_dependent", "")
                exemplary = claim_info.get("exemplary", "")
                
                # Determine claim number
                if not claim_number:
                    claim_number = str(claim_sequence + 1)
                
                # Determine claim type
                claim_type = "dependent" if claim_dependent else "independent"
                
                claim = PatentClaim(
                    claim_number=claim_number,
                    claim_text=claim_text,
                    claim_type=claim_type,
                    dependency=claim_dependent if claim_dependent else None,
                    is_exemplary=bool(exemplary)
                )
                
                claims.append(claim)
                
            except Exception as e:
                logger.warning(f"Error parsing claim: {e}")
                continue
        
        # Sort claims by number
        claims.sort(key=lambda x: int(x.claim_number) if x.claim_number.isdigit() else 0)
        return claims

class QueryGenerator:
    """Generate optimized search queries using LLM"""
    
    def __init__(self, config: PatentSearchConfig):
        self.config = config
    
    @observe(name="generate_search_strategies")
    async def generate_search_strategies(self, user_query: str) -> List[SearchStrategy]:
        """Generate multiple search strategies for comprehensive coverage"""
        try:
            prompt = f"""
You are an expert patent attorney and technology analyst specializing in comprehensive prior art search. Generate sophisticated patent search strategies for: "{user_query}"

TECHNICAL PRECISION RULES:
1. Extract compound technical terms (e.g., "machine learning algorithm" -> ["machine learning", "algorithm", "ML", "artificial intelligence"])
2. Include domain-specific terminology and abbreviations
3. Consider broader conceptual terms and narrower specific implementations
4. Add related technical standards, protocols, or methodologies
5. Include alternative technical approaches that achieve similar outcomes

BANNED WORDS (avoid these in queries):
- "system", "method", "apparatus", "device", "means", "invention"
- "improved", "enhanced", "novel", "new", "better"
- "comprising", "including", "having", "wherein"
- Common legal/procedural terms that don't add technical value

SEARCH STRATEGY TYPES:
1. CORE_TECHNICAL: Direct technical terms with precise phrase matching
2. DOMAIN_SPECIFIC: Industry terminology, standards, and protocols  
3. FUNCTIONAL_ALTERNATIVE: Different technical approaches achieving same function
4. COMPONENT_FOCUSED: Individual technical components and sub-systems
5. STANDARDS_PROTOCOLS: Related technical standards, APIs, protocols
6. COMPANY_PORTFOLIO: Target key industry players' patent portfolios
7. TECHNOLOGY_EVOLUTION: Related legacy and emerging technologies

PATENTSVIEW API SYNTAX - OFFICIAL GUIDELINES:

QUERY OPERATORS:
- "_eq": equal to (default if no operator specified)
- "_neq": not equal to
- "_gt": greater than
- "_gte": greater than or equal to
- "_lt": less than
- "_lte": less than or equal to
- "_begins": string begins with value
- "_contains": string contains value
- "_text_all": text contains ALL words in value string
- "_text_any": text contains ANY words in value string
- "_text_phrase": text contains exact phrase
- "_not": negation operator
- "_and": conjunction (array of criteria)
- "_or": disjunction (array of criteria)

FIELD TARGETING:
- patent_title: Patent title (text field)
- patent_abstract: Patent abstract (text field)
- patent_claims: Patent claims text (use with claims endpoint)
- inventors.inventor_name_last: Inventor last name
- assignees.assignee_organization: Assignee organization
- patent_date: Patent grant date (YYYY-MM-DD format)
- patent_year: Patent grant year

TEXT SEARCH BEST PRACTICES:
- Use "_text_any" ONLY for UNIQUE technical terms (e.g., "OFDMA", "beamforming", "MIMO")
- CRITICAL: "_text_any" with common terms like "5G NR LTE" will match ANY of those words separately, 
  potentially returning MILLIONS of patents containing just "5G" OR just "NR" OR just "LTE"
- Use "_text_phrase" for ALL broad/common terms to ensure precise phrase matching (e.g., "dynamic spectrum sharing")
- Use "_text_all" when ALL terms must be present together in the text
- ALWAYS combine broad terms like "5G" with "_text_phrase" and specific concepts
- Prefer nested queries with "_and" to combine precise phrases with unique technical terms
- For "5G dynamic spectrum sharing", use: "_text_phrase" for "dynamic spectrum sharing" AND "_text_phrase" for "5G"
- Use company names and very specific technical acronyms with "_text_any" for targeted searches

QUERY PRECISION HIERARCHY (most to least precise):
1. "_text_phrase" - exact phrase matching (use for common terms)
2. "_text_all" - all words must appear (use for moderate precision)  
3. "_text_any" - any word matches (use ONLY for unique technical terms)

QUERY STRUCTURE EXAMPLES:
- Simple: {{"patent_title": "wireless communication"}}
- UNIQUE terms with _text_any: {{"_text_any": {{"patent_title": "OFDMA beamforming MIMO"}}}}
- CORRECT for broad terms: {{"_and": [{{"_text_phrase": {{"patent_title": "dynamic spectrum sharing"}}}}, {{"_text_phrase": {{"patent_abstract": "5G"}}}}]}}
- WRONG (too broad): {{"_text_any": {{"patent_abstract": "5G NR LTE dynamic spectrum sharing"}}}}
- Multiple precise phrases: {{"_and": [{{"_text_phrase": {{"patent_title": "dynamic spectrum sharing"}}}}, {{"_text_any": {{"patent_abstract": "beamforming MIMO interference"}}}}]}}
- Complex with assignees: {{"_or": [{{"_text_phrase": {{"patent_title": "dynamic spectrum sharing"}}}}, {{"_and": [{{"assignees.assignee_organization": "Ericsson"}}, {{"_text_phrase": {{"patent_abstract": "spectrum coordination"}}}}]}}]}}
- Company-focused: {{"_and": [{{"assignees.assignee_organization": ["Ericsson", "Nokia", "Samsung"]}}, {{"_text_phrase": {{"patent_abstract": "spectrum sharing"}}}}]}}

VALUE ARRAYS:
- Use arrays for OR conditions: {{"inventors.inventor_name_last": ["Smith", "Jones"]}}
- Matches any value in the array

NESTED FIELDS:
- Format: "entity.field_name" (e.g., "inventors.inventor_name_last")
- Available nested fields: inventors.*, assignees.*, citations.*

DATE FORMATS:
- Use ISO 8601 format: YYYY-MM-DD
- Example: {{"_gte": {{"patent_date": "2020-01-01"}}}}

FIELD OPTIMIZATION STRATEGY:
- patent_title: 3-5 most critical terms (highest precision)
- patent_abstract: 7-10 descriptive terms (broader coverage)
- Use "_text_any" for multiple related terms
- Combine complementary searches with "_and"
- Use "_or" for alternative approaches

Return ONLY a JSON array with this structure:
[
    {{
        "name": "STRATEGY_NAME",
        "description": "detailed strategy explanation",
        "query": {{
            "_text_any": {{
                "patent_title": "primary technical terms",
                "patent_abstract": "broader descriptive terms"
            }}
        }},
        "expected_results": 15,
        "priority": 1,
        "technical_focus": "primary technical domain",
        "coverage_scope": "NARROW|MEDIUM|BROAD"
    }}
]

Generate exactly 7 diverse strategies covering different technical angles using proper PatentsView API syntax. Include:
- Core technical phrase matching for precision
- Company-specific searches targeting major telecom players  
- Standards-based searches for 3GPP and regulatory terms
- Alternative technology approaches
- Component and algorithmic searches

CRITICAL PRECISION REQUIREMENTS:
- NEVER use "_text_any" with broad terms like "5G", "LTE", "NR", "wireless", "cellular", "spectrum"
- ALWAYS use "_text_phrase" for common/broad technical terms
- ONLY use "_text_any" for very specific technical terms like "OFDMA", "beamforming", "MIMO"
- Combine precise phrases using "_and" for better specificity
- Target 10-50 results per strategy, not thousands
"""
            
            response = await self._call_llm(prompt)
            logger.info(f"LLM Response: {response[:500]}...")  # Debug log
            
            # Clean response - remove any markdown formatting
            cleaned_response = response.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            cleaned_response = cleaned_response.strip()
            
            strategies_data = json.loads(cleaned_response)
            
            strategies = []
            for i, strategy_data in enumerate(strategies_data):
                strategy = SearchStrategy(
                    name=strategy_data.get("name", f"STRATEGY_{i+1}"),
                    description=strategy_data.get("description", ""),
                    query=strategy_data.get("query", {}),
                    expected_results=strategy_data.get("expected_results", 10),
                    priority=strategy_data.get("priority", 1),
                    technical_focus=strategy_data.get("technical_focus"),
                    coverage_scope=strategy_data.get("coverage_scope", "MEDIUM")
                )
                strategies.append(strategy)
            
            return strategies
            
        except Exception as e:
            logger.error(f"Query generation failed: {e}")
            raise
    
    @observe(name="query_generator_llm_call")
    async def _call_llm(self, prompt: str) -> str:
        """Make async call to Azure OpenAI with fixes for 400 errors"""
        try:
            # FIX 2: Proper URL construction without double slashes
            base_url = self.config.azure_endpoint.rstrip('/')
            url = f"{base_url}/openai/deployments/{self.config.azure_deployment}/chat/completions?api-version={self.config.azure_api_version}"
            
            headers = {
                "Content-Type": "application/json",
                "api-key": self.config.azure_api_key
            }
            
            # FIX 3: Correct payload structure for Azure OpenAI
            payload = {
                "messages": [
                    {"role": "system", "content": "You are a patent analysis expert. Generate professional patent analysis in proper JSON format."},
                    {"role": "user", "content": prompt}
                ],
                # FIX 4: Use max_tokens instead of max_completion_tokens for compatibility
                "max_tokens": 4000,  # Compatible with gpt-4o-mini model limits
                "temperature": 0.1,
                # FIX 5: Remove any unsupported parameters
                # "stream": False  # Explicitly set streaming to false
            }
            
            # FIX 6: Input validation and sanitization
            if len(prompt) > 50000:  # Rough token limit check
                logger.warning(f"Prompt may be too long: {len(prompt)} characters")
                prompt = prompt[:50000] + "..."
                payload["messages"][1]["content"] = prompt
            
            # FIX 7: Clean any problematic characters
            cleaned_prompt = self._clean_text_for_api(prompt)
            payload["messages"][1]["content"] = cleaned_prompt
            
            # Log the request details for debugging
            logger.info(f"🔍 Azure OpenAI Request Details:")
            logger.info(f"   URL: {url}")
            logger.info(f"   Deployment: {self.config.azure_deployment}")
            logger.info(f"   API Version: {self.config.azure_api_version}")
            logger.info(f"   Prompt Length: {len(cleaned_prompt)} characters")
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(url, headers=headers, json=payload)
                
                # Log response details
                logger.info(f"📡 Azure OpenAI Response:")
                logger.info(f"   Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    content = result['choices'][0]['message']['content']
                    logger.info(f"   ✅ Success - Response length: {len(content)} characters")
                    return content
                else:
                    # Enhanced error handling for 400 errors
                    logger.error(f"   ❌ Error Response:")
                    logger.error(f"      Status: {response.status_code}")
                    logger.error(f"      Response Text: {response.text}")
                    
                    try:
                        error_json = response.json()
                        logger.error(f"      Error JSON: {json.dumps(error_json, indent=2)}")
                        
                        # FIX 8: Handle specific 400 error cases
                        if 'error' in error_json:
                            error_info = error_json['error']
                            error_type = error_info.get('type', 'Unknown')
                            error_message = error_info.get('message', 'No message')
                            error_code = error_info.get('code', 'No code')
                            
                            logger.error(f"      Error Type: {error_type}")
                            logger.error(f"      Error Message: {error_message}")
                            logger.error(f"      Error Code: {error_code}")
                            
                            # Handle common 400 error causes
                            if 'content_filter' in error_message.lower():
                                raise APIError(f"Content filtered by Azure OpenAI: {error_message}")
                            elif 'token' in error_message.lower():
                                raise APIError(f"Token limit exceeded: {error_message}")
                            elif 'invalid' in error_message.lower():
                                raise APIError(f"Invalid request format: {error_message}")
                            else:
                                raise APIError(f"Azure OpenAI API error: {error_message}")
                    except json.JSONDecodeError:
                        logger.error(f"      Response is not valid JSON: {response.text[:500]}")
                    
                    raise APIError(f"Azure OpenAI API returned {response.status_code}: {response.text[:200]}")
                    
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error in LLM call: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in LLM call: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            raise
    
    def _clean_text_for_api(self, text: str) -> str:
        """Clean text to avoid API issues"""
        # Remove or replace problematic characters
        cleaned = text.replace('\x00', '')  # Remove null bytes
        cleaned = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', cleaned)  # Remove control characters
        # Normalize whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned)
        return cleaned.strip()

class PatentAnalyzer:
    """Advanced patent analysis with LLM-powered insights"""
    
    def __init__(self, config: PatentSearchConfig):
        self.config = config
    
    async def quick_relevance_check(self, patent_data: Dict, search_query: str) -> float:
        """Perform quick relevance assessment using only title and abstract (no claims)"""
        try:
            title = patent_data.get("patent_title", "")
            abstract = patent_data.get("patent_abstract", "")
            
            # Use a streamlined prompt for quick assessment
            quick_prompt = f"""
            Assess the relevance of this patent to the search query on a scale of 0.0 to 1.0.
            Consider only the title and abstract for this quick assessment.
            
            Search Query: {search_query}
            
            Patent Title: {title[:200]}
            Patent Abstract: {abstract[:300]}
            
            Respond with ONLY a number between 0.0 and 1.0, nothing else.
            """
            
            response = await self._call_llm(quick_prompt)
            
            # Extract numeric score
            match = re.search(r'[0-9]*\.?[0-9]+', response)
            if match:
                score = float(match.group())
                return min(max(score, 0.0), 1.0)  # Clamp between 0 and 1
            else:
                logger.warning(f"Could not parse relevance score from: {response}")
                return 0.5  # Default fallback
                
        except Exception as e:
            logger.error(f"Quick relevance check failed: {e}")
            return 0.0  # Conservative fallback
    
    async def analyze_patent_with_claims(self, patent_data: Dict, search_query: str) -> PatentAnalysis:
        """Perform full patent analysis including claims retrieval - optimized version"""
        try:
            # Extract basic information
            patent_id = patent_data.get("patent_id", "")
            title = patent_data.get("patent_title", "")
            abstract = patent_data.get("patent_abstract", "")
            
            # Parse inventors and assignees safely
            inventors = self._extract_inventors(patent_data.get("inventors", []))
            assignees = self._extract_assignees(patent_data.get("assignees", []))
            
            # Get claims - this is the expensive operation we're optimizing
            async with EnhancedPatentsViewAPI(self.config) as api:
                claims = await api.get_patent_claims_async(patent_id)
            
            # Perform comprehensive LLM-based analysis with claims
            relevance_score = await self._calculate_relevance_score_detailed(patent_data, claims, search_query)
            risk_assessment = await self._assess_risk(patent_data, claims, search_query)
            technical_analysis = await self._analyze_technology(patent_data, claims)
            competitive_insights = await self._analyze_competitive_position(patent_data)
            
            return PatentAnalysis(
                patent_id=patent_id,
                title=title,
                abstract=abstract,
                inventors=inventors,
                assignees=assignees,
                claims=claims,
                relevance_score=relevance_score,
                risk_assessment=risk_assessment,
                technical_analysis=technical_analysis,
                competitive_insights=competitive_insights,
                source_strategy=patent_data.get("source_strategy"),
                publication_date=patent_data.get("patent_date"),
                patent_year=patent_data.get("patent_year")
            )
            
        except Exception as e:
            logger.error(f"Error analyzing patent {patent_data.get('patent_id', 'unknown')}: {e}")
            raise

    async def analyze_patent(self, patent_data: Dict, search_query: str) -> PatentAnalysis:
        """Perform comprehensive patent analysis"""
        try:
            # Extract basic information
            patent_id = patent_data.get("patent_id", "")
            title = patent_data.get("patent_title", "")
            abstract = patent_data.get("patent_abstract", "")
            
            # Parse inventors and assignees safely
            inventors = self._extract_inventors(patent_data.get("inventors", []))
            assignees = self._extract_assignees(patent_data.get("assignees", []))
            
            # Get claims (this could be async in the future)
            with EnhancedPatentsViewAPI(self.config) as api:
                claims = api.get_patent_claims(patent_id)
            
            # Perform LLM-based analysis
            relevance_score = await self._calculate_relevance_score(patent_data, search_query)
            risk_assessment = await self._assess_risk(patent_data, claims, search_query)
            technical_analysis = await self._analyze_technology(patent_data, claims)
            competitive_insights = await self._analyze_competitive_position(patent_data)
            
            return PatentAnalysis(
                patent_id=patent_id,
                title=title,
                abstract=abstract,
                inventors=inventors,
                assignees=assignees,
                claims=claims,
                relevance_score=relevance_score,
                risk_assessment=risk_assessment,
                technical_analysis=technical_analysis,
                competitive_insights=competitive_insights,
                source_strategy=patent_data.get("source_strategy"),
                publication_date=patent_data.get("patent_date"),
                patent_year=patent_data.get("patent_year")
            )
            
        except Exception as e:
            logger.error(f"Error analyzing patent {patent_data.get('patent_id', 'unknown')}: {e}")
            raise
    
    def _extract_inventors(self, inventors_data: List[Dict]) -> List[str]:
        """Safely extract inventor names"""
        inventors = []
        for inv in inventors_data:
            try:
                first = inv.get("inventor_name_first", "")
                last = inv.get("inventor_name_last", "")
                full_name = f"{first} {last}".strip()
                if full_name:
                    inventors.append(full_name)
            except Exception as e:
                logger.debug(f"Error parsing inventor: {e}")
                continue
        return inventors
    
    def _extract_assignees(self, assignees_data: List[Dict]) -> List[str]:
        """Safely extract assignee organizations"""
        assignees = []
        for ass in assignees_data:
            try:
                org = ass.get("assignee_organization", "")
                if org:
                    assignees.append(org)
            except Exception as e:
                logger.debug(f"Error parsing assignee: {e}")
                continue
        return assignees
    
    @observe(name="calculate_relevance_score")
    async def _calculate_relevance_score(self, patent_data: Dict, search_terms: str) -> float:
        """LLM-based intelligent relevance scoring"""
        try:
            # Prepare patent information for LLM analysis
            title = patent_data.get("patent_title", "")[:200]  # Truncate for token efficiency
            abstract = patent_data.get("patent_abstract", "")[:500]  # Truncate for token efficiency
            patent_year = patent_data.get("patent_year", "Unknown")
            
            # Create context for LLM with limited content
            prompt = f"""Analyze patent relevance to search query. Return ONLY a JSON response.

SEARCH: {search_terms}
TITLE: {title}
ABSTRACT: {abstract}
YEAR: {patent_year}

Return ONLY this JSON:
{{
    "relevance_score": <float 0.0-1.0>,
    "reasoning": "<brief explanation>"
}}

SCORING: 0.0-0.2=irrelevant, 0.3-0.4=slight, 0.5-0.6=moderate, 0.7-0.8=high, 0.9-1.0=excellent"""
            
            response = await self._call_llm(prompt)
            result = json.loads(response)
            return float(result.get("relevance_score", 0.5))
            
        except Exception as e:
            logger.error(f"Relevance scoring failed: {e}")
            return 0.5  # Default to moderate relevance on failure
    
    @observe(name="calculate_relevance_score_detailed")
    async def _calculate_relevance_score_detailed(self, patent_data: Dict, claims: List[PatentClaim], search_terms: str) -> float:
        """Calculate detailed relevance score using patent claims data"""
        try:
            # Prepare patent information for LLM analysis with limited content
            title = patent_data.get("patent_title", "")[:200]
            abstract = patent_data.get("patent_abstract", "")[:500]
            patent_year = patent_data.get("patent_year", "Unknown")
            
            # Extract key claims text (limit to avoid token overflow)
            key_claims_text = []
            for claim in claims[:5]:  # Use top 5 claims for better analysis
                key_claims_text.append(f"Claim {claim.claim_number}: {claim.claim_text[:150]}...")
            
            claims_summary = " ".join(key_claims_text)
            
            # Simplified prompt to avoid token limits
            prompt = f"""Analyze detailed patent relevance including claims. Return ONLY JSON.

SEARCH: {search_terms}
TITLE: {title}
ABSTRACT: {abstract}
CLAIMS: {claims_summary}

Return ONLY this JSON:
{{
    "relevance_score": <float 0.0-1.0>,
    "reasoning": "<brief explanation considering claims>"
}}

Consider both abstract AND claims. Score 0.0-1.0."""
            
            response = await self._call_llm(prompt)
            
            # Clean response and handle non-JSON responses
            cleaned_response = response.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            cleaned_response = cleaned_response.strip()
            
            # Try to parse JSON
            try:
                result = json.loads(cleaned_response)
                return float(result.get("relevance_score", 0.5))
            except json.JSONDecodeError:
                # If JSON parsing fails, try to extract just the number
                logger.warning(f"Failed to parse JSON from relevance response: {cleaned_response[:200]}")
                import re
                score_match = re.search(r'"relevance_score":\s*([0-9]*\.?[0-9]+)', cleaned_response)
                if score_match:
                    score = float(score_match.group(1))
                    return min(max(score, 0.0), 1.0)
                else:
                    logger.warning(f"Could not extract relevance score, using default")
                    return 0.5
            
        except Exception as e:
            logger.error(f"Detailed relevance scoring failed: {e}")
            return 0.5  # Default to moderate relevance on failure
    
    @observe(name="assess_patent_risk")
    async def _assess_risk(self, patent_data: Dict, claims: List[PatentClaim], search_query: str) -> Dict[str, Any]:
        """Perform comprehensive risk assessment"""
        try:
            # Extract key claims for analysis (limited for token efficiency)
            key_claims = [claim.claim_text[:100] for claim in claims[:5]]  # Top 5 claims, truncated
            
            prompt = f"""Patent risk assessment. Return ONLY JSON.

SEARCH: {search_query}
TITLE: {patent_data.get('patent_title', '')[:150]}
CLAIMS: {str(key_claims)[:300]}

Return ONLY this JSON:
{{
    "overall_risk": "<HIGH|MEDIUM|LOW>",
    "blocking_potential": "<HIGH|MEDIUM|LOW>",
    "design_around_difficulty": "<HARD|MEDIUM|EASY>",
    "commercial_impact": "<HIGH|MEDIUM|LOW>",
    "reasoning": "<brief explanation>",
    "specific_concerns": ["<concern1>", "<concern2>"]
}}"""
            
            response = await self._call_llm(prompt)
            
            # Clean response and handle non-JSON responses
            cleaned_response = response.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            cleaned_response = cleaned_response.strip()
            
            try:
                return json.loads(cleaned_response)
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse JSON from risk assessment: {cleaned_response[:200]}")
                return {
                    "overall_risk": "MEDIUM",
                    "blocking_potential": "MEDIUM",
                    "design_around_difficulty": "MEDIUM",
                    "commercial_impact": "MEDIUM",
                    "reasoning": "Analysis failed, defaulting to medium risk",
                    "specific_concerns": ["Unable to assess due to JSON parsing failure"]
                }
            
        except Exception as e:
            logger.error(f"Risk assessment failed: {e}")
            return {
                "overall_risk": "MEDIUM",
                "blocking_potential": "MEDIUM",
                "design_around_difficulty": "MEDIUM",
                "commercial_impact": "MEDIUM",
                "reasoning": "Analysis failed, defaulting to medium risk",
                "specific_concerns": ["Unable to assess due to analysis failure"]
            }
    
    @observe(name="analyze_technology")
    async def _analyze_technology(self, patent_data: Dict, claims: List[PatentClaim]) -> Dict[str, Any]:
        """Analyze technical aspects of the patent"""
        try:
            prompt = f"""Analyze patent technology. Return ONLY JSON.

TITLE: {patent_data.get('patent_title', '')[:150]}
ABSTRACT: {patent_data.get('patent_abstract', '')[:300]}
CLAIMS: {len(claims)} total

Return ONLY this JSON:
{{
    "technology_domain": "<primary tech area>",
    "key_innovations": ["<innovation1>", "<innovation2>"],
    "technical_maturity": "<EMERGING|DEVELOPING|MATURE>",
    "standards_relevance": "<HIGH|MEDIUM|LOW>",
    "implementation_complexity": "<HIGH|MEDIUM|LOW>"
}}"""
            
            response = await self._call_llm(prompt)
            
            # Clean response and handle non-JSON responses
            cleaned_response = response.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            cleaned_response = cleaned_response.strip()
            
            try:
                return json.loads(cleaned_response)
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse JSON from technology analysis: {cleaned_response[:200]}")
                return {
                    "technology_domain": "Unknown",
                    "key_innovations": ["Unable to analyze"],
                    "technical_maturity": "UNKNOWN",
                    "standards_relevance": "UNKNOWN",
                    "implementation_complexity": "UNKNOWN"
                }
            
        except Exception as e:
            logger.error(f"Technology analysis failed: {e}")
            return {
                "technology_domain": "Unknown",
                "key_innovations": ["Unable to analyze"],
                "technical_maturity": "UNKNOWN",
                "standards_relevance": "UNKNOWN",
                "implementation_complexity": "UNKNOWN"
            }
    
    @observe(name="analyze_competitive_position")
    async def _analyze_competitive_position(self, patent_data: Dict) -> Dict[str, Any]:
        """Analyze competitive aspects"""
        try:
            assignees = patent_data.get("assignees", [])
            assignee_names = [a.get("assignee_organization", "") for a in assignees[:2]]  # Limit for token efficiency
            
            prompt = f"""Analyze competitive position. Return ONLY JSON.

ASSIGNEES: {assignee_names}
TITLE: {patent_data.get('patent_title', '')[:100]}
YEAR: {patent_data.get('patent_year', '')}

Return ONLY this JSON:
{{
    "assignee_strength": "<STRONG|MEDIUM|WEAK>",
    "market_position": "<LEADER|FOLLOWER|NICHE>",
    "patent_strategy": "<OFFENSIVE|DEFENSIVE|LICENSING>",
    "competitive_threat": "<HIGH|MEDIUM|LOW>"
}}"""
            
            response = await self._call_llm(prompt)
            
            # Clean response and handle non-JSON responses
            cleaned_response = response.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            cleaned_response = cleaned_response.strip()
            
            try:
                return json.loads(cleaned_response)
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse JSON from competitive analysis: {cleaned_response[:200]}")
                return {
                    "assignee_strength": "UNKNOWN",
                    "market_position": "UNKNOWN",
                    "patent_strategy": "UNKNOWN",
                    "competitive_threat": "UNKNOWN"
                }
            
        except Exception as e:
            logger.error(f"Competitive analysis failed: {e}")
            return {
                "assignee_strength": "UNKNOWN",
                "market_position": "UNKNOWN",
                "patent_strategy": "UNKNOWN",
                "competitive_threat": "UNKNOWN"
            }
    
    @observe(name="patent_analyzer_llm_call")
    async def _call_llm(self, prompt: str) -> str:
        """Make async call to Azure OpenAI with proper error handling and fixes"""
        try:
            # FIX 9: Use same fixes as QueryGenerator
            base_url = self.config.azure_endpoint.rstrip('/')
            url = f"{base_url}/openai/deployments/{self.config.azure_deployment}/chat/completions?api-version={self.config.azure_api_version}"
            
            headers = {
                "Content-Type": "application/json",
                "api-key": self.config.azure_api_key
            }
            
            # Clean and validate prompt
            cleaned_prompt = self._clean_text_for_api(prompt)
            if len(cleaned_prompt) > 50000:  # More conservative limit for gpt-4o-mini
                logger.warning(f"Prompt is very long: {len(cleaned_prompt)} characters, truncating...")
                cleaned_prompt = cleaned_prompt[:50000] + "\n\n[Content truncated for length - analysis continues with available data...]"
            
            payload = {
                "messages": [
                    {"role": "system", "content": "You are a professional patent analysis expert providing technical assessments."},
                    {"role": "user", "content": cleaned_prompt}
                ],
                "max_tokens": 8000,  # Compatible with gpt-4o-mini limits (16384 max)
                "temperature": 0.1
            }
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(url, headers=headers, json=payload)
                
                if response.status_code == 200:
                    result = response.json()
                    content = result['choices'][0]['message']['content'].strip()
                    logger.info(f"✅ LLM call successful, response length: {len(content)} characters")
                    return content
                else:
                    error_details = f"Status {response.status_code}: {response.text[:500]}"
                    logger.error(f"LLM call failed: {error_details}")
                    raise APIError(f"Azure OpenAI API returned {response.status_code}: {response.text[:200]}")
                    
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error in LLM call: {e}")
            logger.error(f"Response content: {e.response.text[:500] if hasattr(e, 'response') else 'No response content'}")
            raise APIError(f"HTTP error: {e}")
        except httpx.RequestError as e:
            logger.error(f"Request error in LLM call: {e}")
            logger.error(f"Request error type: {type(e).__name__}")
            logger.error(f"Request error details: {str(e)}")
            raise APIError(f"Request error: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in LLM call: {e}")
            raise APIError(f"Invalid JSON response: {e}")
        except Exception as e:
            logger.error(f"LLM call failed with unexpected error: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Error details: {str(e)}")
            raise APIError(f"Unexpected error in LLM call: {e}")
    
    def _clean_text_for_api(self, text: str) -> str:
        """Clean text to avoid API issues"""
        # Remove or replace problematic characters
        cleaned = text.replace('\x00', '')  # Remove null bytes
        cleaned = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', cleaned)  # Remove control characters
        # Normalize whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned)
        return cleaned.strip()

class ReportGenerator:
    """Generate comprehensive patent analysis reports"""
    
    def __init__(self, config: PatentSearchConfig):
        self.config = config
    
    @observe(name="generate_comprehensive_report")
    async def generate_comprehensive_report(self, search_result: SearchResult) -> str:
        """Generate a comprehensive patent analysis report with consistent markdown formatting"""
        try:
            # Handle empty results gracefully
            if not search_result.patents:
                return self._generate_empty_report(search_result)
            
            # Prepare patent data for LLM (include analyzed patents up to configured limit)
            analyzed_patents = search_result.patents  # Get all analyzed patents
            report_patents = analyzed_patents[:self.config.report_patent_limit] if len(analyzed_patents) > self.config.report_patent_limit else analyzed_patents
            
            # Create structured data for the report
            patent_summaries = self._prepare_patent_summaries(report_patents)
            
            # Generate report using structured approach
            report = await self._generate_structured_report(search_result, patent_summaries)
            
            # Validate and clean markdown
            cleaned_report = self._clean_markdown_formatting(report)
            
            return cleaned_report
            
        except APIError as e:
            logger.error(f"API error in report generation: {e}")
            return self._generate_error_report(search_result.query, f"API Error: {str(e)}")
        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return self._generate_error_report(search_result.query, f"Unexpected error: {str(e)}")
    
    def _generate_empty_report(self, search_result: SearchResult) -> str:
        """Generate a consistent report when no patents are found"""
        return f"""# Prior Art Search Report

## Search Query
**"{search_result.query}"**

## Executive Summary
No patents were found matching the search criteria. This could indicate either:
- A very novel area with limited prior art
- Search terms that need refinement
- Technical domain outside current patent databases

## Recommendations
1. **Broaden Search Terms**: Try more general or alternative terminology
2. **Check Related Fields**: Explore adjacent technology domains
3. **Manual Search**: Consider direct searches in USPTO, EPO, or Google Patents
4. **Professional Search**: Engage a patent search specialist for complex queries

## Search Details
- **Search Date**: {search_result.timestamp}
- **Strategies Executed**: {len(search_result.search_strategies)}
- **Patents Found**: 0
- **Database Status**: Connected successfully

---
*Report generated by AI Patent Analysis System*
"""

    def _create_human_readable_query_explanation(self, query: Dict, strategy_name: str) -> str:
        """
        Convert technical API query parameters into human-readable explanations.
        
        Args:
            query: Dictionary containing PatentsView API query parameters
            strategy_name: Name of the search strategy for context
            
        Returns:
            Human-readable explanation of what the search query does
        """
        explanations = []
        
        # Handle text phrase searches
        if "_text_phrase" in query:
            for field, terms in query["_text_phrase"].items():
                field_name = field.replace("patent_", "").replace("_", " ").title()
                explanations.append(f"Search for exact phrase '{terms}' in {field_name}")
        
        # Handle text any searches  
        if "_text_any" in query:
            for field, terms in query["_text_any"].items():
                field_name = field.replace("patent_", "").replace("_", " ").title()
                term_list = terms.split() if isinstance(terms, str) else terms
                explanations.append(f"Search for any of these terms in {field_name}: {', '.join(term_list)}")
        
        # Handle text all searches
        if "_text_all" in query:
            for field, terms in query["_text_all"].items():
                field_name = field.replace("patent_", "").replace("_", " ").title()
                term_list = terms.split() if isinstance(terms, str) else terms
                explanations.append(f"Search for ALL these terms in {field_name}: {', '.join(term_list)}")
        
        # Handle exact matches (direct field filters)
        direct_filters = {k: v for k, v in query.items() if not k.startswith("_")}
        if direct_filters:
            for field, value in direct_filters.items():
                field_name = field.replace("_", " ").title()
                if isinstance(value, list):
                    explanations.append(f"Filter by {field_name}: {', '.join(map(str, value))}")
                else:
                    explanations.append(f"Filter by {field_name}: {value}")
        
        # Handle nested conditions
        if "_and" in query:
            explanations.append("Combined with AND logic:")
            for condition in query["_and"]:
                nested_explanation = self._create_human_readable_query_explanation(condition, strategy_name)
                explanations.append(f"  • {nested_explanation}")
        
        if "_or" in query:
            explanations.append("Any of these conditions (OR logic):")
            for condition in query["_or"]:
                nested_explanation = self._create_human_readable_query_explanation(condition, strategy_name)
                explanations.append(f"  • {nested_explanation}")
        
        # Handle special text searches
        if "_text_contains" in query:
            for field, terms in query["_text_contains"].items():
                field_name = field.replace("patent_", "").replace("_", " ").title()
                explanations.append(f"Search for terms containing '{terms}' in {field_name}")
        
        if not explanations:
            return f"Complex query for {strategy_name} strategy"
        
        return "; ".join(explanations)

    def _prepare_patent_summaries(self, patents: List[PatentAnalysis]) -> List[Dict]:
        """Prepare comprehensive patent summaries for enhanced report generation"""
        summaries = []
        for patent in patents:
            # Extract key claims for technical depth
            key_claims = []
            independent_claims = [c for c in patent.claims if c.claim_type == "independent"]
            if independent_claims:
                # Include first 5 independent claims for comprehensive technical analysis
                for claim in independent_claims[:5]:
                    key_claims.append({
                        "number": claim.claim_number,
                        "text": claim.claim_text[:400] + "..." if len(claim.claim_text) > 400 else claim.claim_text,
                        "type": claim.claim_type
                    })
            
            # Extract key inventors (up to 5)
            key_inventors = patent.inventors[:5] if patent.inventors else ["Not available"]
            
            summary = {
                "patent_id": patent.patent_id,
                "title": patent.title,  # Include full title for better analysis
                "abstract": patent.abstract[:600] + "..." if len(patent.abstract) > 600 else patent.abstract,  # Include substantial abstract
                "publication_date": patent.publication_date or f"{patent.patent_year}" if patent.patent_year else "Unknown",
                "inventors": key_inventors,
                "assignees": patent.assignees[:5],  # Include up to 5 assignees
                "relevance_score": patent.relevance_score,
                "risk_assessment": {
                    "overall_risk": patent.risk_assessment.get("overall_risk", "UNKNOWN"),
                    "blocking_potential": patent.risk_assessment.get("blocking_potential", "UNKNOWN"),
                    "design_around_difficulty": patent.risk_assessment.get("design_around_difficulty", "UNKNOWN"),
                    "commercial_impact": patent.risk_assessment.get("commercial_impact", "UNKNOWN"),
                    "reasoning": patent.risk_assessment.get("reasoning", "Not available"),
                    "specific_concerns": patent.risk_assessment.get("specific_concerns", [])
                },
                "technical_analysis": {
                    "technology_domain": patent.technical_analysis.get("technology_domain", "Unknown"),
                    "key_innovations": patent.technical_analysis.get("key_innovations", []),
                    "technical_maturity": patent.technical_analysis.get("technical_maturity", "UNKNOWN"),
                    "standards_relevance": patent.technical_analysis.get("standards_relevance", "UNKNOWN"),
                    "implementation_complexity": patent.technical_analysis.get("implementation_complexity", "UNKNOWN")
                },
                "competitive_insights": {
                    "assignee_strength": patent.competitive_insights.get("assignee_strength", "UNKNOWN"),
                    "market_position": patent.competitive_insights.get("market_position", "UNKNOWN"),
                    "patent_strategy": patent.competitive_insights.get("patent_strategy", "UNKNOWN"),
                    "competitive_threat": patent.competitive_insights.get("competitive_threat", "UNKNOWN")
                },
                "key_claims": key_claims,
                "total_claims": len(patent.claims),
                "source_strategy": patent.source_strategy
            }
            summaries.append(summary)
        return summaries
    
    @observe(name="generate_structured_report")
    async def _generate_structured_report(self, search_result: SearchResult, patent_summaries: List[Dict]) -> str:
        """Generate comprehensive report with detailed technical analysis"""
        
        # Prepare comprehensive search context
        search_context = {
            "query": search_result.query,
            "total_found": search_result.total_found,
            "timestamp": search_result.timestamp,
            "strategies_executed": len(search_result.search_strategies),
            "unique_patents_searched": search_result.metadata.get("unique_patents_found", 0),
            "relevance_threshold": search_result.metadata.get("relevance_threshold", 0.3)
        }
        
        # Prepare strategy information
        strategy_info = []
        for strategy in search_result.search_strategies:
            strategy_info.append({
                "name": strategy.name,
                "description": strategy.description,
                "focus": strategy.technical_focus,
                "scope": strategy.coverage_scope,
                "query": strategy.query
            })
        
        # Prepare technology landscape analysis
        tech_landscape = search_result.technology_landscape
        competitive_analysis = search_result.competitive_analysis
        
        # Create comprehensive prompt with all available data
        report_prompt = f""" CRITICAL MANDATORY INSTRUCTION
Throughout this ENTIRE report, you MUST use the EXACT patent IDs and titles listed in the Patent Inventory below. 

FORBIDDEN ACTIONS:
- NEVER create fake patent numbers like "US12,345,678" or "US87,654,321" 
- NEVER write "Patent 1", "Patent 2", or generic placeholders
- NEVER invent or modify patent IDs or titles

REQUIRED FORMAT for patent references:
Use exactly: "PATENT_ID: EXACT_TITLE_FROM_INVENTORY"
Examples based on inventory below:
- "12256231: Cell search during dynamic spectrum sharing (DSS) operation"
- "12192952: Efficient positioning enhancement for dynamic spectrum sharing"

📋 PATENT INVENTORY (THESE ARE THE ONLY PATENTS YOU CAN REFERENCE):
{self._format_patent_inventory(patent_summaries)}

As a senior patent attorney and technology analyst, write a comprehensive prior art search report for "{search_context['query']}".

SEARCH OVERVIEW:
- Total patents analyzed: {search_context['total_found']}
- Search date: {search_context['timestamp']}
- Search strategies: {search_context['strategies_executed']}
- Database patents reviewed: {search_context['unique_patents_searched']}
- Relevance threshold: {search_context['relevance_threshold']}

SEARCH STRATEGIES EMPLOYED:
{self._format_strategies(strategy_info)}

{self._format_detailed_patents(patent_summaries)}

You MUST generate a report using this EXACT structure and section format. DO NOT deviate from this structure:

# Prior Art Search Report

## 1. Executive Summary
[Provide comprehensive overview of findings, key patents, and main insights]

## 2. Search Methodology & Criteria
[MANDATORY SUBSECTIONS - Include ALL of these:]

### 2.1 Search Overview
[Overall approach and objectives]

### 2.2 Search Strategies Detailed Analysis
[For EACH strategy, include:]
- **Strategy Name and Description**
- **Human-Readable Search Logic**: [Explain in plain English what was searched]
- **PatentsView API Query**: [Show exact JSON query used]
- **Results Summary**: [How many patents found, key insights]

### 2.3 Coverage and Comprehensiveness
[How strategies ensure complete coverage]

## 3. Individual Patent Deep Analysis
[Detailed analysis of EACH patent in inventory - use exact patent IDs and titles]

## 4. Technology Analysis
[Analyze technology domains, trends, innovation areas]

## 5. Patent Risk Assessment Summary
[Overall risk landscape, blocking potential, design-around opportunities]

## 6. Competitive Intelligence
[Market positions, key players, patent strategies]

## 7. Claims Analysis Summary  
[Key technical aspects from patent claims, innovation patterns]

## 8. Strategic Recommendations
[Actionable recommendations for IP strategy]

## 9. Conclusion and Next Steps
[Summary and recommended follow-up actions]

🚨🚨🚨 MANDATORY FORMATTING REQUIREMENTS 🚨🚨🚨
- Use EXACT section headers as shown above (including numbering)
- Include ALL 9 sections - do not skip any
- Use exact patent IDs and titles from Patent Inventory only
- Follow the detailed subsection structure for Section 2
- Make each section substantial with detailed analysis
- Do NOT combine sections or use different numbering
- Do NOT use simplified headings like "Key Patents" instead of "Individual Patent Deep Analysis"
- Do NOT skip the detailed search methodology subsections
- Each section must have substantial content (minimum 2-3 paragraphs per section)

🎯 SECTION COMPLETION CHECKLIST - VERIFY ALL ARE INCLUDED:
□ 1. Executive Summary
□ 2. Search Methodology & Criteria (with 2.1, 2.2, 2.3 subsections)  
□ 3. Individual Patent Deep Analysis
□ 4. Technology Analysis
□ 5. Patent Risk Assessment Summary
□ 6. Competitive Intelligence
□ 7. Claims Analysis Summary
□ 8. Strategic Recommendations
□ 9. Conclusion and Next Steps

START YOUR RESPONSE WITH: "# Prior Art Search Report"
"""

        # Call LLM with comprehensive prompt
        analyzer = PatentAnalyzer(self.config)
        
        # Log prompt details for debugging
        logger.info(f"📝 Report prompt length: {len(report_prompt)} characters")
        logger.info(f"🔍 Patent summaries count: {len(patent_summaries)}")
        logger.info(f"📊 Search strategies count: {len(strategy_info)}")
        
        # Check if prompt is too long
        if len(report_prompt) > 45000:  # Conservative limit
            logger.warning(f"⚠️ Report prompt is very long ({len(report_prompt)} chars), using simplified prompt...")
            # Use simplified prompt for very long cases
            simplified_prompt = self._create_simplified_report_prompt(search_result, patent_summaries)
            report = await analyzer._call_llm(simplified_prompt)
        else:
            try:
                report = await analyzer._call_llm(report_prompt)
            except Exception as e:
                logger.warning(f"⚠️ Full prompt failed ({e}), trying simplified prompt...")
                simplified_prompt = self._create_simplified_report_prompt(search_result, patent_summaries)
                try:
                    report = await analyzer._call_llm(simplified_prompt)
                except Exception as e2:
                    logger.error(f"⚠️ Simplified prompt also failed ({e2}), creating minimal report...")
                    report = self._create_minimal_report(search_result, patent_summaries)
        
        return report
    
    def _create_simplified_report_prompt(self, search_result: SearchResult, patent_summaries: List[Dict]) -> str:
        """Create a simplified report prompt for cases where the full prompt fails"""
        logger.info("📝 Creating simplified report prompt...")
        
        # Create basic patent list - limit to top 10 patents for token efficiency
        patent_list = []
        top_patents = patent_summaries[:10]  # Limit to top 10 patents
        for i, patent in enumerate(top_patents, 1):
            patent_list.append(f"{i}. {patent['patent_id']}: {patent['title'][:80]}...")
            patent_list.append(f"   Relevance: {patent['relevance_score']:.2f} | {patent['assignees'][0] if patent['assignees'] else 'No assignee'}")
        
        patent_inventory = "\n".join(patent_list)
        
        # Simplified strategy overview
        strategy_summary = []
        for i, strategy in enumerate(search_result.search_strategies[:3], 1):  # Limit to 3 strategies
            strategy_summary.append(f"Strategy {i}: {strategy.name} - {strategy.description[:50]}...")
        
        strategies_text = "\n".join(strategy_summary)
        
        simplified_prompt = f"""Generate a structured patent search report for: "{search_result.query}"

PATENT INVENTORY (USE EXACT IDs and TITLES):
{patent_inventory}

SEARCH OVERVIEW:
{strategies_text}

SEARCH STATISTICS:
- Total patents: {search_result.total_found}
- Search date: {search_result.timestamp}
- Strategies: {len(search_result.search_strategies)}

REQUIRED REPORT STRUCTURE (USE EXACT HEADINGS):

# Prior Art Search Report

## 1. Executive Summary
[Brief overview of search results and key findings]

## 2. Search Methodology & Criteria
[How the search was conducted, strategies used]

## 3. Individual Patent Deep Analysis
[Detailed analysis of each patent using exact patent IDs from inventory above]

## 4. Technology Analysis
[Technology domains and trends identified]

## 5. Patent Risk Assessment Summary
[Overall risk landscape and potential blocking patents]

## 6. Competitive Intelligence
[Key players and market positions]

## 7. Claims Analysis Summary
[Technical insights from patent claims]

## 8. Strategic Recommendations
[Actionable recommendations]

## 9. Conclusion and Next Steps
[Summary and follow-up actions]

CRITICAL: Use exact patent IDs and titles from the Patent Inventory. Follow the numbered section structure exactly."""

        return simplified_prompt
    
    def _create_minimal_report(self, search_result: SearchResult, patent_summaries: List[Dict]) -> str:
        """Create a minimal report without LLM when all else fails"""
        logger.info("📝 Creating minimal fallback report...")
        
        # Create basic patent list
        patent_list = []
        for i, patent in enumerate(patent_summaries, 1):
            patent_list.append(f"**{patent['patent_id']}**: {patent['title']}")
            patent_list.append(f"- Assignee: {patent['assignees'][0] if patent['assignees'] else 'Not available'}")
            patent_list.append(f"- Relevance Score: {patent['relevance_score']:.2f}")
            patent_list.append(f"- Date: {patent['publication_date']}")
            patent_list.append("")
        
        patents_section = "\n".join(patent_list)
        
        # Create strategy list
        strategy_list = []
        for i, strategy in enumerate(search_result.search_strategies, 1):
            strategy_list.append(f"**Strategy {i}**: {strategy.name}")
            strategy_list.append(f"- Description: {strategy.description}")
            strategy_list.append(f"- Focus: {strategy.technical_focus}")
            strategy_list.append("")
        
        strategies_section = "\n".join(strategy_list)
        
        minimal_report = f"""# Prior Art Search Report

## Search Query
**"{search_result.query}"**

## Executive Summary
Found {len(patent_summaries)} relevant patents through {len(search_result.search_strategies)} search strategies. The patents show various levels of relevance to the query, with scores ranging from {min(p['relevance_score'] for p in patent_summaries):.2f} to {max(p['relevance_score'] for p in patent_summaries):.2f}.

## Search Methodology
{strategies_section}

## Search Statistics
- **Search Date**: {search_result.timestamp}
- **Total Patents Found**: {search_result.total_found}
- **Patents Analyzed**: {len(patent_summaries)}
- **Search Strategies Used**: {len(search_result.search_strategies)}
- **Relevance Threshold**: {search_result.metadata.get('relevance_threshold', 'N/A')}

## Patent Inventory

{patents_section}

## Summary
This search identified {len(patent_summaries)} patents of potential relevance to "{search_result.query}". Further detailed analysis would be needed to assess specific technical overlaps and patent risks.

---
*Report generated by AI Patent Analysis System - Minimal Mode*
"""
        
        return minimal_report
    
    def _format_strategies(self, strategy_info: List[Dict]) -> str:
        """Format search strategies for the report prompt with detailed PatentsView API queries and human-readable explanations"""
        formatted = []
        for i, strategy in enumerate(strategy_info, 1):
            # Get the actual query used
            query_details = strategy.get('query', {})
            query_json = json.dumps(query_details, indent=2) if query_details else "Query not available"
            
            # Create human-readable explanation
            human_readable = self._create_human_readable_query_explanation(query_details, strategy.get('name', ''))
            
            formatted.append(f"""
STRATEGY {i}: {strategy['name']}
Description: {strategy['description']}
Technical Focus: {strategy['focus']}
Coverage Scope: {strategy['scope']}

HUMAN-READABLE SEARCH LOGIC:
{human_readable}

PatentsView API Query (Technical Details):
{query_json}
""")
        
        return "\n".join(formatted)
    
    def _format_patent_inventory(self, patent_summaries: List[Dict]) -> str:
        """Format a quick patent inventory for reference at the top of the prompt"""
        inventory = []
        for i, patent in enumerate(patent_summaries, 1):
            assignee_list = patent['assignees'] if patent['assignees'] else ["No assignee"]
            primary_assignee = assignee_list[0] if assignee_list else "No assignee"
            inventory.append(f"📍 {patent['patent_id']}: {patent['title']}")
            inventory.append(f"   └─ Assignee: {primary_assignee} | Relevance: {patent['relevance_score']:.2f} | Date: {patent['publication_date']}")
            inventory.append("")  # Add blank line for readability
        return "\n".join(inventory)
    
    def _format_detailed_patents(self, patent_summaries: List[Dict]) -> str:
        """Format detailed patent information for comprehensive analysis"""
        formatted_patents = []
        
        for i, patent in enumerate(patent_summaries, 1):
            patent_text = f"""
PATENT {i}: {patent['patent_id']}
Title: {patent['title']}
Publication: {patent['publication_date']}
Assignee(s): {', '.join(patent['assignees'])}
Inventor(s): {', '.join(patent['inventors'])}
Relevance Score: {patent['relevance_score']:.2f}

Abstract: {patent['abstract']}

Technical Analysis:
- Domain: {patent['technical_analysis']['technology_domain']}
- Key Innovations: {', '.join(patent['technical_analysis']['key_innovations'])}
- Maturity: {patent['technical_analysis']['technical_maturity']}
- Standards Relevance: {patent['technical_analysis']['standards_relevance']}
- Implementation Complexity: {patent['technical_analysis']['implementation_complexity']}

Risk Assessment:
- Overall Risk: {patent['risk_assessment']['overall_risk']}
- Blocking Potential: {patent['risk_assessment']['blocking_potential']}
- Design-Around Difficulty: {patent['risk_assessment']['design_around_difficulty']}
- Commercial Impact: {patent['risk_assessment']['commercial_impact']}
- Risk Reasoning: {patent['risk_assessment']['reasoning']}
- Specific Concerns: {', '.join(patent['risk_assessment']['specific_concerns'])}

Competitive Analysis:
- Assignee Strength: {patent['competitive_insights']['assignee_strength']}
- Market Position: {patent['competitive_insights']['market_position']}
- Patent Strategy: {patent['competitive_insights']['patent_strategy']}
- Competitive Threat: {patent['competitive_insights']['competitive_threat']}

Key Claims ({patent['total_claims']} total):"""
            
            for claim in patent['key_claims']:
                patent_text += f"\n- Claim {claim['number']} ({claim['type']}): {claim['text']}"
            
            patent_text += f"\nSource Strategy: {patent['source_strategy']}\n"
            formatted_patents.append(patent_text)
        
        return "\n".join(formatted_patents)
    
    def _clean_markdown_formatting(self, report: str) -> str:
        """Clean and validate markdown formatting"""
        
        # Remove any JSON blocks that might have leaked through
        report = re.sub(r'```json.*?```', '', report, flags=re.DOTALL)
        report = re.sub(r'```.*?```', '', report, flags=re.DOTALL)
        
        # Fix header spacing
        report = re.sub(r'\n#+', r'\n\n##', report)
        report = re.sub(r'\n\n\n+', r'\n\n', report)
        
        # Ensure consistent bullet points
        report = re.sub(r'\n\s*[•·]\s*', r'\n- ', report)
        
        # Clean up extra whitespace
        report = re.sub(r'[ \t]+$', '', report, flags=re.MULTILINE)
        
        return report.strip()
    
    def _generate_error_report(self, query: str, error: str) -> str:
        """Generate a consistent error report"""
        return f"""# Prior Art Search Report - Error

## Search Query
**"{query}"**

## Status
❌ **Search Failed**

## Error Details
```
{error}
```

## Troubleshooting
1. **Check Configuration**: Verify API keys and endpoints
2. **Network Issues**: Confirm internet connectivity
3. **Service Status**: Check if patent databases are accessible
4. **Query Format**: Ensure search terms are properly formatted

## Next Steps
- Review system logs for detailed error information
- Contact support if the issue persists
- Try a simplified search query

---
*Error report generated at {datetime.now().isoformat()}*
"""


class PatentSearchEngine:
    """Main patent search engine orchestrating all components"""
    
    def __init__(self, config: Optional[PatentSearchConfig] = None):
        self.config = config or PatentSearchConfig()
        self.query_generator = QueryGenerator(self.config)
        self.analyzer = PatentAnalyzer(self.config)
        self.report_generator = ReportGenerator(self.config)
    
    @observe(name="patent_search")
    async def search(self, query: str, max_results: int = None, relevance_threshold: float = None) -> SearchResult:
        """Perform comprehensive patent search with analysis"""
        max_results = max_results or self.config.default_max_results
        relevance_threshold = relevance_threshold or self.config.default_relevance_threshold
        
        logger.info(f"Starting enhanced patent search for: '{query}'")
        
        try:
            # Generate search strategies
            strategies = await self.query_generator.generate_search_strategies(query)
            logger.info(f"Generated {len(strategies)} search strategies")
            
            # Execute searches IN PARALLEL for massive speed improvement
            all_patents = []
            async with EnhancedPatentsViewAPI(self.config) as api:
                # Create parallel tasks for all strategies
                strategy_tasks = [
                    api.search_patents_async(strategy) for strategy in strategies
                ]
                
                # Execute all strategies concurrently
                logger.info(f"Executing {len(strategies)} search strategies in parallel...")
                strategy_results = await asyncio.gather(*strategy_tasks, return_exceptions=True)
                
                # Collect results and handle any exceptions
                for i, result in enumerate(strategy_results):
                    if isinstance(result, Exception):
                        logger.error(f"Strategy {strategies[i].name} failed with exception: {result}")
                        continue
                    elif isinstance(result, list):
                        logger.info(f"Strategy {strategies[i].name}: {len(result)} patents")
                        all_patents.extend(result)
                    else:
                        logger.warning(f"Strategy {strategies[i].name}: unexpected result type {type(result)}")
            
            # Remove duplicates by patent ID
            unique_patents = {}
            for patent in all_patents:
                patent_id = patent.get("patent_id")
                if patent_id and patent_id not in unique_patents:
                    unique_patents[patent_id] = patent
            
            patent_list = list(unique_patents.values())
            logger.info(f"Found {len(patent_list)} unique patents")
            
            # OPTIMIZATION: Phase 1 - Parallel quick relevance filtering
            logger.info("Phase 1: Parallel quick relevance filtering...")
            
            # Create batches for parallel processing
            batch_size = self.config.batch_size
            patent_batches = [patent_list[i:i + batch_size] for i in range(0, len(patent_list), batch_size)]
            
            relevant_patents = []
            for batch in patent_batches:
                # Process each batch in parallel
                batch_tasks = [
                    self.analyzer.quick_relevance_check(patent_data, query) 
                    for patent_data in batch
                ]
                
                batch_scores = await asyncio.gather(*batch_tasks)
                
                # Collect patents that meet threshold
                for patent_data, score in zip(batch, batch_scores):
                    if score >= relevance_threshold:
                        relevant_patents.append((patent_data, score))
            
            logger.info(f"Phase 1 complete: {len(relevant_patents)}/{len(patent_list)} patents passed relevance threshold")
            
            # Sort by quick relevance and limit to reduce claims API calls
            relevant_patents.sort(key=lambda x: x[1], reverse=True)
            top_relevant = relevant_patents[:max_results * 2]  # Get 2x to allow for some filtering
            
            # OPTIMIZATION: Phase 2 - Parallel detailed analysis with claims
            logger.info(f"Phase 2: Parallel detailed analysis for {len(top_relevant)} relevant patents...")
            
            # Process in smaller batches to avoid API rate limits
            analysis_batch_size = min(3, self.config.batch_size)  # Smaller batches for claims API
            analysis_batches = [top_relevant[i:i + analysis_batch_size] for i in range(0, len(top_relevant), analysis_batch_size)]
            
            analyzed_patents = []
            for batch in analysis_batches:
                # Process each batch in parallel
                batch_tasks = [
                    self.analyzer.analyze_patent_with_claims(patent_data, query) 
                    for patent_data, _ in batch
                ]
                
                batch_analyses = await asyncio.gather(*batch_tasks, return_exceptions=True)
                
                # Collect successful analyses
                for analysis in batch_analyses:
                    if isinstance(analysis, PatentAnalysis):
                        analyzed_patents.append(analysis)
                    else:
                        logger.error(f"Patent analysis failed: {analysis}")
            
            # Final sort by detailed relevance score
            analyzed_patents.sort(key=lambda x: x.relevance_score, reverse=True)
            
            # Limit final results
            final_patents = analyzed_patents[:max_results]
            
            # Generate landscape and competitive analysis
            technology_landscape = await self._analyze_technology_landscape(final_patents, query)
            competitive_analysis = self._analyze_competitive_landscape(final_patents)
            
            logger.info(f"Search complete: {len(final_patents)} patents analyzed (saved {len(patent_list) - len(top_relevant)} claims API calls)")
            
            # Create search result
            search_result = SearchResult(
                query=query,
                total_found=len(final_patents),
                patents=final_patents,
                search_strategies=strategies,
                technology_landscape=technology_landscape,
                competitive_analysis=competitive_analysis,
                timestamp=datetime.now().isoformat(),
                metadata={
                    "relevance_threshold": relevance_threshold,
                    "max_results": max_results,
                    "unique_patents_found": len(patent_list),
                    "strategies_executed": len(strategies)
                }
            )
            
            return search_result
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise
    
    async def generate_report(self, search_result: SearchResult) -> str:
        """Generate comprehensive patent analysis report"""
        try:
            logger.info("Generating comprehensive patent analysis report...")
            return await self.report_generator.generate_comprehensive_report(search_result)
        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise
    
    async def _analyze_technology_landscape(self, patents: List[PatentAnalysis], query: str) -> Dict[str, Any]:
        """Analyze the overall technology landscape"""
        try:
            domains = {}
            innovations = []
            maturity_dist = self._analyze_maturity_distribution(patents)
            
            for patent in patents:
                # Collect technology domains
                domain = patent.technical_analysis.get("technology_domain", "Unknown")
                domains[domain] = domains.get(domain, 0) + 1
                
                # Collect innovations
                patent_innovations = patent.technical_analysis.get("key_innovations", [])
                innovations.extend(patent_innovations)
            
            # Calculate average relevance
            avg_relevance = sum(p.relevance_score for p in patents) / len(patents) if patents else 0
            
            return {
                "technology_domains": domains,
                "key_innovation_areas": list(set(innovations)),
                "avg_relevance": avg_relevance,
                "maturity_distribution": maturity_dist
            }
            
        except Exception as e:
            logger.error(f"Technology landscape analysis failed: {e}")
            return {
                "technology_domains": {},
                "key_innovation_areas": [],
                "avg_relevance": 0,
                "maturity_distribution": {}
            }
    
    def _analyze_competitive_landscape(self, patents: List[PatentAnalysis]) -> Dict[str, Any]:
        """Analyze competitive landscape from patents"""
        try:
            assignee_counts = {}
            market_leaders = []
            
            for patent in patents:
                for assignee in patent.assignees:
                    assignee_counts[assignee] = assignee_counts.get(assignee, 0) + 1
                    
                    # Identify market leaders based on assignee strength
                    strength = patent.competitive_insights.get("assignee_strength", "")
                    if strength == "STRONG" and assignee not in market_leaders:
                        market_leaders.append(assignee)
            
            # Sort assignees by patent count
            top_assignees = dict(sorted(assignee_counts.items(), key=lambda x: x[1], reverse=True)[:10])
            
            return {
                "top_assignees": top_assignees,
                "market_leaders": market_leaders,
                "total_assignees": len(assignee_counts)
            }
            
        except Exception as e:
            logger.error(f"Competitive landscape analysis failed: {e}")
            return {
                "top_assignees": {},
                "market_leaders": [],
                "total_assignees": 0
            }
    
    def _analyze_maturity_distribution(self, patents: List[PatentAnalysis]) -> Dict[str, int]:
        """Analyze technology maturity distribution"""
        maturity_dist = {}
        for patent in patents:
            maturity = patent.technical_analysis.get("technical_maturity", "UNKNOWN")
            maturity_dist[maturity] = maturity_dist.get(maturity, 0) + 1
        return maturity_dist