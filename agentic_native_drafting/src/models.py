from typing import List, Literal, Optional, Any
from pydantic import BaseModel


class ReviewComment(BaseModel):
    comment: str
    severity: Literal["minor", "major", "critical"]


class PatentClaim(BaseModel):
    """Individual patent claim with structured data"""
    claim_number: int
    claim_text: str
    claim_type: Literal["independent", "dependent"]
    dependency: Optional[str] = None  # For dependent claims


class ClaimDraftingResult(BaseModel):
    """Result of claim drafting with structured data"""
    claims: List[PatentClaim]
    summary: str
    num_claims: int


class ClaimReviewResult(BaseModel):
    """Result of claim review with structured data"""
    review_comments: List[ReviewComment]
    overall_assessment: str
    claims_reviewed: List[str]  # Store the actual claims that were reviewed


class PatentDraft(BaseModel):
    claims: List[str]
    review_comments: List[ReviewComment] = []
    # Add structured data support
    structured_claims: Optional[List[PatentClaim]] = None
    drafting_result: Optional[ClaimDraftingResult] = None
    review_result: Optional[ClaimReviewResult] = None


class ConversationMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str
    timestamp: Optional[str] = None


class ConversationContext(BaseModel):
    conversation_id: str
    summary: str = ""
    messages: List[ConversationMessage] = []
    user_intent: Optional[str] = None  # "patent", "conversation", "ambiguous"
    pending_request: Optional[str] = None  # What the user wants but hasn't provided details for yet
    generated_claims: List[str] = []  # Store generated patent claims for easy access
    # Add structured data support
    structured_claims: Optional[List[PatentClaim]] = None
    last_drafting_result: Optional[ClaimDraftingResult] = None
    last_review_result: Optional[ClaimReviewResult] = None


class AgentResponse(BaseModel):
    """Response from the agent with action planning and reasoning"""
    conversation_response: str
    reasoning: str
    should_draft_claims: bool = False
    claims: Optional[List[str]] = None
    review_comments: Optional[List[ReviewComment]] = None
    # Add structured data support
    structured_claims: Optional[List[PatentClaim]] = None
    drafting_result: Optional[ClaimDraftingResult] = None
    review_result: Optional[ClaimReviewResult] = None
    prior_art_result: Optional[Any] = None