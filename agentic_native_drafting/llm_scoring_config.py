#!/usr/bin/env python3
"""
Configuration for Pure LLM-Based Patent Relevance Scoring System
Centralized control over scoring parameters and thresholds
NO FALLBACK MECHANISMS - Pure LLM scoring only
"""

# LLM Scoring Configuration
LLM_SCORING_CONFIG = {
    # Relevance Thresholds
    "DEFAULT_RELEVANCE_THRESHOLD": 0.3,      # Default minimum relevance score
    "HIGH_QUALITY_THRESHOLD": 0.7,           # Threshold for high-quality patents
    "EXCELLENT_THRESHOLD": 0.9,              # Threshold for excellent matches
    
    # Batch Processing
    "BATCH_SIZE": 5,                         # Number of patents to process at once
    "MAX_CONCURRENT_LLM_CALLS": 3,           # Maximum concurrent LLM API calls
    
    # LLM Parameters
    "TEMPERATURE": 0.1,                      # Low temperature for consistent scoring
    "MAX_TOKENS": 300,                       # Maximum tokens for scoring response
    "TIMEOUT_SECONDS": 30,                   # Timeout for LLM API calls
    "MAX_RETRIES": 3,                        # Maximum retry attempts for LLM calls
    "RETRY_DELAY_SECONDS": 2,                # Initial delay between retries
    
    # Pure LLM Configuration
    "PURE_LLM_SCORING": True,               # Only use LLM-based scoring
    "EXCLUDE_ON_FAILURE": True,             # Exclude patents when LLM fails
    
    # Logging and Monitoring
    "LOG_SCORING_DETAILS": True,             # Log detailed scoring information
    "LOG_CONFIDENCE_SCORES": True,           # Log confidence scores
    "LOG_REASONING": True,                   # Log LLM reasoning for scores
    
    # Domain-Specific Thresholds
    "DOMAIN_THRESHOLDS": {
        "5G_TELECOM": 0.4,                   # 5G and telecommunications
        "AI_ML": 0.5,                        # Artificial intelligence and machine learning
        "BLOCKCHAIN": 0.4,                   # Blockchain and cryptocurrency
        "IOT": 0.4,                          # Internet of Things
        "SOFTWARE": 0.3,                     # General software and computing
        "HARDWARE": 0.3,                     # Hardware and electronics
        "DEFAULT": 0.3                       # Default for unknown domains
    },
    
    # Scoring Categories
    "SCORING_CATEGORIES": {
        "IRRELEVANT": (0.0, 0.2),           # Completely unrelated
        "SLIGHTLY_RELEVANT": (0.3, 0.4),    # Minimal relevance
        "MODERATELY_RELEVANT": (0.5, 0.6),  # Some connection
        "HIGHLY_RELEVANT": (0.7, 0.8),      # Strong connection
        "EXCELLENT_MATCH": (0.9, 1.0)       # Directly addresses query
    }
}

# LLM Prompt Templates
LLM_PROMPTS = {
    "RELEVANCE_SCORING": """
You are a patent attorney specializing in prior art analysis. Your task is to evaluate the relevance of a patent to a specific search query.

SEARCH QUERY: {search_query}

PATENT INFORMATION:
Title: {patent_title}
Abstract: {patent_abstract}
Year: {patent_year}

Please analyze the relevance and return ONLY a JSON response with this exact structure:
{{
    "relevance_score": <float between 0.0 and 1.0>,
    "confidence": <float between 0.0 and 1.0>,
    "reasoning": "<brief explanation of why this score was given>",
    "key_matches": ["<list of key terms/concepts that match>"],
    "relevance_level": "<LOW/MEDIUM/HIGH/EXCELLENT>"
}}

SCORING CRITERIA:
- 0.0-0.2: Irrelevant or completely unrelated
- 0.3-0.4: Slightly related, minimal relevance
- 0.5-0.6: Moderately relevant, some connection
- 0.7-0.8: Highly relevant, strong connection
- 0.9-1.0: Excellent match, directly addresses the query

Consider:
1. Direct term matches in title/abstract
2. Conceptual relevance to the search domain
3. Technical alignment with the query intent
4. Patent recency (newer patents may be more relevant)
5. Specificity of the technology described

Return ONLY the JSON response, no other text.
""",

    "BATCH_SCORING": """
You are a patent attorney evaluating multiple patents for relevance to a search query.

SEARCH QUERY: {search_query}

PATENTS TO EVALUATE:
{patent_list}

For each patent, provide a relevance score and brief reasoning. Return ONLY a JSON array with this structure:
[
    {{
        "patent_id": "<patent_id>",
        "relevance_score": <float 0.0-1.0>,
        "confidence": <float 0.0-1.0>,
        "reasoning": "<brief explanation>",
        "relevance_level": "<LOW/MEDIUM/HIGH/EXCELLENT>"
    }}
]

Score consistently using the same criteria for all patents.
"""
}

# Performance Optimization Settings
PERFORMANCE_CONFIG = {
    "ENABLE_CACHING": True,                  # Cache LLM responses for similar queries
    "CACHE_TTL_HOURS": 24,                  # Cache time-to-live in hours
    "ENABLE_PARALLEL_PROCESSING": False,     # Process patents in parallel (use with caution)
    "RATE_LIMIT_DELAY": 1.0,                # Delay between LLM API calls (seconds)
    
    # Memory Management
    "MAX_CACHED_SCORES": 1000,              # Maximum number of cached scores
    "CLEANUP_INTERVAL_HOURS": 6,            # Cache cleanup interval
}

# Error Handling Configuration
ERROR_HANDLING = {
    "MAX_RETRIES": 3,                        # Maximum retry attempts for LLM calls
    "RETRY_DELAY_SECONDS": 2,                # Delay between retries
    "EXCLUDE_ON_ERROR": True,                # Exclude patents when LLM fails
    "LOG_ERROR_DETAILS": True,               # Log detailed error information
}

def get_domain_threshold(domain: str) -> float:
    """Get relevance threshold for a specific domain"""
    return LLM_SCORING_CONFIG["DOMAIN_THRESHOLDS"].get(domain, LLM_SCORING_CONFIG["DOMAIN_THRESHOLDS"]["DEFAULT"])

def get_scoring_category(score: float) -> str:
    """Get scoring category for a given score"""
    for category, (min_score, max_score) in LLM_SCORING_CONFIG["SCORING_CATEGORIES"].items():
        if min_score <= score <= max_score:
            return category
    return "UNKNOWN"

def is_high_quality(score: float) -> bool:
    """Check if a score indicates high quality"""
    return score >= LLM_SCORING_CONFIG["HIGH_QUALITY_THRESHOLD"]

def is_excellent_match(score: float) -> bool:
    """Check if a score indicates an excellent match"""
    return score >= LLM_SCORING_CONFIG["EXCELLENT_THRESHOLD"]
