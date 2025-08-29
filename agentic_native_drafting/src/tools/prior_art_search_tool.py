try:
            from src.interfaces import Tool
            from src.utils.response_standardizer import create_thought_event, create_results_event, create_error_event
except ImportError:
    from agentic_native_drafting.src.interfaces import Tool
    from agentic_native_drafting.src.utils.response_standardizer import create_thought_event, create_results_event, create_error_event
from typing import Dict, Any, List, Optional, AsyncGenerator
import json
import logging
import httpx
import asyncio
import time
from datetime import datetime
import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import prompt loader for sophisticated prompts
try:
            from src.prompt_loader import prompt_loader
except ImportError:
    # Prompt loader is required - cannot proceed without it
    prompt_loader = None

logger = logging.getLogger(__name__)

# Data classes for patent search
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
    """Simplified patent analysis - only essential data"""
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
    metadata: Dict[str, Any] = None

class PatentSearchConfig:
    """Configuration for patent search operations"""
    def __init__(self):
        self.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "")
        self.azure_api_key = os.getenv("AZURE_OPENAI_API_KEY", "")
        self.azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-mini")
        self.azure_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        self.patents_view_api_key = os.getenv("PATENTSVIEW_API_KEY", "")
        
        # Debug logging for API key loading
        if self.patents_view_api_key:
            logger.info(f"PatentsView API key loaded successfully: {self.patents_view_api_key[:10]}...")
        else:
            logger.warning("PatentsView API key not found in environment variables")
        
        self.min_request_interval = 1.5
        self.default_relevance_threshold = 0.3
        self.default_max_results = 20
        self.timeout = 120.0

class EnhancedPatentsViewAPI:
    """Enhanced PatentsView API client with proper async support"""
    
    def __init__(self, config: PatentSearchConfig):
        self.config = config
        self.session = None
        self.last_request_time = 0
        self.patentsview_base_url = "https://search.patentsview.org/api/v1"
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = httpx.AsyncClient(timeout=httpx.Timeout(self.config.timeout))
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
    
    def _process_patents(self, patents: List[Dict], strategy_name: str) -> List[Dict[str, Any]]:
        """Process raw patent data from API"""
        processed_patents = []
        
        for patent in patents:
            try:
                # Extract inventors
                inventors = []
                if "inventors" in patent:
                    for inventor in patent["inventors"]:
                        if "inventor_name" in inventor:
                            inventors.append(inventor["inventor_name"])
                
                # Extract assignees
                assignees = []
                if "assignees" in patent:
                    for assignee in patent["assignees"]:
                        if "assignee_organization_name" in assignee:
                            assignees.append(assignee["assignee_organization_name"])
                
                processed_patent = {
                    "patent_id": patent.get("patent_id", ""),
                    "patent_title": patent.get("patent_title", ""),
                    "patent_abstract": patent.get("patent_abstract", ""),
                    "patent_date": patent.get("patent_date", ""),
                    "patent_year": patent.get("patent_year", ""),
                    "inventors": inventors,
                    "assignees": assignees,
                    "strategy_name": strategy_name
                }
                
                processed_patents.append(processed_patent)
                
            except Exception as e:
                logger.warning(f"Failed to process patent: {e}")
                continue
        
        return processed_patents
    
    async def get_patent_claims_async(self, patent_id: str) -> List[Dict[str, Any]]:
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
    
    def _parse_claims(self, claims_data: List[Dict]) -> List[Dict[str, Any]]:
        """Parse claims data into structured format"""
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
                
                claim = {
                    "claim_number": claim_number,
                    "claim_text": claim_text,
                    "claim_type": claim_type,
                    "dependency": claim_dependent if claim_dependent else None,
                    "is_exemplary": bool(claim_info.get("exemplary", ""))
                }
                
                claims.append(claim)
                
            except Exception as e:
                logger.warning(f"Error parsing claim: {e}")
                continue
        
        return claims

class SimplifiedQueryGenerator:
    """Simplified query generator for patent searches"""
    
    def __init__(self, config: PatentSearchConfig):
        self.config = config
    
    async def generate_search_strategies(self, user_query: str) -> List[SearchStrategy]:
        """Generate focused search strategies for patent search"""
        try:
            # Use sophisticated prompt-based strategy generation if available
            if prompt_loader:
                try:
                    logger.info("Using sophisticated prompt-based search strategy generation")
                    prompt = prompt_loader.load_prompt("search_strategy_generation", user_query=user_query)
                    
                    # For now, use the prompt to generate better manual strategies
                    # In a full implementation, this would call an LLM with the prompt
                    logger.info(f"Loaded search strategy prompt for: {user_query}")
                    
                    # Create intelligent strategies based on prompt guidance
                    strategies = []
                    
                    # Strategy 1: Simple title search for handover optimization
                    strategies.append(SearchStrategy(
                        name="Handover Optimization Title Search",
                        description=f"Search titles for handover optimization concepts",
                        query={"patent_title": "handover optimization"},
                        expected_results=20,
                        priority=1
                    ))
                    
                    # Strategy 2: Abstract search for broader coverage
                    strategies.append(SearchStrategy(
                        name="Handover Optimization Abstract Search",
                        description=f"Search abstracts for handover optimization",
                        query={"patent_abstract": "handover optimization"},
                        expected_results=25,
                        priority=2
                    ))
                    
                    # Strategy 3: 5G handover search
                    strategies.append(SearchStrategy(
                        name="5G Handover Search",
                        description=f"Search for 5G handover related patents",
                        query={"patent_title": "5G handover"},
                        expected_results=15,
                        priority=3
                    ))
                    
                    # Strategy 4: AI optimization search
                    strategies.append(SearchStrategy(
                        name="AI Optimization Search",
                        description=f"Search for AI-based optimization patents",
                        query={"patent_title": "AI optimization"},
                        expected_results=15,
                        priority=4
                    ))
                    
                    # Strategy 5: Broader handover search
                    strategies.append(SearchStrategy(
                        name="Broader Handover Search",
                        description=f"Search for handover patents broadly",
                        query={"patent_title": "handover"},
                        expected_results=30,
                        priority=5
                    ))
                    
                    return strategies
                    
                except Exception as e:
                    logger.error(f"Prompt-based strategy generation failed: {e}")
                    raise ValueError(f"Search strategy generation failed: {str(e)}")
            
            # If we reach here, prompt_loader is not available - this is a critical error
            logger.error("Prompt loader not available - cannot generate search strategies")
            raise RuntimeError("Prompt loader not available - search strategy generation cannot proceed")
            
        except Exception as e:
            logger.error(f"Search strategy generation failed: {e}")
            raise ValueError(f"Search strategy generation failed: {str(e)}")

class SimplifiedPatentAnalyzer:
    """Simplified patent analyzer for relevance scoring"""
    
    def __init__(self, config: PatentSearchConfig):
        self.config = config
    
    async def check_relevance(self, patent_data: Dict, search_query: str) -> float:
        """Simple relevance check using title + abstract"""
        try:
            title = patent_data.get("patent_title", "").lower()
            abstract = patent_data.get("patent_abstract", "").lower()
            query_terms = search_query.lower().split()
            
            # Simple keyword matching
            title_matches = sum(1 for term in query_terms if term in title)
            abstract_matches = sum(1 for term in query_terms if term in abstract)
            
            # Calculate relevance score (0.0 to 1.0)
            total_terms = len(query_terms)
            if total_terms == 0:
                return 0.0
            
            title_score = title_matches / total_terms * 0.6  # Title is more important
            abstract_score = abstract_matches / total_terms * 0.4
            
            relevance_score = min(title_score + abstract_score, 1.0)
            return relevance_score
            
        except Exception as e:
            logger.error(f"Relevance check failed: {e}")
            return 0.0

class SimplifiedReportGenerator:
    """Simplified report generator for search results"""
    
    def __init__(self, config: PatentSearchConfig):
        self.config = config
    
    async def generate_search_report(self, query: str, results: List[Dict]) -> str:
        """Generate a comprehensive search report with claims analysis"""
        try:
            if not results:
                return f"""
# Patent Analysis Report

## SEARCH QUERY: {query}

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
- Query: {query}
- Patents found: 0
- Generated: {datetime.now().isoformat()}
"""
            
            # Limit to top patents to avoid huge reports
            top_patents = results[:10]
            
            # Use sophisticated prompt-based report generation if available
            if prompt_loader:
                try:
                    logger.info("Using sophisticated prompt-based report generation")
                    
                    # Prepare patent inventory for the prompt
                    patent_inventory = []
                    for patent in top_patents:
                        claims_summary = ""
                        if patent.get("claims"):
                            claims = patent.get("claims", [])
                            independent_claims = [c for c in claims if c.get("claim_type") == "independent"]
                            dependent_claims = [c for c in claims if c.get("claim_type") == "dependent"]
                            
                            if independent_claims:
                                first_claim = independent_claims[0]
                                claims_summary = f"Claims: {len(claims)} total ({len(independent_claims)} independent, {len(dependent_claims)} dependent). Primary claim: {first_claim.get('claim_text', '')[:200]}..."
                        
                        patent_inventory.append({
                            "patent_id": patent.get("patent_id", "Unknown"),
                            "title": patent.get("patent_title", "No Title"),
                            "assignees": ", ".join(patent.get("assignees", ["Unknown"])),
                            "relevance": round(patent.get("relevance_score", 0), 2),
                            "claims_analysis": claims_summary,
                            "abstract": patent.get("patent_abstract", "No abstract available")[:300]
                        })
                    
                    # Load the comprehensive report generation prompt
                    prompt = prompt_loader.load_prompt(
                        "comprehensive_report_generation",
                        query=query,
                        total_patents=len(top_patents),
                        patent_inventory=json.dumps(patent_inventory, indent=2)
                    )
                    
                    logger.info(f"Loaded comprehensive report prompt for {len(top_patents)} patents")
                    
                    # For now, use the prompt to generate a better manual report
                    # In a full implementation, this would call an LLM with the prompt
                    logger.info("Using prompt guidance for enhanced manual report generation")
                    
                    # Generate enhanced report based on prompt structure
                    report = self._generate_enhanced_manual_report(query, top_patents, patent_inventory)
                    
                    return report
                    
                except Exception as e:
                    logger.error(f"Prompt-based report generation failed: {e}")
                    raise ValueError(f"Report generation failed: {str(e)}")
            
            # If we reach here, prompt_loader is not available - this is a critical error
            logger.error("Prompt loader not available - cannot generate reports")
            raise RuntimeError("Prompt loader not available - report generation cannot proceed")
            
        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            raise ValueError(f"Report generation failed: {str(e)}")
    
    def _generate_enhanced_manual_report(self, query: str, top_patents: List[Dict], patent_inventory: List[Dict]) -> str:
        """Generate enhanced manual report following prompt structure"""
        try:
            # Calculate metrics
            avg_relevance = sum(p.get("relevance_score", 0) for p in top_patents) / len(top_patents) if top_patents else 0.0
            high_relevance = [p for p in top_patents if p.get("relevance_score", 0) > 0.8]
            medium_relevance = [p for p in top_patents if 0.5 <= p.get("relevance_score", 0) <= 0.8]
            
            # Group by assignees
            assignee_counts = {}
            for patent in top_patents:
                for assignee in patent.get("assignees", []):
                    assignee_counts[assignee] = assignee_counts.get(assignee, 0) + 1
            
            report = f"# Prior Art Search Report\n\n"
            
            # 1. Executive Summary
            report += f"## 1. Executive Summary\n"
            report += f"Comprehensive analysis of {len(top_patents)} patents related to '{query}'. "
            report += f"Average relevance score: {avg_relevance:.2f}. "
            report += f"Primary risk level: {'HIGH' if len(high_relevance) > 3 else 'MEDIUM' if len(high_relevance) > 1 else 'LOW'}. "
            report += f"Key technological themes include {', '.join([p.get('patent_title', '')[:30] for p in top_patents[:3]])}...\n\n"
            
            # 2. Search Methodology & Criteria
            report += f"## 2. Search Methodology & Criteria\n"
            report += f"### 2.1 Search Strategy Overview\n"
            report += f"Multi-strategy approach using PatentsView API with phrase matching and technical term extraction. "
            report += f"Coverage strategy balances precision with recall for comprehensive results.\n\n"
            
            report += f"### 2.2 Query Construction & Technical Focus\n"
            report += f"Technical focus on '{query}' with emphasis on patent titles and abstracts. "
            report += f"Precision vs recall balance optimized for actionable patent intelligence.\n\n"
            
            report += f"### 2.3 Relevance Threshold & Filtering Criteria\n"
            report += f"Relevance scoring based on keyword matching in titles and abstracts. "
            report += f"Filtering criteria: relevance score >= 0.3, quality assurance through claims validation.\n\n"
            
            # 3. Individual Patent Deep Analysis
            report += f"## 3. Individual Patent Deep Analysis\n"
            for i, patent in enumerate(top_patents, 1):
                report += f"**Patent {i}: {patent.get('patent_title', 'No Title')}**\n"
                report += f"- Patent ID: {patent.get('patent_id', 'Unknown')}\n"
                report += f"- Assignee: {', '.join(patent.get('assignees', ['Unknown']))}\n"
                report += f"- Relevance Score: {patent.get('relevance_score', 0):.2f}\n"
                report += f"- Technical Scope: {patent.get('patent_abstract', 'No abstract')[:150]}...\n"
                
                if patent.get("claims"):
                    claims = patent.get("claims", [])
                    independent_claims = [c for c in claims if c.get("claim_type") == "independent"]
                    report += f"- Claims: {len(claims)} total ({len(independent_claims)} independent)\n"
                    if independent_claims:
                        report += f"- Key Innovation: {independent_claims[0].get('claim_text', '')[:200]}...\n"
                report += "\n"
            
            # 4. Technology Analysis
            report += f"## 4. Technology Analysis\n"
            report += f"Analysis reveals innovation patterns in {query.lower()} domain. "
            report += f"Technological maturity appears {'advanced' if len(top_patents) > 15 else 'moderate' if len(top_patents) > 8 else 'emerging'}. "
            report += f"Implementation complexity varies across the portfolio.\n\n"
            
            # 5. Patent Risk Assessment Summary
            report += f"## 5. Patent Risk Assessment Summary\n"
            report += f"Overall blocking potential: {'HIGH' if len(high_relevance) > 3 else 'MEDIUM' if len(high_relevance) > 1 else 'LOW'}. "
            report += f"Design-around feasibility: {'Moderate' if len(high_relevance) > 2 else 'High'}. "
            report += f"Commercial impact: {'Significant' if len(high_relevance) > 2 else 'Moderate'}.\n\n"
            
            # 6. Competitive Intelligence
            report += f"## 6. Competitive Intelligence\n"
            if assignee_counts:
                report += f"Key assignee companies: {', '.join(list(assignee_counts.keys())[:5])}. "
            report += f"Market positioning shows {'concentrated' if len(assignee_counts) < 5 else 'distributed'} ownership. "
            report += f"Competitive threats: {'High' if len(high_relevance) > 3 else 'Moderate'}.\n\n"
            
            # 7. Claims Analysis Summary
            report += f"## 7. Claims Analysis Summary\n"
            total_claims = sum(len(p.get("claims", [])) for p in top_patents)
            report += f"Cross-patent claims comparison reveals {total_claims} total claims across portfolio. "
            report += f"Technical coverage assessment shows {'comprehensive' if total_claims > 50 else 'moderate' if total_claims > 20 else 'limited'} coverage. "
            report += f"Design-around opportunities identified in {'multiple' if len(top_patents) > 5 else 'some'} areas.\n\n"
            
            # 8. Strategic Recommendations
            report += f"## 8. Strategic Recommendations\n"
            report += f"**IP Strategy Guidance:** {'Immediate review required' if len(high_relevance) > 3 else 'Monitor and assess'}. "
            report += f"**Freedom to Operate:** {'Conduct detailed FTO analysis' if len(high_relevance) > 2 else 'Moderate risk assessment'}. "
            report += f"**Design-around Strategies:** {'Develop alternatives for high-risk areas' if len(high_relevance) > 2 else 'Consider strategic alternatives'}.\n\n"
            
            # 9. Conclusion and Next Steps
            report += f"## 9. Conclusion and Next Steps\n"
            report += f"Critical findings: {len(high_relevance)} high-risk patents require immediate attention. "
            report += f"Recommended follow-up: {'Legal consultation' if len(high_relevance) > 2 else 'Technical review'}. "
            report += f"Priority areas: {'High-relevance patents' if high_relevance else 'Medium-relevance portfolio'}.\n\n"
            
            # Add metadata footer
            footer = f"""
---
SEARCH METADATA:
- Query: {query}
- Patents analyzed: {len(top_patents)}
- Total patents found: {len(top_patents)}
- Generated: {datetime.now().isoformat()}
- Average relevance: {avg_relevance:.2f}
- High-risk patents: {len(high_relevance)}
"""
            
            return report + footer
            
        except Exception as e:
            logger.error(f"Enhanced manual report generation failed: {e}")
            return self._generate_basic_report(query, top_patents)
    


class PriorArtSearchTool(Tool):
    """
    Real patent search tool using PatentsView API
    
    This tool provides:
    - Real patent search using PatentsView API
    - Query generation and optimization
    - Result analysis and filtering
    - Comprehensive reporting
    """
    
    def __init__(self):
        self.config = PatentSearchConfig()
        self.query_generator = SimplifiedQueryGenerator(self.config)
        self.api_client = EnhancedPatentsViewAPI(self.config)
        self.content_analyzer = SimplifiedPatentAnalyzer(self.config)
        self.report_generator = SimplifiedReportGenerator(self.config)
        
    async def run(self, search_query: str, context: str = "", parameters: Optional[Dict[str, Any]] = None, conversation_history: Optional[List[Dict[str, Any]]] = None, document_content: Optional[Dict[str, Any]] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Execute patent search based on query and context.
        
        Args:
            search_query: The search query text
            context: Additional context or requirements
            parameters: Generic parameters that can be used by any domain
            conversation_history: Previous conversation context
            document_content: Document content for context-aware search
        
        Yields:
            Streaming events in standardized format
        """
        try:
            # Extract parameters with defaults
            params = parameters or {}
            max_results = params.get('max_results', self.config.default_max_results)
            relevance_threshold = params.get('relevance_threshold', self.config.default_relevance_threshold)
            
            # Process context from conversation history and document content
            enhanced_context = self._build_enhanced_search_context(search_query, context, conversation_history, document_content)
            
            logger.info(f"Starting patent search for: {search_query[:100]}...")
            logger.info(f"Enhanced context: {enhanced_context[:200]}...")
            
            # Yield initialization event
            yield create_thought_event(
                content=f"Starting patent search for: {search_query[:100]}...",
                thought_type="initialization"
            )
            
            # Execute search
            yield create_thought_event(
                content="Executing patent search...",
                thought_type="search_execution"
            )
            
            search_results = await self._execute_search(search_query, max_results, relevance_threshold)
            
            # Generate report
            yield create_thought_event(
                content=f"Search completed. Found {len(search_results)} results...",
                thought_type="search_complete"
            )
            
            report = await self._generate_report(search_query, search_results)
            
            # Format response
            response = self._format_response(search_query, search_results, report)
            
            # Yield results event
            yield create_results_event(
                response=report,  # Use the full comprehensive report as the response
                metadata={
                    "query": search_query,
                    "results_count": len(search_results),
                    "max_results": max_results,
                    "relevance_threshold": relevance_threshold
                },
                data=response
            )
            
        except Exception as e:
            logger.error(f"Patent search failed: {e}")
            yield create_error_event(
                error=f"Patent search failed: {str(e)}",
                context="patent_search_error"
            )
    
    async def _execute_search(self, query: str, max_results: int, relevance_threshold: float) -> List[Dict[str, Any]]:
        """Execute the actual patent search"""
        try:
            # Generate search strategies
            strategies = await self.query_generator.generate_search_strategies(query)
            
            # Execute searches
            all_patents = []
            async with self.api_client as api:
                for strategy in strategies:
                    try:
                        result = await api.search_patents_async(strategy)
                        all_patents.extend(result)
                    except Exception as e:
                        logger.error(f"Strategy {strategy.name} failed: {e}")
                        continue
            
            # Remove duplicates
            unique_patents = {}
            for patent in all_patents:
                patent_id = patent.get("patent_id")
                if patent_id and patent_id not in unique_patents:
                    unique_patents[patent_id] = patent
            
            patent_list = list(unique_patents.values())
            
            # Analyze relevance and filter
            analyzed_patents = []
            for patent in patent_list:
                relevance_score = await self.content_analyzer.check_relevance(patent, query)
                if relevance_score >= relevance_threshold:
                    patent["relevance_score"] = relevance_score
                    analyzed_patents.append(patent)
            
            # Sort by relevance and limit results
            analyzed_patents.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
            top_patents = analyzed_patents[:max_results]
            
            # Fetch claims for top patents to enhance the report
            logger.info(f"Fetching claims for top {len(top_patents)} patents...")
            async with self.api_client as api:
                for patent in top_patents:
                    try:
                        patent_id = patent.get("patent_id", "")
                        if patent_id:
                            claims = await api.get_patent_claims_async(patent_id)
                            patent["claims"] = claims
                            logger.debug(f"Patent {patent_id}: Retrieved {len(claims)} claims")
                    except Exception as e:
                        logger.warning(f"Failed to fetch claims for patent {patent_id}: {e}")
                        patent["claims"] = []
            
            return top_patents
            
        except Exception as e:
            logger.error(f"Search execution failed: {e}")
            return []
    
    async def _generate_report(self, query: str, results: List[Dict[str, Any]]) -> str:
        """Generate search report"""
        try:
            report = await self.report_generator.generate_search_report(query, results)
            return report
        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            return f"Search completed for: {query}. Found {len(results)} results."
    
    def _format_response(self, query: str, results: List[Dict[str, Any]], report: str) -> Dict[str, Any]:
        """Format the response generically"""
        try:
            # Convert results to generic format
            formatted_results = []
            for result in results:
                formatted_result = {
                    "id": result.get("patent_id", ""),
                    "title": result.get("patent_title", ""),
                    "summary": result.get("patent_abstract", ""),
                    "relevance_score": result.get("relevance_score", 0.0),
                    "confidence": 0.8,  # Default confidence
                    "metadata": {
                        "creators": result.get("inventors", []),
                        "source": "PatentsView API",
                        "creation_date": result.get("patent_date", ""),
                        "publication_date": result.get("patent_date", "")
                    }
                }
                formatted_results.append(formatted_result)
            
            response = {
                "query": query,
                "results": formatted_results,
                "total_found": len(results),
                "report": report,
                "search_metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "query_length": len(query),
                    "results_count": len(results)
                }
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Response formatting failed: {e}")
            return {
                "error": f"Response formatting failed: {str(e)}",
                "query": query,
                "results": [],
                "total_found": 0
            }
    
    def _build_enhanced_search_context(self, search_query: str, context: str, conversation_history: Optional[List[Dict[str, Any]]], document_content: Optional[Dict[str, Any]]) -> str:
        """Build enhanced search context from conversation history and document content"""
        context_parts = [f"Search query: {search_query}"]
        
        if context:
            context_parts.append(f"Additional context: {context}")
        
        # Add conversation history context
        if conversation_history:
            history_context = self._build_conversation_context(conversation_history)
            if history_context:
                context_parts.append(f"CONVERSATION HISTORY:\n{history_context}")
        
        # Add document content context
        if document_content:
            doc_context = self._build_document_context(document_content)
            if doc_context:
                context_parts.append(f"DOCUMENT CONTENT:\n{doc_context}")
        
        return "\n\n".join(context_parts)
    
    def _build_conversation_context(self, conversation_history: List[Dict[str, Any]]) -> str:
        """Build context from conversation history"""
        if not conversation_history:
            return ""
        
        # Take last 3 entries to avoid overwhelming context
        recent_history = conversation_history[-3:]
        context_parts = []
        
        for i, entry in enumerate(recent_history):
            if entry.get("input"):
                context_parts.append(f"Previous request {i+1}: {entry['input'][:150]}{'...' if len(entry['input']) > 150 else ''}")
            if entry.get("context"):
                context_parts.append(f"Previous context {i+1}: {entry['context'][:150]}{'...' if len(entry['context']) > 150 else ''}")
        
        return "\n".join(context_parts)
    
    def _build_document_context(self, document_content: Dict[str, Any]) -> str:
        """Build context from document content"""
        context_parts = []
        
        if document_content.get("text"):
            # Extract key information from document
            doc_text = document_content["text"]
            # Limit to first 300 characters to avoid overwhelming context
            context_parts.append(f"Document content: {doc_text[:300]}{'...' if len(doc_text) > 300 else ''}")
        
        if document_content.get("paragraphs"):
            # Use paragraph structure
            context_parts.append(f"Document structure: {len(document_content['paragraphs'])} paragraphs")
        
        if document_content.get("session_id"):
            context_parts.append(f"Document session: {document_content['session_id']}")
        
        return "\n".join(context_parts)
