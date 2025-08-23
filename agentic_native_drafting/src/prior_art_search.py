#!/usr/bin/env python3
"""
SIMPLIFIED Patent Search Module - Focused on Core Functionality
- Generate search queries
- Find relevant patents  
- Score relevance (title + abstract only)
- Generate comprehensive report with claims analysis and risk assessment
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
MAX_PROMPT_LENGTH = 50000
DEFAULT_TIMEOUT = 30.0

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PatentClaim:
    """Represents a patent claim with detailed information"""
    claim_number: str
    claim_text: str
    claim_type: str = "independent"
    dependency: Optional[str] = None
    is_exemplary: bool = False

@dataclass
class SimplePatentAnalysis:
    """SIMPLIFIED patent analysis - only essential data"""
    patent_id: str
    title: str
    abstract: str
    inventors: List[str]
    assignees: List[str]
    claims: List[PatentClaim]
    relevance_score: float
    publication_date: Optional[str] = None
    patent_year: Optional[str] = None

@dataclass
class SearchStrategy:
    """Patent search strategy configuration"""
    name: str
    description: str
    query: Dict[str, Any]
    expected_results: int = 10
    priority: int = 1

@dataclass
class SearchResult:
    """Search results container"""
    query: str
    total_found: int
    patents: List[SimplePatentAnalysis]
    search_strategies: List[SearchStrategy]
    timestamp: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PatentSearchConfig:
    """Configuration for patent search operations"""
    azure_endpoint: str = field(default_factory=lambda: os.getenv("AZURE_OPENAI_ENDPOINT", ""))
    azure_api_key: str = field(default_factory=lambda: os.getenv("AZURE_OPENAI_API_KEY", ""))
    azure_deployment: str = field(default_factory=lambda: os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-mini"))
    azure_api_version: str = field(default_factory=lambda: os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"))
    patents_view_api_key: str = field(default_factory=lambda: os.getenv("PATENTSVIEW_API_KEY", ""))
    min_request_interval: float = DEFAULT_MIN_REQUEST_INTERVAL  # Fix: add this attribute
    default_min_request_interval: float = DEFAULT_MIN_REQUEST_INTERVAL
    default_relevance_threshold: float = DEFAULT_RELEVANCE_THRESHOLD
    default_max_results: int = DEFAULT_MAX_RESULTS
    batch_size: int = DEFAULT_BATCH_SIZE
    timeout: float = DEFAULT_TIMEOUT

class EnhancedPatentsViewAPI:
    """Enhanced PatentsView API client with proper async support"""
    
    def __init__(self, config: PatentSearchConfig):
        self.config = config
        self.session = None
        self.last_request_time = 0
        self.patentsview_base_url = "https://search.patentsview.org/api/v1"
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = httpx.AsyncClient(timeout=self.config.timeout)
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.aclose()
    
    async def _rate_limit_async(self) -> None:
        """Async rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.config.min_request_interval:
            sleep_time = self.config.min_request_interval - time_since_last
            await asyncio.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    async def search_patents_async(self, strategy: SearchStrategy) -> List[Dict[str, Any]]:
        """Execute patent search strategy asynchronously"""
        await self._rate_limit_async()
        
        if not strategy.query:
            logger.warning(f"Empty query in strategy: {strategy.name}")
            return []
        
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
        if self.config.patents_view_api_key:
            headers["X-Api-Key"] = self.config.patents_view_api_key
        
        try:
            logger.info(f"Executing PatentsView API call for strategy: {strategy.name}")
            logger.debug(f"API payload for {strategy.name}: {payload}")
            response = await self.session.post(
                f"{self.patentsview_base_url}/patent/",
                json=payload,
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("error", False):
                    logger.error(f"PatentsView API error in strategy {strategy.name}: {data}")
                    return []
                
                patents = data.get("patents", [])
                total_count = data.get("total_patent_count", len(patents))
                logger.info(f"PatentsView API returned {len(patents)} patents for strategy '{strategy.name}' (total available: {total_count})")
                return self._process_patents(patents, strategy.name)
            else:
                logger.error(f"PatentsView API call for strategy {strategy.name} failed with status {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Strategy {strategy.name} failed: {e}")
            return []
    
    async def get_patent_claims_async(self, patent_id: str) -> List[PatentClaim]:
        """Retrieve patent claims asynchronously"""
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
        if self.config.patents_view_api_key:
            headers["X-Api-Key"] = self.config.patents_view_api_key
        
        try:
            logger.debug(f"Fetching claims async for patent: {patent_id}")
            
            response = await self.session.post(
                f"{self.patentsview_base_url}/g_claim/",
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
    
    def _process_patents(self, patents: List[Dict], strategy_name: str) -> List[Dict]:
        """Process raw patent data"""
        processed = []
        
        for patent in patents:
            try:
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
        """Parse claims data into PatentClaim objects"""
        claims = []
        
        for claim_info in claims_data:
            try:
                claim_text = claim_info.get("claim_text", "")
                if not claim_text:
                    continue
                
                claim_sequence = claim_info.get("claim_sequence", 0)
                claim_number = claim_info.get("claim_number", "")
                claim_dependent = claim_info.get("claim_dependent", "")
                
                if not claim_number:
                    claim_number = str(claim_sequence + 1)
                
                claim_type = "dependent" if claim_dependent else "independent"
                
                claim = PatentClaim(
                    claim_number=claim_number,
                    claim_text=claim_text,
                    claim_type=claim_type,
                    dependency=claim_dependent if claim_dependent else None,
                    is_exemplary=bool(claim_info.get("exemplary", ""))
                )
                
                claims.append(claim)
                
            except Exception as e:
                logger.warning(f"Error parsing claim: {e}")
                continue
                
        return claims

class SimplifiedQueryGenerator:
    """SIMPLIFIED query generator - just focus on getting good searches"""
    
    def __init__(self, config: PatentSearchConfig):
        self.config = config
    
    @observe(name="generate_search_strategies_simple")
    async def generate_search_strategies(self, user_query: str) -> List[SearchStrategy]:
        """Generate focused search strategies without over-analysis"""
        try:
            prompt = f"""Generate focused patent search strategies for: "{user_query}"

You are an expert patent analyst creating precise search strategies. Use PatentsView API syntax.

OPERATOR REFERENCE:
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

Return ONLY a JSON array with this structure:
[
    {{
        "name": "STRATEGY_NAME",
        "description": "detailed strategy explanation",
        "query": {{<PatentsView query structure>}},
        "expected_results": 15,
        "priority": 1,
        "technical_focus": "primary technical domain",
        "coverage_scope": "NARROW|MEDIUM|BROAD"
    }}
]

Generate exactly 4-5 diverse strategies covering different technical angles using proper PatentsView API syntax.

CRITICAL PRECISION REQUIREMENTS:
- NEVER use "_text_any" with broad terms like "5G", "LTE", "NR", "wireless", "cellular", "spectrum"
- ALWAYS use "_text_phrase" for common/broad technical terms
- ONLY use "_text_any" for very specific technical terms like "OFDMA", "beamforming", "MIMO"
- Combine precise phrases using "_and" for better specificity
- Target 10-50 results per strategy, not thousands"""

            response = await self._call_llm(prompt)
            
            # Clean and parse response
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
                    priority=strategy_data.get("priority", 1)
                )
                strategies.append(strategy)
            
            return strategies
            
        except Exception as e:
            logger.error(f"Query generation failed: {e}")
            raise
    
    @observe(name="simple_llm_call") 
    async def _call_llm(self, prompt: str) -> str:
        """Simple LLM call with proper Azure OpenAI setup"""
        try:
            base_url = self.config.azure_endpoint.rstrip('/')
            url = f"{base_url}/openai/deployments/{self.config.azure_deployment}/chat/completions?api-version={self.config.azure_api_version}"
            
            headers = {
                "Content-Type": "application/json",
                "api-key": self.config.azure_api_key
            }
            
            payload = {
                "messages": [
                    {"role": "system", "content": "You are a patent search expert. Generate precise JSON responses."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 2000,
                "temperature": 0.1
            }
            
            async with httpx.AsyncClient(timeout=self.config.timeout) as client:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                result = response.json()
                return result["choices"][0]["message"]["content"]
                
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise

class SimplifiedPatentAnalyzer:
    """SIMPLIFIED analyzer - just relevance scoring"""
    
    def __init__(self, config: PatentSearchConfig):
        self.config = config
    
    async def check_relevance(self, patent_data: Dict, search_query: str) -> float:
        """Simple relevance check using title + abstract only"""
        try:
            title = patent_data.get("patent_title", "")[:200]
            abstract = patent_data.get("patent_abstract", "")[:400] 
            
            prompt = f"""Analyze patent relevance to search query with comprehensive evaluation. Return ONLY a JSON response.

SEARCH QUERY: {search_query}
PATENT TITLE: {title}
PATENT ABSTRACT: {abstract}

Conduct thorough relevance analysis considering:

TECHNICAL RELEVANCE FACTORS:
1. Direct Technology Match: Does the patent directly address the search technology?
2. Core Innovation Alignment: How well do the patent's innovations align with the search focus?
3. Technical Approach Similarity: Are the underlying technical approaches comparable?
4. Implementation Scope: Does the patent cover the same technical scope as the search?
5. Standards Compatibility: Does the patent relate to relevant technical standards?

SEMANTIC ANALYSIS:
- Analyze technical terminology overlap
- Consider conceptual relationships between patent and search
- Evaluate innovation novelty in the context of the search
- Assess practical applicability to the search domain

RELEVANCE SCORING CRITERIA:
- 0.0-0.2: IRRELEVANT - No meaningful connection to search query
- 0.3-0.4: SLIGHT - Tangential relation, some shared terminology but different focus
- 0.5-0.6: MODERATE - Related technology area with some overlapping concepts  
- 0.7-0.8: HIGH - Strong technical alignment with clear relevance to search
- 0.9-1.0: EXCELLENT - Direct match with high innovation overlap

Return ONLY this JSON structure:
{{
    "relevance_score": <float 0.0-1.0>,
    "reasoning": "<detailed explanation of relevance assessment considering technical alignment, innovation overlap, and practical applicability>",
    "key_alignment_factors": ["<factor1>", "<factor2>", "<factor3>"],
    "technical_overlap_level": "<NONE|LOW|MEDIUM|HIGH>",
    "innovation_relevance": "<NOT_RELEVANT|TANGENTIAL|RELATED|HIGHLY_RELEVANT>"
}}

Provide comprehensive analysis focusing on technical depth and practical relevance to the search query."""
            
            response = await self._call_llm(prompt)
            
            # Parse JSON response
            try:
                # Clean response and handle non-JSON responses
                cleaned_response = response.strip()
                if cleaned_response.startswith("```json"):
                    cleaned_response = cleaned_response[7:]
                if cleaned_response.endswith("```"):
                    cleaned_response = cleaned_response[:-3]
                cleaned_response = cleaned_response.strip()
                
                result = json.loads(cleaned_response)
                score = float(result.get("relevance_score", 0.5))
                return min(max(score, 0.0), 1.0)
            except json.JSONDecodeError:
                # Fallback: try to extract just the number
                match = re.search(r'[0-9]*\.?[0-9]+', response)
                if match:
                    score = float(match.group())
                    return min(max(score, 0.0), 1.0)
                else:
                    return 0.5
                
        except Exception as e:
            logger.error(f"Relevance check failed: {e}")
            return 0.0
    
    async def analyze_patent_simple(self, patent_data: Dict, search_query: str) -> SimplePatentAnalysis:
        """Create simplified patent analysis"""
        try:
            # Extract basic info
            patent_id = patent_data.get("patent_id", "")
            title = patent_data.get("patent_title", "")
            abstract = patent_data.get("patent_abstract", "")
            
            # Extract inventors and assignees
            inventors = self._extract_inventors(patent_data.get("inventors", []))
            assignees = self._extract_assignees(patent_data.get("assignees", []))
            
            # Get claims
            async with EnhancedPatentsViewAPI(self.config) as api:
                claims = await api.get_patent_claims_async(patent_id)
            
            # Get relevance score
            relevance_score = await self.check_relevance(patent_data, search_query)
            
            return SimplePatentAnalysis(
                patent_id=patent_id,
                title=title,
                abstract=abstract,
                inventors=inventors,
                assignees=assignees,
                claims=claims,
                relevance_score=relevance_score,
                publication_date=patent_data.get("patent_date"),
                patent_year=patent_data.get("patent_year")
            )
            
        except Exception as e:
            logger.error(f"Error analyzing patent {patent_data.get('patent_id', 'unknown')}: {e}")
            raise
    
    def _extract_inventors(self, inventors_data: List[Dict]) -> List[str]:
        """Extract inventor names"""
        inventors = []
        for inv in inventors_data:
            try:
                first = inv.get("inventor_name_first", "")
                last = inv.get("inventor_name_last", "")
                full_name = f"{first} {last}".strip()
                if full_name:
                    inventors.append(full_name)
            except Exception:
                continue
        return inventors
    
    def _extract_assignees(self, assignees_data: List[Dict]) -> List[str]:
        """Extract assignee organizations"""
        assignees = []
        for ass in assignees_data:
            try:
                org = ass.get("assignee_organization", "")
                if org:
                    assignees.append(org)
            except Exception:
                continue
        return assignees

    async def _call_llm(self, prompt: str) -> str:
        """Simple LLM call"""
        try:
            base_url = self.config.azure_endpoint.rstrip('/')
            url = f"{base_url}/openai/deployments/{self.config.azure_deployment}/chat/completions?api-version={self.config.azure_api_version}"
            
            headers = {
                "Content-Type": "application/json", 
                "api-key": self.config.azure_api_key
            }
            
            payload = {
                "messages": [
                    {"role": "system", "content": "You are an expert patent analyst specializing in technical relevance assessment."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 1500,  # Increased for detailed analysis
                "temperature": 0.1
            }
            
            async with httpx.AsyncClient(timeout=self.config.timeout) as client:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                result = response.json()
                return result["choices"][0]["message"]["content"]
                
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise

class SimplifiedReportGenerator:
    """SIMPLIFIED report generator - focus on claims analysis and risk"""
    
    def __init__(self, config: PatentSearchConfig):
        self.config = config
    
    @observe(name="generate_simple_report")
    async def generate_report(self, search_result: SearchResult) -> str:
        """Generate focused report with claims analysis and risk assessment"""
        try:
            # Limit to top patents to avoid huge reports
            top_patents = search_result.patents[:10]
            
            if not top_patents:
                # Return simple report when no patents found
                return f"""
# Patent Analysis Report

## SEARCH QUERY: {search_result.query}

## EXECUTIVE SUMMARY
No relevant patents found matching the search criteria. This could indicate:
- The technology is very new/emerging
- Different terminology might be used in patents
- The search query may need refinement

## RECOMMENDATIONS
1. Try broader search terms
2. Consider related technical concepts
3. Search with different technical terminology
4. Check for pending applications (not covered in this search)

---
SEARCH METADATA:
- Query: {search_result.query}
- Patents found: 0
- Search strategies: {len(search_result.search_strategies)}
- Generated: {search_result.timestamp}
"""
            
            # Prepare claims summaries for ALL patents at once
            claims_summaries = []
            for patent in top_patents:
                # Get key claims text (first 3 independent claims)
                key_claims = []
                for claim in patent.claims[:5]:
                    if len(key_claims) < 3 and "dependent" not in claim.claim_type.lower():
                        key_claims.append(f"Claim {claim.claim_number}: {claim.claim_text[:200]}")
                
                claims_text = " | ".join(key_claims) if key_claims else "No key claims found"
                claims_summaries.append({
                    "patent_id": patent.patent_id,
                    "title": patent.title[:100],
                    "assignees": ", ".join(patent.assignees[:2]),
                    "relevance": patent.relevance_score,
                    "key_claims": claims_text
                })
            
            # ONE comprehensive LLM call for the entire report
            prompt = f"""Generate a comprehensive patent analysis report with mandatory structured format.

SEARCH QUERY: "{search_result.query}"
TOTAL PATENTS ANALYZED: {len(top_patents)}

PATENT INVENTORY - USE EXACT IDs AND TITLES:
{json.dumps(claims_summaries, indent=2)}

🚨🚨🚨 MANDATORY REPORT STRUCTURE - DO NOT DEVIATE 🚨🚨🚨

Generate a comprehensive report with EXACTLY these 9 sections in this order:

## 1. Executive Summary
[Comprehensive overview: key findings, total patents analyzed, primary risk level, main technological themes, overall competitive landscape assessment, and critical insights summary]

## 2. Search Methodology & Criteria
### 2.1 Search Strategy Overview
[Detailed explanation of search approach, query formulation rationale, and coverage strategy]

### 2.2 Query Construction & Technical Focus
[Technical rationale for search terms, field targeting strategy, and precision vs recall balance]

### 2.3 Relevance Threshold & Filtering Criteria  
[Explanation of relevance scoring methodology, filtering criteria applied, and quality assurance measures]

## 3. Individual Patent Deep Analysis
[FOR EACH PATENT: Provide detailed analysis including:]
- Patent ID and full title
- Assignee and publication details
- Relevance score with detailed justification
- Technical innovation summary from claims
- Specific claim elements relevant to search
- Risk factors and blocking potential
- Design-around feasibility assessment

## 4. Technology Analysis
[Deep technical analysis: innovation patterns, technological maturity assessment, standards alignment, implementation complexity patterns, and emerging technology trends across the patent portfolio]

## 5. Patent Risk Assessment Summary
[Comprehensive risk evaluation: overall blocking potential across portfolio, design-around difficulty analysis, commercial impact assessment, enforcement likelihood, and strategic risk recommendations]

## 6. Competitive Intelligence
[Competitive landscape analysis: key assignee companies, market positioning assessment, patent strategy analysis, competitive threats evaluation, and industry leadership indicators]

## 7. Claims Analysis Summary
[Detailed claims examination: core innovation patterns, claim scope analysis, technical differentiation factors, overlap identification, and potential infringement vectors]

## 8. Strategic Recommendations
[Actionable recommendations: IP strategy guidance, freedom to operate recommendations, design-around strategies, licensing considerations, and competitive positioning advice]

## 9. Conclusion and Next Steps
[Summary of critical findings, recommended follow-up actions, priority areas for additional research, and strategic implementation timeline]

🚨🚨🚨 MANDATORY FORMATTING REQUIREMENTS 🚨🚨🚨
- Use EXACT section headers as shown above (including numbering 1-9)
- Include ALL 9 sections - do not skip any
- Use exact patent IDs and titles from Patent Inventory only
- Follow the detailed subsection structure for Section 2 (2.1, 2.2, 2.3)
- Make each section substantial with detailed analysis (minimum 2-3 paragraphs per section)
- Do NOT combine sections or use different numbering
- Do NOT use simplified headings
- Each section must provide actionable insights and detailed technical analysis

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

ANALYSIS DEPTH REQUIREMENTS:
- Provide specific technical details from patent claims
- Include quantitative assessments where possible
- Reference specific claim numbers and technical elements
- Offer practical, actionable insights for each section
- Maintain professional patent analysis standards throughout

START YOUR RESPONSE WITH: "# Prior Art Search Report"

Focus on practical insights, specific claim analysis, and actionable intelligence for IP strategy decisions."""

            report = await self._call_llm(prompt)
            
            # Add metadata footer
            avg_relevance = sum(p.relevance_score for p in top_patents)/len(top_patents) if top_patents else 0.0
            footer = f"""

---
SEARCH METADATA:
- Query: {search_result.query}
- Patents analyzed: {len(top_patents)}
- Search strategies: {len(search_result.search_strategies)}
- Generated: {search_result.timestamp}
- Average relevance: {avg_relevance:.2f}
"""
            
            return report + footer
            
        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            raise
    
    @observe(name="simple_report_llm_call")
    async def _call_llm(self, prompt: str) -> str:
        """LLM call for report generation"""
        try:
            base_url = self.config.azure_endpoint.rstrip('/')
            url = f"{base_url}/openai/deployments/{self.config.azure_deployment}/chat/completions?api-version={self.config.azure_api_version}"
            
            headers = {
                "Content-Type": "application/json",
                "api-key": self.config.azure_api_key
            }
            
            payload = {
                "messages": [
                    {"role": "system", "content": "You are an expert patent analyst and IP strategist. Generate comprehensive, professional patent analysis reports with detailed technical analysis and actionable insights."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 6000,  # Increased for comprehensive reports
                "temperature": 0.15  # Slightly higher for more natural comprehensive analysis
            }
            
            async with httpx.AsyncClient(timeout=self.config.timeout) as client:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                result = response.json()
                return result["choices"][0]["message"]["content"]
                
        except httpx.TimeoutException as e:
            logger.error(f"Report LLM call timed out: {e}")
            raise Exception(f"LLM call timed out after {self.config.timeout}s")
        except httpx.HTTPStatusError as e:
            logger.error(f"Report LLM call HTTP error: {e.response.status_code} - {e.response.text}")
            raise Exception(f"HTTP {e.response.status_code}: {e.response.text}")
        except Exception as e:
            logger.error(f"Report LLM call failed: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            raise Exception(f"LLM call failed: {type(e).__name__}: {str(e)}")

class SimplifiedPatentSearchEngine:
    """SIMPLIFIED main search engine - streamlined workflow"""
    
    def __init__(self, config: Optional[PatentSearchConfig] = None):
        self.config = config or PatentSearchConfig()
        self.query_generator = SimplifiedQueryGenerator(self.config)
        self.analyzer = SimplifiedPatentAnalyzer(self.config)
        self.report_generator = SimplifiedReportGenerator(self.config)
    
    @observe(name="simplified_patent_search")
    async def search(self, query: str, max_results: int = None, relevance_threshold: float = None) -> SearchResult:
        """Simplified patent search workflow"""
        max_results = max_results or self.config.default_max_results
        relevance_threshold = relevance_threshold or self.config.default_relevance_threshold
        
        logger.info(f"Starting simplified patent search for: '{query}'")
        
        try:
            # 1. Generate search strategies
            strategies = await self.query_generator.generate_search_strategies(query)
            logger.info(f"Generated {len(strategies)} search strategies for query: '{query}'")
            
            # 2. Execute searches sequentially to avoid rate limiting
            all_patents = []
            total_api_patents = 0
            async with EnhancedPatentsViewAPI(self.config) as api:
                for i, strategy in enumerate(strategies, 1):
                    try:
                        logger.info(f"Executing strategy {i}/{len(strategies)}: {strategy.name}")
                        result = await api.search_patents_async(strategy)
                        strategy_count = len(result)
                        total_api_patents += strategy_count
                        logger.info(f"Strategy '{strategy.name}' retrieved {strategy_count} patents from PatentsView API")
                        all_patents.extend(result)
                    except Exception as e:
                        logger.error(f"Strategy {strategy.name} failed: {e}")
                        continue
            
            logger.info(f"Total patents retrieved from all PatentsView API calls: {total_api_patents}")
            
            # 3. Remove duplicates
            unique_patents = {}
            for patent in all_patents:
                patent_id = patent.get("patent_id")
                if patent_id and patent_id not in unique_patents:
                    unique_patents[patent_id] = patent
            
            patent_list = list(unique_patents.values())
            duplicates_removed = total_api_patents - len(patent_list)
            logger.info(f"After deduplication: {len(patent_list)} unique patents (removed {duplicates_removed} duplicates)")
            
            # 4. Simple parallel relevance filtering
            relevant_patents = []
            batch_size = self.config.batch_size
            
            for i in range(0, len(patent_list), batch_size):
                batch = patent_list[i:i + batch_size]
                tasks = [self.analyzer.check_relevance(patent, query) for patent in batch]
                scores = await asyncio.gather(*tasks)
                
                for patent, score in zip(batch, scores):
                    if score >= relevance_threshold:
                        relevant_patents.append((patent, score))
            
            logger.info(f"Found {len(relevant_patents)} relevant patents above threshold {relevance_threshold}")
            
            # 5. Sort and limit
            relevant_patents.sort(key=lambda x: x[1], reverse=True)
            top_relevant = relevant_patents[:max_results]
            
            # 6. Full analysis with claims for top patents only
            analyzed_patents = []
            for patent_data, score in top_relevant:
                try:
                    analysis = await self.analyzer.analyze_patent_simple(patent_data, query)
                    analyzed_patents.append(analysis)
                except Exception as e:
                    logger.error(f"Failed to analyze patent {patent_data.get('patent_id')}: {e}")
            
            logger.info(f"Completed analysis for {len(analyzed_patents)} patents")
            
            # 7. Create search result
            search_result = SearchResult(
                query=query,
                total_found=len(analyzed_patents),
                patents=analyzed_patents,
                search_strategies=strategies,
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
            logger.error(f"Simplified search failed: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise
    
    async def generate_report(self, search_result: SearchResult) -> str:
        """Generate simplified comprehensive report"""
        try:
            logger.info("Generating simplified comprehensive report...")
            return await self.report_generator.generate_report(search_result)
        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            raise

# Keep the original classes as backup but rename for clarity
PatentSearchEngine = SimplifiedPatentSearchEngine

# For backward compatibility
if __name__ == "__main__":
    async def test_simplified_search():
        engine = SimplifiedPatentSearchEngine()
        result = await engine.search("dynamic spectrum sharing", max_results=5)
        report = await engine.generate_report(result)
        print(f"Found {result.total_found} patents")
        print(f"Report length: {len(report)} characters")
    
    asyncio.run(test_simplified_search())
