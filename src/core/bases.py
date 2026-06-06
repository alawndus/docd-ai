"""Abstract base classes for extensibility across voice, agents, services, parsers."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from .models import (
    VoiceRequest,
    QueryResponse,
    Quest,
    User,
    Credential,
    TrustNode,
)


class BaseVoiceHandler(ABC):
    """Base class for voice interaction handlers (Twilio, etc.)."""

    @abstractmethod
    async def receive_message(self, request: VoiceRequest) -> VoiceRequest:
        """Receive and validate incoming voice/SMS request."""
        pass

    @abstractmethod
    async def send_response(
        self, phone_number: str, response_text: str, call_id: Optional[str] = None
    ) -> bool:
        """Send response back to user via voice/SMS."""
        pass

    @abstractmethod
    async def transcribe_audio(self, audio_data: bytes) -> str:
        """Transcribe audio to text (e.g., Whisper)."""
        pass


class BaseAgent(ABC):
    """Base class for AI agents (local, cloud, specialized)."""

    def __init__(self, agent_id: str, name: str):
        self.agent_id = agent_id
        self.name = name

    @abstractmethod
    async def query(self, question: str, context: Dict[str, Any]) -> QueryResponse:
        """Answer a question given context."""
        pass

    @abstractmethod
    async def learn(self, feedback: Dict[str, Any]) -> None:
        """Learn from feedback (e.g., community verification)."""
        pass

    @abstractmethod
    async def sync(self) -> None:
        """Sync with central server (regulations, trust graph, etc.)."""
        pass

    async def health_check(self) -> bool:
        """Check if agent is operational."""
        return True


class BaseService(ABC):
    """Base class for business logic services."""

    @abstractmethod
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute service logic."""
        pass


class BaseParser(ABC):
    """Base class for document/data parsers."""

    @abstractmethod
    def parse(self, data: str) -> Dict[str, Any]:
        """Parse input data and return structured output."""
        pass


class QueryService(BaseService):
    """Service for answering user queries (voice -> answer -> quest routing)."""

    def __init__(self, trust_graph: "BaseTrustGraph", agent: BaseAgent):
        """
        Initialize QueryService.
        
        Args:
            trust_graph: Trust graph instance for peer verification
            agent: AI agent for answering questions
        """
        self.trust_graph = trust_graph
        self.agent = agent

    async def execute(self, question: str, user_id: Optional[str] = None, **kwargs) -> QueryResponse:
        """
        Execute a query: classify → check trust → invoke agent → verify.
        
        Args:
            question: User's question
            user_id: Optional user ID (for trust context)
            
        Returns:
            QueryResponse with answer and metadata
        """
        # Placeholder: will be implemented in Phase 2
        return QueryResponse(
            text="I can help with that. Please clarify your question.",
            confidence=0.5,
        )


class VerificationService(BaseService):
    """Service for community verification of completed quests."""

    def __init__(self, trust_graph: "BaseTrustGraph"):
        """
        Initialize VerificationService.
        
        Args:
            trust_graph: Trust graph instance
        """
        self.trust_graph = trust_graph

    async def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute verification logic.
        
        Returns:
            Status of verification request
        """
        # Placeholder: will be implemented in Phase 3
        return {"status": "pending"}


class BaseTrustGraph(ABC):
    """Base class for trust graph implementation."""

    @abstractmethod
    def add_user(self, user: User) -> bool:
        """Add user to trust graph."""
        pass

    @abstractmethod
    def add_trust_relationship(self, source_user_id: str, target_user_id: str, weight: float = 1.0) -> bool:
        """Create trust edge from source to target."""
        pass

    @abstractmethod
    def get_trust_score(self, user_id: str, context_user_id: Optional[str] = None) -> float:
        """Get user's trust score (optionally from another user's perspective)."""
        pass

    @abstractmethod
    def is_trusted_by(self, user_id: str, threshold: float = 0.5) -> bool:
        """Check if user meets trust threshold."""
        pass

    @abstractmethod
    def add_credential(self, credential: Credential) -> bool:
        """Add credential to trust graph."""
        pass

    @abstractmethod
    def resolve_trust_path(self, source_user_id: str, target_user_id: str) -> List[str]:
        """Find trust path between two users."""
        pass


__all__ = [
    "BaseVoiceHandler",
    "BaseAgent",
    "BaseService",
    "BaseParser",
    "BaseTrustGraph",
    "QueryService",
    "VerificationService",
]
