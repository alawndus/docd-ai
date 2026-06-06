"""Domain models for Doc D AI Engine.

Represents core entities across voice, trust graph, quests, and agents.
"""

from datetime import datetime
from enum import Enum
from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field


class UserRole(str, Enum):
    """User roles in the system."""
    VETERAN = "veteran"
    SMALL_BUSINESS = "small_business"
    COMMUNITY_VERIFIER = "community_verifier"
    AGENT_ADMIN = "agent_admin"
    SERVICE_PROVIDER = "service_provider"


class User(BaseModel):
    """A person in the system (veteran, business owner, verifier, etc.)."""
    id: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="Full name")
    phone_number: Optional[str] = Field(None, description="Phone for voice interaction")
    email: Optional[str] = Field(None, description="Email contact")
    roles: List[UserRole] = Field(default_factory=list, description="User roles")
    trust_score: float = Field(default=0.0, description="Aggregate trust score (0-100)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom attributes")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        use_enum_values = True


class CredentialStatus(str, Enum):
    """Status of a verifiable credential."""
    PENDING = "pending"
    VERIFIED = "verified"
    REVOKED = "revoked"
    EXPIRED = "expired"


class Credential(BaseModel):
    """A verifiable credential proving completion of a quest or achievement."""
    id: str = Field(..., description="Unique credential ID")
    user_id: str = Field(..., description="User who earned this credential")
    quest_id: str = Field(..., description="Quest that was completed")
    status: CredentialStatus = Field(default=CredentialStatus.PENDING)
    issued_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = Field(None, description="When credential expires")
    verified_by: List[str] = Field(default_factory=list, description="User IDs who verified")
    on_chain_hash: Optional[str] = Field(None, description="Hash/reference for blockchain")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom data")

    class Config:
        use_enum_values = True


class TrustNode(BaseModel):
    """A node in the trust graph (represents a user's position)."""
    user_id: str = Field(..., description="User this node represents")
    trust_level: float = Field(default=0.0, description="Initial trust (0-100)")
    credentials: List[str] = Field(default_factory=list, description="Credential IDs held")
    verified_quests: List[str] = Field(default_factory=list, description="Completed quest IDs")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom attributes")


class TrustEdge(BaseModel):
    """An edge in the trust graph (trust relationship between users)."""
    source_user_id: str = Field(..., description="User who trusts")
    target_user_id: str = Field(..., description="User who is trusted")
    trust_weight: float = Field(default=1.0, description="Strength of trust (0-1)")
    reason: Optional[str] = Field(None, description="Why they trust (credential ID, verification, etc.)")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class QuestStep(BaseModel):
    """A single step in a quest."""
    id: str = Field(..., description="Unique step ID")
    question: str = Field(..., description="Question or prompt for the user")
    answer_type: str = Field(default="text", description="Type: text, choice, number, etc.")
    choices: Optional[List[str]] = Field(None, description="Options if answer_type=choice")
    required: bool = Field(default=True, description="Is this step required?")
    next_steps: Dict[str, str] = Field(default_factory=dict, description="Map answers to next step IDs")


class Quest(BaseModel):
    """A gamified compliance path (regulation converted to interactive quest)."""
    id: str = Field(..., description="Unique quest ID")
    title: str = Field(..., description="Quest title (e.g., 'VA Benefits Quest')")
    description: str = Field(..., description="What this quest helps you achieve")
    regulation_source: Optional[str] = Field(None, description="Regulation it's based on")
    steps: List[QuestStep] = Field(default_factory=list, description="Quest steps")
    required_verifiers: int = Field(default=1, description="How many peers must verify completion")
    badge_name: Optional[str] = Field(None, description="Badge earned on completion")
    category: str = Field(default="general", description="Category: va_benefits, business_permit, nemt, etc.")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom attributes")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class QuestProgress(BaseModel):
    """User's progress through a quest."""
    id: str = Field(..., description="Unique progress ID")
    user_id: str = Field(..., description="User taking the quest")
    quest_id: str = Field(..., description="Quest being taken")
    current_step_id: str = Field(..., description="Current step ID")
    answers: Dict[str, Any] = Field(default_factory=dict, description="Answers so far")
    status: str = Field(default="in_progress", description="in_progress, completed, abandoned")
    verifications_received: int = Field(default=0, description="Peer verifications so far")
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = Field(None, description="When finished")


class VoiceInteraction(BaseModel):
    """Record of a voice/SMS interaction."""
    id: str = Field(..., description="Unique interaction ID")
    user_id: Optional[str] = Field(None, description="User ID (may be unknown initially)")
    phone_number: str = Field(..., description="Phone number that initiated call/SMS")
    message_type: str = Field(..., description="voice_call, sms, etc.")
    transcribed_text: Optional[str] = Field(None, description="Transcribed speech or SMS text")
    intent: Optional[str] = Field(None, description="Classified intent (benefit_lookup, permit_help, etc.)")
    response_text: Optional[str] = Field(None, description="Text response sent back")
    matched_quest: Optional[str] = Field(None, description="Quest ID if routed to a quest")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Call metadata (duration, provider, etc.)")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class VoiceRequest(BaseModel):
    """Incoming voice request (e.g., from Twilio webhook)."""
    phone_number: str = Field(...)
    message_text: Optional[str] = Field(None, description="SMS or transcribed text")
    call_id: Optional[str] = Field(None, description="Twilio call SID")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional Twilio data")


class QueryResponse(BaseModel):
    """Response to a user query."""
    text: str = Field(..., description="Text response")
    matched_quest_id: Optional[str] = Field(None, description="If routable to a quest")
    confidence: float = Field(default=1.0, description="Confidence in response (0-1)")
    verified_by: Optional[List[str]] = Field(None, description="User IDs who verified this answer")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional context")
