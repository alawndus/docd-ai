# Copilot Instructions for Doc D AI Engine

**Vision**: Trendsetter app serving veterans, small businesses, and rural communities through a decentralized, voice-first, trust-based compliance network.

**Four Strategic Pillars**:
1. **Voice-Activated Command Center** — Phone/SMS queries with real-time AI + peer verification
2. **Blockchain Trust Graph** — Decentralized peer verification (immutable credentials, privacy-first)
3. **Hyper-Local AI Agents** — Edge-first deployment for offline-capable, community-specific intelligence
4. **Compliance-as-Quest** — Gamified bureaucracy (regulations as branching quests, peer voting verification)

See `plan.md` in the session folder for phased roadmap.

---

## Setup & Prerequisites

- **Python 3.11+** required
- **Virtual environment**: All commands assume `.venv/` is initialized and activated
- **Dependencies**: FastAPI, Uvicorn, Pytest, httpx, Twilio (see `requirements.txt`)

## Build, Test, and Run Commands

### Development Setup
```bash
make build          # Create venv and install all dependencies
```

### Running the Application
```bash
make run            # Start uvicorn dev server (--reload enabled) at http://127.0.0.1:8000
```

**Startup scripts** (alternative to Makefile):
- **Linux/macOS**: `./scripts/run.sh` (creates venv if needed, activates, installs, runs)
- **Windows PowerShell**: `.\scripts\run.ps1`

### Testing
```bash
make test           # Run entire test suite with pytest
pytest tests/test_simple_parser.py -v     # Run single test file
pytest tests/ -k "test_parse_key_values" -v  # Run specific test by name
```

Tests use the standard pytest discovery pattern (`tests/test_*.py` files).

### Docker
```bash
make docker-build   # Build Docker image (docd-ai:latest)
make docker-run     # Run image on port 8000
docker-compose up   # Run full stack with Chroma vector DB
```

## Architecture Overview

### Strategic Pillars (In Development)

#### 1. Voice-Activated Command Center (`/src/voice/`)
- **VoiceHandler** — Twilio webhook integration (phone/SMS)
- **Transcriber** — Convert speech to text (OpenAI Whisper)
- **QueryClassifier** — Route incoming queries (benefit lookup, compliance check, documentation)
- **VoiceFlowOrchestrator** — Manage conversation flows
- Integration: Receives voice → classifies → queries trust graph + local AI → responds via voice

#### 2. Trust Graph (`/src/trust_graph/`)
- **TrustGraphDB** — Peer-to-peer verification network (nodes: users/credentials, edges: trust relationships)
- **CredentialManager** — Issue/verify immutable credentials from quest completion
- **TrustResolver** — Algorithm to answer "should I trust this person/credential?"
- **PrivacyLayer** — Verifiable credentials (zero-knowledge proofs for sensitive data)
- Data: Uses graph DB (Neo4j or networkx initially, blockchain-ready later)

#### 3. Quest System (`/src/quests/`)
- **QuestEngine** — Evaluate compliance paths as branching decision trees
- **QuestParser** — Convert regulations into interactive quests
- **VotingSystem** — Community verification (peer voting replaces forms)
- **ProgressTracker** — Badges, milestones, completion status
- Endpoint: Voice asks question → matched to quest → guided through steps → community votes → credential issued

#### 4. Hyper-Local AI Agents (`/src/agents/`)
- **BaseAgent** — Abstract agent lifecycle (init, query, learn, sync)
- **LocalLLMAgent** — Lightweight model for edge deployment (supports offline mode)
- **SyncProtocol** — Push/pull regulations, trust graph diffs with central server
- **EdgeDeployment** — Containerized agent for Raspberry Pi, local servers
- Pattern: Deploy as Docker container, runs offline, syncs trust graph when connected

### Core Foundation

- **Domain Models** (`/src/core/models.py`) — User, Credential, Quest, VoiceInteraction, TrustNode
- **Abstract Base Classes** (`/src/core/bases.py`) — BaseParser, BaseAgent, BaseService, VoiceHandler
- **Service Layer** (`/src/services/`) — Business logic services (QueryService, VerificationService)
- **Configuration** (`src/config.py`) — Environment variables for Twilio, LLM, graph DB endpoints
- **FastAPI App** (`src/app.py`) — Routes for voice webhooks, quest API, trust graph queries

### Current Endpoints (and Future)
- `GET /health` — Health check
- `POST /parse` — Simple text parsing (legacy, will be integrated into voice/quest flows)
- `POST /voice/webhook` — Twilio webhook (incoming calls/SMS) — *in development*
- `GET /quests` — List available quests — *in development*
- `POST /quests/{quest_id}/verify` — Community voting — *in development*
- `GET /trust-graph/{user_id}/trusted-by` — Query trust relationships — *in development*

## Key Conventions

### Type Hints & Domain Models
- **Always use type hints** in function signatures and class attributes (e.g., `def parse_key_values(text: str) -> Dict[str, str]`)
- Use **union syntax** for optional types: `str | None` instead of `Optional[str]`
- Create **Pydantic BaseModel** for all domain entities (User, Credential, Quest, TrustNode)
- Import types from `typing` for complex types (Dict, List, Tuple, etc.)

### Abstract Base Classes (ABCs)
All new modules should inherit from appropriate base:
- **VoiceHandler** — For Twilio, voice transcription, call routing
- **BaseAgent** — For AI agents (with `query()`, `learn()`, `sync()` methods)
- **BaseService** — For business logic (e.g., QueryService, VerificationService)
- **BaseParser** — For document/data parsing

Example pattern:
```python
from src.core.bases import BaseAgent

class ComplianceAgent(BaseAgent):
    async def query(self, question: str) -> str:
        """Answer compliance question using local knowledge."""
        pass
```

### Service Layer Pattern
Separate concerns: API routes handle HTTP, services handle logic, agents/parsers handle data transformation.

Example:
```python
# In src/services/query_service.py
class QueryService:
    def __init__(self, trust_graph, local_agent):
        self.trust_graph = trust_graph
        self.local_agent = local_agent
    
    async def answer_query(self, question: str, user_id: str) -> Answer:
        # Classify → check trust graph → invoke agent → verify answer → return
        pass

# In src/app.py
@app.post("/voice/webhook")
async def voice_webhook(request: VoiceRequest):
    service = QueryService(trust_graph, agent)
    answer = await service.answer_query(request.transcribed_text, request.user_id)
    return TwilioResponse(message=answer.text)
```

### Testing
- Place tests in `tests/` directory mirroring the `src/` structure
- Use descriptive test names starting with `test_` (e.g., `test_trust_graph_resolves_peer_trust`)
- Tests use **Pydantic models** for request validation
- Use `httpx` for testing FastAPI endpoints
- Test abstract behaviors: all agents should pass same test suite

### Documentation
- Include **docstrings** for all functions and classes (one-liner minimum)
- Document **integration points**: How does this module talk to voice? Trust graph? Quests?
- Example docstring:
  ```python
  """
  ComplianceAgent queries local regulations and peer verification.
  
  Integrates with:
  - TrustGraph: For peer verification
  - VoiceHandler: For Twilio integration
  - QuestEngine: For guided compliance paths
  """
  ```

### Environment Configuration
- **Copy** `.env.example` → `.env` before running
- Settings loaded via Pydantic `BaseSettings` with type hints
- **New variables** for pillars (add to config.py):
  - `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER` — Voice integration
  - `GRAPH_DB_URL` — Trust graph database (Neo4j or local)
  - `LOCAL_LLM_MODEL_PATH` — For edge agent deployment
  - `BLOCKCHAIN_RPC_URL` — For future credential issuance (optional)

### Quest & Verification Pattern
1. User asks question via voice
2. QueryService classifies intent
3. If matches quest → invoke QuestEngine to guide through steps
4. At end of quest → community voting request posted
5. After N peer approvals → credential issued to trust graph
6. Credential becomes proof for future queries
