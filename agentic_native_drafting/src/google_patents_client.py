#!/usr/bin/env python3
"""
Google Patents Client for Claims Retrieval
Uses Google Patents web pages to extract claims for specific patent numbers
"""

import httpx
import re
from typing import List
import logging
import time

# Set up logging
logger = logging.getLogger(__name__)

class GooglePatentsClient:
    """Client for retrieving patent claims from Google Patents"""
    
    def __init__(self, timeout: float = 30.0):
        self.base_url = "https://patents.google.com/patent"
        self.session = httpx.Client(timeout=timeout)
        self.last_request_time = 0
        self.min_request_interval = 2.0  # Be respectful to Google's servers
    
    def _rate_limit(self):
        """Rate limiting to be respectful to Google's servers"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            logger.info(f"Rate limiting: sleeping for {sleep_time:.2f}s")
            time.sleep(sleep_time)
        self.last_request_time = time.time()
    
    def get_patent_claims(self, patent_number: str) -> List[str]:
        """
        Retrieve claims for a specific patent number from Google Patents
        
        Args:
            patent_number: Patent number (e.g., '10499252', 'US10499252', 'US10499252B1')
        
        Returns:
            List of claim strings, or empty list if not found
        """
        self._rate_limit()
        
        if not patent_number:
            logger.warning("Empty patent number provided")
            return []
        
        # Clean patent number
        clean_patent = self._clean_patent_number(patent_number)
        
        try:
            # Construct Google Patents URL
            url = f"{self.base_url}/{clean_patent}"
            logger.info(f"Fetching claims from Google Patents: {url}")
            
            # Make request
            response = self.session.get(url)
            
            if response.status_code == 200:
                html_content = response.text
                claims = self._extract_claims_from_html(html_content)
                
                if claims:
                    logger.info(f"Successfully extracted {len(claims)} claims from Google Patents")
                    return claims
                else:
                    logger.info("No claims found in Google Patents HTML")
                    return []
            else:
                logger.warning(f"Google Patents returned status {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Failed to retrieve claims from Google Patents: {e}")
            return []
    
    def _clean_patent_number(self, patent_number: str) -> str:
        """Clean and format patent number for Google Patents URL"""
        # Remove common prefixes and clean up
        clean = patent_number.strip().upper()
        
        # If it's already a full US patent number, use as is
        if clean.startswith('US'):
            return clean
        
        # Otherwise, assume it's a US patent and add US prefix
        return f"US{clean}"
    
    def _extract_claims_from_html(self, html_content: str) -> List[str]:
        """Extract claims from Google Patents HTML content"""
        claims = []
        
        try:
            # Look for claims section in the HTML
            # Google Patents typically has claims in a structured format
            
            # Method 1: Look for claims in structured data
            claims_pattern = r'<span[^>]*class="[^"]*claim[^"]*"[^>]*>(.*?)</span>'
            claim_matches = re.findall(claims_pattern, html_content, re.IGNORECASE | re.DOTALL)
            
            if claim_matches:
                for match in claim_matches:
                    # Clean up HTML tags and extract text
                    clean_claim = self._clean_html_text(match)
                    if clean_claim and len(clean_claim.strip()) > 10:  # Minimum claim length
                        claims.append(clean_claim.strip())
            
            # Method 2: Look for claims in JSON-LD structured data
            if not claims:
                json_ld_pattern = r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>'
                json_matches = re.findall(json_ld_pattern, html_content, re.IGNORECASE | re.DOTALL)
                
                for json_match in json_matches:
                    try:
                        import json
                        data = json.loads(json_match)
                        if isinstance(data, dict) and 'claims' in data:
                            claims_data = data['claims']
                            if isinstance(claims_data, list):
                                for claim in claims_data:
                                    if isinstance(claim, dict) and 'text' in claim:
                                        clean_claim = self._clean_html_text(claim['text'])
                                        if clean_claim and len(clean_claim.strip()) > 10:
                                            claims.append(clean_claim.strip())
                    except (json.JSONDecodeError, KeyError):
                        continue
            
            # Method 3: Look for claims in specific HTML sections
            if not claims:
                # Look for claims in various HTML structures
                claim_section_patterns = [
                    r'<div[^>]*class="[^"]*claims[^"]*"[^>]*>(.*?)</div>',
                    r'<section[^>]*class="[^"]*claims[^"]*"[^>]*>(.*?)</section>',
                    r'<h[1-6][^>]*>.*?[Cc]laims?.*?</h[1-6]>(.*?)(?=<h[1-6]|$)',
                ]
                
                for pattern in claim_section_patterns:
                    matches = re.findall(pattern, html_content, re.IGNORECASE | re.DOTALL)
                    for match in matches:
                        # Extract individual claims from the section
                        individual_claims = self._extract_individual_claims(match)
                        claims.extend(individual_claims)
            
            # Remove duplicates and sort
            unique_claims = list(dict.fromkeys(claims))  # Preserve order while removing duplicates
            return unique_claims
            
        except Exception as e:
            logger.error(f"Error extracting claims from HTML: {e}")
            return []
    
    def _extract_individual_claims(self, claims_section: str) -> List[str]:
        """Extract individual claims from a claims section"""
        individual_claims = []
        
        try:
            # Look for numbered claims (e.g., "1. A method...", "2. The method of claim 1...")
            claim_patterns = [
                r'<p[^>]*>(\d+\.\s*[^<]+)</p>',  # <p>1. A method...</p>
                r'<div[^>]*>(\d+\.\s*[^<]+)</div>',  # <div>1. A method...</div>
                r'(\d+\.\s*[^<\n]+)',  # 1. A method... (general pattern)
            ]
            
            for pattern in claim_patterns:
                matches = re.findall(pattern, claims_section, re.IGNORECASE | re.DOTALL)
                for match in matches:
                    clean_claim = self._clean_html_text(match)
                    if clean_claim and len(clean_claim.strip()) > 10:
                        individual_claims.append(clean_claim.strip())
            
            return individual_claims
            
        except Exception as e:
            logger.error(f"Error extracting individual claims: {e}")
            return []
    
    def _clean_html_text(self, html_text: str) -> str:
        """Clean HTML text by removing tags and normalizing whitespace"""
        # Remove HTML tags
        clean_text = re.sub(r'<[^>]+>', '', html_text)
        
        # Decode HTML entities
        import html
        clean_text = html.unescape(clean_text)
        
        # Normalize whitespace
        clean_text = re.sub(r'\s+', ' ', clean_text)
        
        return clean_text.strip()
    
    def close(self):
        """Close the HTTP session"""
        if self.session:
            self.session.close()

def get_google_patents_claims(patent_number: str) -> List[str]:
    """
    Convenience function to get claims from Google Patents
    
    Args:
        patent_number: Patent number (e.g., '10499252', 'US10499252')
        
    Returns:
        List of claim strings
    """
    client = GooglePatentsClient()
    try:
        return client.get_patent_claims(patent_number)
    finally:
        client.close()

if __name__ == "__main__":
    # Test the Google Patents client
    import logging
    logging.basicConfig(level=logging.INFO)
    
    client = GooglePatentsClient()
    
    # Test with the patent we found earlier
    test_patent = "10499252"
    print(f"Testing Google Patents claims retrieval for patent {test_patent}")
    
    claims = client.get_patent_claims(test_patent)
    
    if claims:
        print(f"✅ Found {len(claims)} claims:")
        for i, claim in enumerate(claims[:3], 1):  # Show first 3
            print(f"{i}. {claim[:100]}...")
        if len(claims) > 3:
            print(f"... and {len(claims) - 3} more claims")
    else:
        print("❌ No claims found")
    
    client.close()
