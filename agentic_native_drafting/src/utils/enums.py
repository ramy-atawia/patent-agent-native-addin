#!/usr/bin/env python3
"""
Generic enums for the new backend.
No dependencies on legacy files.
"""

from enum import Enum

class IntentType(Enum):
    """Generic user intent types that can work with any domain"""
    CONTENT_DRAFTING = "content_drafting"
    CONTENT_REVIEW = "content_review"
    GUIDANCE = "guidance"
    ANALYSIS = "analysis"
    QUERY = "query"
    GENERAL_CONVERSATION = "general_conversation"
    SEARCH = "search"
    ASSESSMENT = "assessment"
