#!/usr/bin/env python3
"""
Generic models for the new backend.
No dependencies on legacy files.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime

@dataclass
class SearchConfig:
    """Generic configuration for search operations"""
    max_results: int = 10
    min_relevance_score: float = 0.3
    search_timeout: int = 30
    max_retries: int = 3

@dataclass
class SearchResult:
    """Generic result from search operations"""
    item_id: str
    title: str
    summary: str
    creators: List[str] = field(default_factory=list)
    source: str = ""
    creation_date: str = ""
    publication_date: str = ""
    relevance_score: float = 0.0
    confidence: float = 0.0
    reasoning: str = ""

@dataclass
class SearchQuery:
    """Generic search query structure"""
    query_text: str
    domain: str = ""
    keywords: List[str] = field(default_factory=list)
    filters: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SearchReport:
    """Generic search report structure"""
    query: SearchQuery
    results: List[SearchResult]
    total_found: int
    search_timestamp: datetime = field(default_factory=datetime.now)
    summary: str = ""
    recommendations: List[str] = field(default_factory=list)
