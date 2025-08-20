"""
Optimized Prior Art Search Module with Claims
Uses proven working fields and correct claims endpoint
"""

import os
import json
import logging
import httpx
import time
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import Google Patents client for claims retrieval
try:
    from .google_patents_client import GooglePatentsClient
    GOOGLE_PATENTS_AVAILABLE = True
except ImportError:
    try:
        from google_patents_client import GooglePatentsClient
        GOOGLE_PATENTS_AVAILABLE = True
    except ImportError:
        GOOGLE_PATENTS_AVAILABLE = False
        logging.warning("Google Patents client not available - claims will use PatentsView API only")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class OptimizedPatent:
    """Optimized patent data structure with claims"""
    patent_id: str
    title: str
    abstract: str
    inventors: List[str]
    assignees: List[str]
    claims: List[str]
    relevance_score: float

@dataclass
class OptimizedSearchResult:
    """Optimized search result"""
    query: str
    patents: List[OptimizedPatent]
    total_found: int
    timestamp: str

class OptimizedPatentsViewAPI:
    """Optimized PatentsView API client with claims support"""
    
    def __init__(self, api_key: str = None):
        self.base_url = "https://search.patentsview.org/api/v1"
        self.session = httpx.Client(timeout=30.0)
        self.api_key = api_key or os.getenv("PATENTSVIEW_API_KEY")
        self.last_request_time = 0
        self.min_request_interval = 1.5  # Conservative rate limiting
        
        if not self.api_key:
            logger.warning("No PatentsView API key found")
    
    def _rate_limit(self):
        """Simple rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            logger.info(f"Rate limiting: sleeping for {sleep_time:.2f}s")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def search_patents(self, search_terms: str, max_results: int = 5) -> List[Dict]:
        """Enhanced primary patent search with dynamic query building and optimization"""
        self._rate_limit()
        
        if not search_terms or not search_terms.strip():
            logger.warning("Empty search terms provided")
            return []
        
        # Extract core technical terms using smart extraction
        logger.info(f"Original search terms: '{search_terms}'")
        technical_terms = extract_technical_terms_llm(search_terms)
        logger.info(f"Extracted technical terms: '{technical_terms}'")
        
        # Enhanced field selection for better results (using only supported fields)
        enhanced_fields = [
            "patent_id",
            "patent_title", 
            "patent_abstract",
            "inventors",
            "assignees"
        ]
        
        # Dynamic query building based on EXTRACTED technical terms
        query_strategy = self._build_optimal_query(technical_terms)
        
        payload = {
            "q": query_strategy,
            "f": enhanced_fields,
            "o": {
                "size": min(max_results * 4, 50),  # Get more results for better selection
                "sort": "relevance"  # Add relevance sorting
            }
        }
        
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["X-Api-Key"] = self.api_key
        
        try:
            logger.info(f"Enhanced search: '{technical_terms}' (max_results={max_results})")
            logger.info(f"Query strategy: {query_strategy}")
            
            # Add retry logic for better reliability
            response = self._make_search_request_with_retry(payload, headers)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("error", False):
                    logger.error(f"API error: {data}")
                    return []
                
                patents = data.get("patents", [])
                total_hits = data.get("total_hits", len(patents))
                
                # Check if results are relevant (simple relevance check)
                relevant_patents = self._filter_relevant_patents(patents, technical_terms)
                
                if len(relevant_patents) < max_results:
                    logger.warning(f"PatentsView returned {len(patents)} patents but only {len(relevant_patents)} are relevant")
                    logger.info("Consider using Google Patents as alternative search source")
                
                # Enhanced result processing
                processed_patents = self._process_search_results(relevant_patents, technical_terms)
                
                logger.info(f"Enhanced search successful: {len(processed_patents)} patents, {total_hits} total matches")
                return processed_patents
            else:
                logger.error(f"Search failed with status {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Enhanced search failed: {e}")
            return []
    
    def _filter_relevant_patents(self, patents: List[Dict], search_terms: str) -> List[Dict]:
        """Filter patents to ensure they contain relevant terms"""
        if not patents:
            return []
        
        relevant_patents = []
        search_lower = search_terms.lower()
        search_words = set(search_lower.split())
        
        for patent in patents:
            title = patent.get("patent_title", "").lower()
            abstract = patent.get("patent_abstract", "").lower()
            
            # Check if patent contains at least one search term
            title_match = any(word in title for word in search_words)
            abstract_match = any(word in abstract for word in search_words)
            
            if title_match or abstract_match:
                relevant_patents.append(patent)
            else:
                logger.debug(f"Filtered out irrelevant patent: {patent.get('patent_id', 'Unknown')} - {patent.get('patent_title', 'No title')}")
        
        return relevant_patents
    
    def _build_optimal_query(self, search_terms: str) -> Dict:
        """Build smart query strategy: adaptive based on number of search terms"""
        # Split search terms into individual words
        words = search_terms.strip().split()
        
        if len(words) == 1:
            # Single word: search in title and abstract
            return {
                "_or": [
                    {"_text_any": {"patent_title": search_terms}},
                    {"_text_any": {"patent_abstract": search_terms}}
                ]
            }
        elif len(words) == 2:
            # Two words: use AND strategy for focused results
            return {
                "_and": [
                    {"_or": [{"_text_any": {"patent_title": words[0]}}, {"_text_any": {"patent_abstract": words[0]}}]},
                    {"_or": [{"_text_any": {"patent_title": words[1]}}, {"_text_any": {"patent_abstract": words[1]}}]}
                ]
            }
        elif len(words) == 3:
            # Three words: use AND strategy but more focused
            return {
                "_and": [
                    {"_or": [{"_text_any": {"patent_title": words[0]}}, {"_text_any": {"patent_abstract": words[0]}}]},
                    {"_or": [{"_text_any": {"patent_title": words[1]}}, {"_text_any": {"patent_abstract": words[1]}}]},
                    {"_or": [{"_text_any": {"patent_title": words[2]}}, {"_text_any": {"patent_abstract": words[2]}}]}
                ]
            }
        else:
            # Four or more words: use smart OR strategy for broader coverage
            # Focus on the most important terms (first 3) with AND, then OR for others
            primary_terms = words[:3]
            secondary_terms = words[3:]
            
            # Primary terms with AND (must have at least 2 of the 3 most important terms)
            primary_conditions = []
            for term in primary_terms:
                primary_conditions.append({
                    "_or": [
                        {"_text_any": {"patent_title": term}},
                        {"_text_any": {"patent_abstract": term}}
                    ]
                })
            
            # Secondary terms with OR (bonus if found, but not required)
            secondary_conditions = []
            for term in secondary_terms:
                secondary_conditions.append({
                    "_or": [
                        {"_text_any": {"patent_title": term}},
                        {"_text_any": {"patent_abstract": term}}
                    ]
                })
            
            # Build query: require 2 of 3 primary terms, OR any secondary terms
            if secondary_conditions:
                return {
                    "_or": [
                        {
                            "_and": [
                                {"_or": [primary_conditions[0], primary_conditions[1]]},  # At least 2 of 3 primary
                                {"_or": [primary_conditions[2]]}  # Third primary term
                            ]
                        },
                        {
                            "_and": [
                                {"_or": [primary_conditions[0], primary_conditions[2]]},  # Alternative 2 of 3
                                {"_or": [primary_conditions[1]]}  # Second primary term
                            ]
                        },
                        {
                            "_and": [
                                {"_or": [primary_conditions[1], primary_conditions[2]]},  # Alternative 2 of 3
                                {"_or": [primary_conditions[0]]}  # First primary term
                            ]
                        },
                        {"_or": secondary_conditions}  # Any secondary terms
                    ]
                }
            else:
                # No secondary terms, just require 2 of 3 primary terms
                return {
                    "_or": [
                        {"_and": [primary_conditions[0], primary_conditions[1]]},
                        {"_and": [primary_conditions[0], primary_conditions[2]]},
                        {"_and": [primary_conditions[1], primary_conditions[2]]}
                    ]
                }
    
    def _make_search_request_with_retry(self, payload: Dict, headers: Dict, max_retries: int = 3) -> Any:
        """Make search request with retry logic"""
        for attempt in range(max_retries):
            try:
                response = self.session.post(
                    f"{self.base_url}/patent/",
                    json=payload,
                    headers=headers,
                    timeout=30.0
                )
                return response
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(f"Search attempt {attempt + 1} failed: {e}, retrying...")
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise e
    
    def _process_search_results(self, patents: List[Dict], search_terms: str) -> List[Dict]:
        """Process and enhance search results"""
        if not patents:
            return []
        
        processed_patents = []
        search_lower = search_terms.lower()
        
        for patent in patents:
            # Add relevance scoring
            relevance_score = self._calculate_relevance_score(patent, search_lower)
            patent["relevance_score"] = relevance_score
            
            # Add search metadata
            patent["search_terms"] = search_terms
            patent["search_timestamp"] = time.time()
            
            processed_patents.append(patent)
        
        # Sort by relevance score
        processed_patents.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        
        return processed_patents
    
    def _calculate_relevance_score(self, patent: Dict, search_terms: str) -> float:
        """Calculate relevance score for a patent"""
        score = 0.0
        
        # Title relevance (highest weight)
        title = patent.get("patent_title", "").lower()
        if search_terms in title:
            score += 0.5
        elif any(term in title for term in search_terms.split()):
            score += 0.3
        
        # Abstract relevance
        abstract = patent.get("patent_abstract", "").lower()
        if search_terms in abstract:
            score += 0.3
        elif any(term in abstract for term in search_terms.split()):
            score += 0.2
        
        # Recency bonus (newer patents get slight boost)
        patent_year = patent.get("patent_year")
        if patent_year and patent_year >= 2020:
            score += 0.1
        
        # Normalize score
        return min(1.0, score)
    
    def get_patent_claims(self, patent_id: str) -> List[str]:
        """Get claims for a specific patent using working query structure from PatentsView forum"""
        self._rate_limit()
        
        if not patent_id:
            return []
        
        # Use the working query structure discovered in the PatentsView forum
        # This approach successfully retrieves claims using _and operator
        payload = {
            "f": [
                "patent_id",
                "claim_sequence", 
                "claim_text",
                "claim_number",
                "claim_dependent",
                "exemplary"
            ],
            "o": {
                "size": 100
            },
            "q": {
                "_and": [
                    {"patent_id": patent_id}
                ]
            },
            "s": [
                {"patent_id": "asc"}, 
                {"claim_sequence": "asc"}
            ]
        }
        
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["X-Api-Key"] = self.api_key
        
        try:
            logger.info(f"Fetching claims for patent: {patent_id}")
            
            response = self.session.post(
                f"{self.base_url}/g_claim/",
                json=payload,
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                claims = data.get("g_claims", [])
                claim_texts = []
                
                logger.info(f"Retrieved {len(claims)} claims for patent {patent_id}")
                
                for claim in claims:
                    claim_text = claim.get("claim_text", "")
                    claim_sequence = claim.get("claim_sequence", 0)
                    claim_number = claim.get("claim_number", "")
                    claim_dependent = claim.get("claim_dependent", "")
                    exemplary = claim.get("exemplary", "")
                    
                    if claim_text:
                        # Format claim with number or sequence
                        if claim_number:
                            formatted_claim = f"{claim_number}. {claim_text}"
                        else:
                            # Note: claim_sequence 0 = claim 1, claim_sequence 1 = claim 2, etc.
                            claim_display_number = claim_sequence + 1
                            formatted_claim = f"{claim_display_number}. {claim_text}"
                        
                        # Add metadata if available
                        metadata = []
                        if claim_dependent:
                            metadata.append(f"Dependent: {claim_dependent}")
                        if exemplary:
                            metadata.append(f"Exemplary: {exemplary}")
                        
                        if metadata:
                            formatted_claim += f" [{', '.join(metadata)}]"
                        
                        claim_texts.append(formatted_claim)
                
                # Sort by claim sequence
                claim_texts.sort(key=lambda x: int(x.split('.')[0]) if x.split('.')[0].isdigit() else 0)
                
                logger.info(f"Successfully processed {len(claim_texts)} claims for patent {patent_id}")
                return claim_texts
            else:
                logger.warning(f"Claims endpoint returned {response.status_code} for patent {patent_id}")
                return []
                
        except Exception as e:
            logger.error(f"Claims endpoint failed for patent {patent_id}: {e}")
            return []
    
    def get_patent_claims_hybrid(self, patent_id: str) -> List[str]:
        """
        Hybrid claims retrieval: try PatentsView API first, then Google Patents as fallback
        
        Args:
            patent_id: Patent ID to retrieve claims for
            
        Returns:
            List of claim strings
        """
        if not patent_id:
            return []
        
        # First try PatentsView API
        logger.info(f"Trying PatentsView API for claims: {patent_id}")
        patentsview_claims = self.get_patent_claims(patent_id)
        
        if patentsview_claims:
            logger.info(f"PatentsView API successful: {len(patentsview_claims)} claims")
            return patentsview_claims
        
        # If PatentsView fails, try Google Patents
        if GOOGLE_PATENTS_AVAILABLE:
            logger.info(f"PatentsView API failed, trying Google Patents: {patent_id}")
            try:
                google_client = GooglePatentsClient()
                google_claims = google_client.get_patent_claims(patent_id)
                google_client.close()
                
                if google_claims:
                    logger.info(f"Google Patents successful: {len(google_claims)} claims")
                    return google_claims
                else:
                    logger.info(f"Google Patents also failed: {patent_id}")
                    return []
                    
            except Exception as e:
                logger.error(f"Google Patents claims retrieval failed: {e}")
                return []
        else:
            logger.info("Google Patents client not available")
            return []

def search_prior_art_optimized(search_query: str, max_results: int = 5) -> OptimizedSearchResult:
    """Optimized prior art search with claims using hybrid approach"""
    
    api_client = OptimizedPatentsViewAPI()
    
    # Use the main search method
    patent_data = api_client.search_patents(search_query, max_results)
    
    if not patent_data:
        return OptimizedSearchResult(
            query=search_query,
            patents=[],
            total_found=0,
            timestamp=datetime.now().isoformat()
        )
    
    # Process patents and get claims
    optimized_patents = []
    
    for i, patent in enumerate(patent_data):
        try:
            patent_id = patent.get("patent_id", "")
            if not patent_id:
                continue
            
            # Get claims for this patent using hybrid method
            claims = api_client.get_patent_claims_hybrid(patent_id)
            
            # Extract inventor names
            inventors = []
            for inv in patent.get("inventors", []):
                first = inv.get("inventor_name_first", "")
                last = inv.get("inventor_name_last", "")
                full = f"{first} {last}".strip()
                if full:
                    inventors.append(full)
            
            # Extract assignee organizations
            assignees = []
            for ass in patent.get("assignees", []):
                org = ass.get("assignee_organization", "")
                if org:
                    assignees.append(org)
            
            # Enhanced relevance scoring based on search type
            base_score = max(0.1, 1.0 - (i * 0.2))
            
            # Boost score for spectrum-related searches
            if "spectrum" in search_query.lower() or "sharing" in search_query.lower():
                if any(term in patent.get("patent_title", "").lower() for term in ["spectrum", "sharing", "dynamic", "adaptive"]):
                    base_score += 0.3
            
            relevance_score = min(1.0, base_score)
            
            optimized_patent = OptimizedPatent(
                patent_id=patent_id,
                title=patent.get("patent_title", ""),
                abstract=patent.get("patent_abstract", ""),
                inventors=inventors,
                assignees=assignees,
                claims=claims,
                relevance_score=relevance_score
            )
            
            optimized_patents.append(optimized_patent)
            
        except Exception as e:
            logger.error(f"Error processing patent: {e}")
            continue
    
    # Sort by relevance score
    optimized_patents.sort(key=lambda x: x.relevance_score, reverse=True)
    
    return OptimizedSearchResult(
        query=search_query,
        patents=optimized_patents,
        total_found=len(optimized_patents),
        timestamp=datetime.now().isoformat()
    )

def format_optimized_results(result: OptimizedSearchResult) -> str:
    """Generate professional patent report using LLM with comprehensive prompt"""
    if not result.patents:
        return f"# Prior Art Search Results: {result.query}\n\nNo relevant patents found."
    
    # Prepare patent data for LLM
    patent_data = prepare_patent_data_for_llm(result)
    
    # Create comprehensive prompt
    prompt = create_comprehensive_prompt(patent_data)
    
    # Generate report using LLM
    report = generate_llm_report(prompt)
    
    return report

def prepare_patent_data_for_llm(result: OptimizedSearchResult) -> Dict:
    """Prepare patent data in clean format for LLM processing"""
    patents = []
    
    for patent in result.patents:
        # Clean and prepare patent data
        patent_info = {
            "patent_id": patent.patent_id,
            "title": patent.title,
            "abstract": patent.abstract,
            "inventors": patent.inventors,
            "assignees": patent.assignees,
            "claims": patent.claims,
            "relevance_score": patent.relevance_score,
            "risk_level": "HIGH" if patent.relevance_score >= 0.8 else "MEDIUM" if patent.relevance_score >= 0.5 else "LOW"
        }
        patents.append(patent_info)
    
    return {
        "query": result.query,
        "total_found": result.total_found,
        "timestamp": result.timestamp,
        "patents": patents
    }

def create_comprehensive_prompt(patent_data: Dict) -> str:
    """Create comprehensive prompt for professional patent attorney report with self-reflection"""
    
    prompt = f"""
You are a senior patent attorney with 20+ years of experience in patent law and prior art analysis. Your task is to generate a comprehensive, professional prior art search report that provides actionable business intelligence for inventors and patent attorneys.

## SEARCH CONTEXT
- **Search Query:** {patent_data['query']}
- **Total Patents Found:** {patent_data['total_found']}
- **Patents Analyzed:** {len(patent_data['patents'])}
- **Search Timestamp:** {patent_data['timestamp']}

## PATENT DATA TO ANALYZE
{json.dumps(patent_data['patents'], indent=2)}

## CRITICAL INSTRUCTIONS FOR SELF-REFLECTION AND EVALUATION

### 1. RELEVANCE ASSESSMENT (MANDATORY)
Before including any patent in your report, you MUST evaluate its relevance:

**RELEVANCE CRITERIA:**
- **High Relevance:** Patent directly relates to the search query technology/domain
- **Medium Relevance:** Patent has some connection but may be tangential
- **Low Relevance:** Patent has minimal or no connection to search query
- **Irrelevant:** Patent is completely outside the search domain

**SELF-REFLECTION QUESTIONS:**
- Does this patent actually block the technology described in the search query?
- Is this patent in the same technology domain as the search query?
- Would a patent attorney consider this patent relevant to the search?
- Does this patent contain claims that could realistically block the invention?

### 2. PATENT SELECTION RULES
- **ONLY include patents that are HIGHLY RELEVANT** to the search query
- **EXCLUDE patents that are tangential, unrelated, or outside the domain**
- **PRIORITIZE patents with the strongest blocking potential**
- **LIMIT to 3-5 most relevant patents** unless more are clearly necessary

### 3. QUALITY CONTROL CHECKLIST
Before finalizing your report, ask yourself:
- [ ] Are all included patents highly relevant to the search query?
- [ ] Have I excluded patents that are outside the technology domain?
- [ ] Are the blocking claims actually related to the search technology?
- [ ] Would a patent attorney agree with my relevance assessment?
- [ ] Does this report provide actionable business intelligence?

## REPORT STRUCTURE REQUIREMENTS

### 1. EXECUTIVE SUMMARY (Business Decision Focus)
- **Risk Level:** 🔴 High, 🟡 Medium, 🟢 Low (based on actual blocking potential)
- **Key Blocking Patents:** ONLY the most relevant patents (3-5 maximum)
- **Immediate Action Required:** Yes/No with clear reasoning
- **Business Impact:** Specific, quantifiable impact assessment

### 2. RISK ASSESSMENT MATRIX (Actionable)
- **Patent ID, Title, Risk Level, Specific Blocking Claims, What's Blocking, Action Required**
- **ONLY include patents that actually block the search technology**
- **EXCLUDE patents that are not relevant to the search domain**

### 3. TECHNICAL ANALYSIS (Practical, Not Academic)
- **What's Blocking:** Specific technical overlap with search query
- **What's NOT Blocking:** Clear differentiation opportunities
- **Workaround Options:** Practical technical alternatives
- **Technical Differentiation:** Specific ways to avoid infringement

### 4. BUSINESS RECOMMENDATIONS (Actionable)
- **Licensing Strategy:** Specific companies and realistic cost estimates
- **Development Strategy:** Clear technical alternatives
- **Timeline:** Specific, actionable timeframes
- **Cost-Benefit:** Quantified analysis

### 5. FREEDOM TO OPERATE ASSESSMENT (Clear Decision)
- **Can You Proceed?** Yes/No/Maybe with clear conditions
- **What You Need to Do:** Specific, actionable steps
- **Timeline:** Realistic timeframes
- **Alternatives:** Clear pivot options

### 6. NEXT STEPS (Immediate Actions)
- **Week 1, Month 1, Month 3:** Specific, actionable tasks
- **Resource Requirements:** What's needed to execute

## FINAL QUALITY ASSURANCE

Before delivering your report, perform this final check:

**RELEVANCE VALIDATION:**
1. Does each included patent directly relate to "{patent_data['query']}"?
2. Are the blocking claims actually relevant to the search technology?
3. Would a patent attorney consider this analysis accurate?
4. Does this report provide actionable business intelligence?

**IF ANY PATENT FAILS THE RELEVANCE TEST, REMOVE IT FROM THE REPORT.**

## OUTPUT FORMAT
Generate a professional markdown report that follows the structure above. Ensure that:
- Only highly relevant patents are included
- The analysis is practical and actionable
- Business recommendations are specific and realistic
- The report provides clear, actionable intelligence

Remember: Quality over quantity. It's better to have 3 highly relevant patents than 10 marginally relevant ones.

Generate the report now:
"""
    
    return prompt

def generate_llm_report(prompt: str) -> str:
    """Generate professional report using Azure OpenAI (same as other services)"""
    
    try:
        # Get Azure OpenAI configuration (same as agent.py)
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")
        
        if not endpoint or not api_key or not deployment_name:
            logger.error("Missing Azure OpenAI configuration")
            return f"""# AZURE OPENAI CONFIGURATION REQUIRED

Please set the following environment variables:
- AZURE_OPENAI_ENDPOINT
- AZURE_OPENAI_API_KEY  
- AZURE_OPENAI_DEPLOYMENT_NAME
- AZURE_OPENAI_API_VERSION (optional, defaults to 2024-12-01-preview)

---
*Report generation failed due to missing configuration*"""
        
        # Prepare request (same pattern as agent.py)
        url = f"{endpoint.rstrip('/')}/openai/deployments/{deployment_name}/chat/completions?api-version={api_version}"
        
        headers = {
            "Content-Type": "application/json",
            "api-key": api_key
        }
        
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_completion_tokens": 4000,
            "temperature": 0.1
        }
        
        # Send request using httpx (same as agent.py)
        with httpx.Client(timeout=60) as client:
            logger.info(f"Generating professional patent report using Azure OpenAI: {deployment_name}")
            response = client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            
            # Extract content from response
            report_content = result['choices'][0]['message']['content']
            logger.info(f"Successfully generated patent report: {len(report_content)} characters")
            
            return report_content
            
    except Exception as e:
        logger.error(f"Failed to generate LLM report: {e}")
        return f"""# REPORT GENERATION FAILED

An error occurred while generating the professional patent report:

**Error:** {str(e)}

**What Happened:**
The system attempted to use Azure OpenAI to generate a professional patent attorney report but encountered an error.

**Possible Causes:**
1. Azure OpenAI service is unavailable
2. API rate limits exceeded
3. Network connectivity issues
4. Invalid API configuration

**Next Steps:**
1. Check your Azure OpenAI service status
2. Verify your API configuration
3. Try again in a few minutes
4. Contact support if the issue persists

---
*Report generated on {datetime.now().isoformat()}*
*Error occurred during LLM processing*"""

def extract_technical_terms_llm(user_query: str) -> str:
    """Use LLM to extract core technical terms for patent search"""
    
    prompt = f"""
    Extract ONLY the core technical terms from this patent search query.
    Ignore common words, search terms, and non-technical language.
    
    User Query: "{user_query}"
    
    Return ONLY the technical terms separated by spaces.
    
    Examples:
    - "search report for AI in 5G" → "AI 5G"
    - "find patents about blockchain smart contracts" → "blockchain smart contracts"
    - "look up prior art for machine learning algorithms" → "machine learning algorithms"
    - "search database for quantum computing patents" → "quantum computing"
    - "generate report on IoT security protocols" → "IoT security protocols"
    
    Rules:
    1. Remove search words: search, find, look, generate, report, patents, prior art
    2. Remove common words: for, in, on, about, the, a, an, and, or
    3. Keep technical terms: AI, 5G, blockchain, machine learning, quantum computing
    4. Keep compound terms together: "smart contracts", "machine learning"
    5. Return only the technical terms, nothing else
    
    Technical Terms:"""
    
    try:
        # Use your existing Azure OpenAI integration
        response = generate_llm_report(prompt)
        extracted_terms = response.strip()
        
        # Log the extraction for debugging
        logger.info(f"Query extraction: '{user_query}' → '{extracted_terms}'")
        
        return extracted_terms
        
    except Exception as e:
        logger.error(f"Failed to extract technical terms: {e}")
        # Fallback to simple filtering if LLM fails
        return extract_technical_terms_fallback(user_query)

def extract_technical_terms_fallback(user_query: str) -> str:
    """Fallback method for technical term extraction if LLM fails"""
    
    # Common words to ignore
    stop_words = {
        'search', 'report', 'find', 'look', 'generate', 'patents', 'prior', 'art',
        'for', 'in', 'on', 'about', 'the', 'a', 'an', 'and', 'or', 'but',
        'with', 'by', 'from', 'to', 'of', 'is', 'are', 'was', 'were',
        'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
        'will', 'would', 'could', 'should', 'may', 'might', 'can'
    }
    
    # Split query and filter out stop words
    words = user_query.lower().split()
    technical_terms = [word for word in words if word not in stop_words]
    
    extracted = ' '.join(technical_terms)
    logger.info(f"Fallback extraction: '{user_query}' → '{extracted}'")
    
    return extracted

# Convenience function for direct use
def search_patents(query: str, max_results: int = 5) -> str:
    """Simple function to search patents and return formatted results with claims"""
    
    # Extract core technical terms using LLM
    logger.info(f"Original user query: '{query}'")
    technical_query = extract_technical_terms_llm(query)
    logger.info(f"Extracted technical terms: '{technical_query}'")
    
    # Use extracted terms for the actual search
    result = search_prior_art_optimized(technical_query, max_results)
    return format_optimized_results(result)

def run_comprehensive_test_cases():
    """Run comprehensive test cases and store results for analysis"""
    import json
    import os
    from datetime import datetime
    
    # Test cases covering different technology domains
    test_cases = [
        {
            "name": "5G Dynamic Spectrum Sharing",
            "query": "5G dynamic spectrum sharing",
            "domain": "Telecommunications",
            "expected_terms": ["5G", "dynamic", "spectrum", "sharing"]
        },
        {
            "name": "AI in 5G",
            "query": "AI in 5G",
            "domain": "AI + Telecommunications", 
            "expected_terms": ["AI", "5G"]
        },
        {
            "name": "Machine Learning Algorithms",
            "query": "Machine Learning Algorithms",
            "domain": "Software/AI",
            "expected_terms": ["Machine", "Learning", "Algorithms"]
        },
        {
            "name": "Blockchain Smart Contracts",
            "query": "Blockchain Smart Contracts",
            "domain": "Cryptocurrency/Finance",
            "expected_terms": ["blockchain", "smart", "contracts"]
        },
        {
            "name": "Quantum Computing",
            "query": "Quantum Computing",
            "domain": "Advanced Technology",
            "expected_terms": ["Quantum", "Computing"]
        }
    ]
    
    # Results storage
    test_results = {
        "timestamp": datetime.now().isoformat(),
        "test_cases": []
    }
    
    print("🧪 RUNNING COMPREHENSIVE TEST CASES")
    print("=" * 80)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 TEST CASE {i}: {test_case['name']}")
        print(f"Query: '{test_case['query']}'")
        print(f"Domain: {test_case['domain']}")
        print(f"Expected Terms: {test_case['expected_terms']}")
        print("-" * 60)
        
        try:
            # Run the search
            result = search_patents(test_case['query'], 5)
            
            # Extract key metrics from the result
            result_analysis = {
                "test_case": test_case,
                "search_successful": True,
                "result_length": len(result),
                "result_preview": result[:500] + "..." if len(result) > 500 else result,
                "timestamp": datetime.now().isoformat()
            }
            
            # Store the result
            test_results["test_cases"].append(result_analysis)
            
            print(f"✅ Search completed successfully")
            print(f"📊 Result length: {len(result)} characters")
            print(f"📝 Preview: {result[:200]}...")
            
        except Exception as e:
            print(f"❌ Search failed: {e}")
            result_analysis = {
                "test_case": test_case,
                "search_successful": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            test_results["test_cases"].append(result_analysis)
    
    # Save results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"comprehensive_test_results_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(test_results, f, indent=2)
    
    print(f"\n💾 Test results saved to: {filename}")
    
    # Generate summary report
    successful_tests = sum(1 for tc in test_results["test_cases"] if tc["search_successful"])
    total_tests = len(test_results["test_cases"])
    
    print(f"\n📊 TEST SUMMARY")
    print("=" * 40)
    print(f"Total Tests: {total_tests}")
    print(f"Successful: {successful_tests}")
    print(f"Failed: {total_tests - successful_tests}")
    print(f"Success Rate: {(successful_tests/total_tests)*100:.1f}%")
    
    return test_results, filename


def run_telecom_test_cases():
    """Run 10 telecom-specific test cases with varying complexity levels"""
    import json
    import os
    from datetime import datetime

    # Telecom test cases with varying complexity (1-6+ terms)
    telecom_test_cases = [
        {
            "name": "5G Core Network",
            "query": "5G core network",
            "domain": "Telecommunications",
            "complexity": "2 terms",
            "expected_terms": ["5G", "core", "network"]
        },
        {
            "name": "Network Slicing",
            "query": "network slicing",
            "domain": "Telecommunications", 
            "complexity": "2 terms",
            "expected_terms": ["network", "slicing"]
        },
        {
            "name": "Massive MIMO Beamforming",
            "query": "massive MIMO beamforming",
            "domain": "Telecommunications",
            "complexity": "3 terms", 
            "expected_terms": ["massive", "MIMO", "beamforming"]
        },
        {
            "name": "Edge Computing 5G",
            "query": "edge computing 5G",
            "domain": "Telecommunications",
            "complexity": "3 terms",
            "expected_terms": ["edge", "computing", "5G"]
        },
        {
            "name": "Network Function Virtualization",
            "query": "network function virtualization",
            "domain": "Telecommunications",
            "complexity": "3 terms",
            "expected_terms": ["network", "function", "virtualization"]
        },
        {
            "name": "5G Dynamic Spectrum Sharing QoS",
            "query": "5G dynamic spectrum sharing QoS",
            "domain": "Telecommunications",
            "complexity": "5 terms",
            "expected_terms": ["5G", "dynamic", "spectrum", "sharing", "QoS"]
        },
        {
            "name": "Software Defined Networking SDN",
            "query": "software defined networking SDN",
            "domain": "Telecommunications",
            "complexity": "4 terms",
            "expected_terms": ["software", "defined", "networking", "SDN"]
        },
        {
            "name": "Network Security Authentication",
            "query": "network security authentication",
            "domain": "Telecommunications",
            "complexity": "3 terms",
            "expected_terms": ["network", "security", "authentication"]
        },
        {
            "name": "5G Ultra Reliable Low Latency",
            "query": "5G ultra reliable low latency communications",
            "domain": "Telecommunications",
            "complexity": "6 terms",
            "expected_terms": ["5G", "ultra", "reliable", "low", "latency", "communications"]
        },
        {
            "name": "Mobile Edge Computing MEC",
            "query": "mobile edge computing MEC 5G",
            "domain": "Telecommunications",
            "complexity": "5 terms",
            "expected_terms": ["mobile", "edge", "computing", "MEC", "5G"]
        }
    ]

    # Results storage
    test_results = {
        "timestamp": datetime.now().isoformat(),
        "domain": "Telecommunications",
        "test_cases": []
    }

    print("🧪 RUNNING 10 TELECOM TEST CASES")
    print("=" * 80)
    print("📡 DOMAIN: Telecommunications")
    print("🎯 COMPLEXITY: 1-6+ terms")
    print("=" * 80)

    for i, test_case in enumerate(telecom_test_cases, 1):
        print(f"\n🔍 TEST CASE {i}: {test_case['name']}")
        print(f"Query: '{test_case['query']}'")
        print(f"Complexity: {test_case['complexity']}")
        print(f"Expected Terms: {test_case['expected_terms']}")
        print("-" * 60)

        try:
            # Run the search
            result = search_patents(test_case['query'], 5)

            # Extract key metrics from the result
            result_analysis = {
                "test_case": test_case,
                "search_successful": True,
                "result_length": len(result),
                "result_preview": result[:500] + "..." if len(result) > 500 else result,
                "timestamp": datetime.now().isoformat()
            }

            # Store the result
            test_results["test_cases"].append(result_analysis)

            print(f"✅ Search completed successfully")
            print(f"📊 Result length: {len(result)} characters")
            print(f"📝 Preview: {result[:200]}...")

        except Exception as e:
            print(f"❌ Search failed: {e}")
            result_analysis = {
                "test_case": test_case,
                "search_successful": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            test_results["test_cases"].append(result_analysis)

    # Save results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"telecom_test_results_{timestamp}.json"

    with open(filename, 'w') as f:
        json.dump(test_results, f, indent=2)

    print(f"\n💾 Telecom test results saved to: {filename}")

    # Generate summary report
    successful_tests = sum(1 for tc in test_results["test_cases"] if tc["search_successful"])
    total_tests = len(test_results["test_cases"])

    print(f"\n📊 TELECOM TEST SUMMARY")
    print("=" * 50)
    print(f"Total Tests: {total_tests}")
    print(f"Successful: {successful_tests}")
    print(f"Failed: {total_tests - successful_tests}")
    print(f"Success Rate: {(successful_tests/total_tests)*100:.1f}%")

    # Complexity breakdown
    complexity_stats = {}
    for tc in test_results["test_cases"]:
        if tc["search_successful"]:
            complexity = tc["test_case"]["complexity"]
            if complexity not in complexity_stats:
                complexity_stats[complexity] = {"total": 0, "successful": 0}
            complexity_stats[complexity]["total"] += 1
            complexity_stats[complexity]["successful"] += 1
        else:
            complexity = tc["test_case"]["complexity"]
            if complexity not in complexity_stats:
                complexity_stats[complexity] = {"total": 0, "successful": 0}
            complexity_stats[complexity]["total"] += 1

    print(f"\n📈 COMPLEXITY BREAKDOWN:")
    for complexity, stats in complexity_stats.items():
        success_rate = (stats["successful"]/stats["total"])*100 if stats["total"] > 0 else 0
        print(f"  {complexity}: {stats['successful']}/{stats['total']} ({success_rate:.1f}%)")

    return test_results, filename
