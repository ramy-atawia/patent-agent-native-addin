"""
Optimized Prior Art Search Module with Claims
Uses proven working fields and correct claims endpoint
"""

import os
import json
import logging
import httpx
import time
from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime

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
        """Search patents using only proven working fields"""
        self._rate_limit()
        
        if not search_terms or not search_terms.strip():
            logger.warning("Empty search terms provided")
            return []
        
        # Use only the proven working fields
        payload = {
            "q": {
                "_text_any": {
                    "patent_title": search_terms
                }
            },
            "f": [
                "patent_id",
                "patent_title", 
                "patent_abstract",
                "inventors",
                "assignees"
            ],
            "o": {
                "size": max_results
            }
        }
        
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["X-Api-Key"] = self.api_key
        
        try:
            logger.info(f"Searching patents: '{search_terms}' (max_results={max_results})")
            
            response = self.session.post(
                f"{self.base_url}/patent/",
                json=payload,
                headers=headers
            )
            
            response.raise_for_status()
            data = response.json()
            
            if data.get("error", False):
                logger.error(f"API error: {data}")
                return []
            
            patents = data.get("patents", [])
            total_hits = data.get("total_hits", len(patents))
            
            logger.info(f"Search successful: {len(patents)} patents returned, {total_hits} total matches")
            return patents
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
    
    def get_patent_claims(self, patent_id: str) -> List[str]:
        """Get claims using the correct g_claim endpoint"""
        self._rate_limit()
        
        if not patent_id:
            return []
        
        # Use the correct claims endpoint from documentation
        payload = {
            "q": {"patent_id": patent_id},
            "f": ["patent_id", "claim_sequence", "claim_text", "claim_number"],
            "o": {
                "size": 50,  # Get up to 50 claims
                "pad_patent_id": False
            },
            "s": [{"patent_id": "asc"}, {"claim_sequence": "asc"}]
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
                
                for claim in claims:
                    claim_text = claim.get("claim_text", "")
                    claim_sequence = claim.get("claim_sequence", 0)
                    claim_number = claim.get("claim_number", "")
                    
                    if claim_text:
                        # Format claim with sequence and number
                        if claim_number:
                            formatted_claim = f"{claim_number}. {claim_text}"
                        else:
                            formatted_claim = f"{claim_sequence + 1}. {claim_text}"
                        claim_texts.append(formatted_claim)
                
                # Sort by claim sequence
                claim_texts.sort(key=lambda x: int(x.split('.')[0]) if x.split('.')[0].isdigit() else 0)
                
                logger.info(f"Retrieved {len(claim_texts)} claims for patent {patent_id}")
                return claim_texts
            else:
                logger.info(f"Claims endpoint returned {response.status_code} for patent {patent_id}")
                return []
                
        except Exception as e:
            logger.info(f"Claims endpoint unavailable for patent {patent_id}: {e}")
            return []

def search_prior_art_optimized(search_query: str, max_results: int = 5) -> OptimizedSearchResult:
    """Optimized prior art search with claims"""
    
    api_client = OptimizedPatentsViewAPI()
    
    # Search for patents
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
            
            # Get claims for this patent
            claims = api_client.get_patent_claims(patent_id)
            
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
            
            # Simple relevance scoring
            relevance_score = max(0.1, 1.0 - (i * 0.2))
            
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
    """Format results as optimized markdown with claims"""
    if not result.patents:
        return f"# Prior Art Search Results: {result.query}\n\nNo relevant patents found."
    
    lines = [
        f"# Prior Art Search Results: {result.query}",
        f"",
        f"**Total found:** {result.total_found}",
        f"**Search time:** {result.timestamp}",
        f"",
        f"## Summary",
        f""
    ]
    
    for i, patent in enumerate(result.patents, 1):
        lines.extend([
            f"### {i}. {patent.title}",
            f"",
            f"**Patent ID:** {patent.patent_id}",
            f"**Relevance Score:** {patent.relevance_score:.2f}",
            f"",
            f"**Abstract:** {patent.abstract}",
            f"",
            f"**Inventors:** {', '.join(patent.inventors) if patent.inventors else 'Not available'}",
            f"",
            f"**Assignees:** {', '.join(patent.assignees) if patent.assignees else 'Not available'}",
            f"",
            f"**Claims:** {len(patent.claims)} found",
            f""
        ])
        
        # Add claims if available
        if patent.claims:
            lines.append("**Claim Details:**")
            for claim in patent.claims[:5]:  # Show first 5 claims
                lines.append(f"- {claim[:150]}...")
            if len(patent.claims) > 5:
                lines.append(f"- ... and {len(patent.claims) - 5} more claims")
        else:
            lines.append("**Claims:** Not available for this patent")
        
        lines.append("")
    
    return "\n".join(lines)

# Convenience function for direct use
def search_patents(query: str, max_results: int = 5) -> str:
    """Simple function to search patents and return formatted results with claims"""
    result = search_prior_art_optimized(query, max_results)
    return format_optimized_results(result)
