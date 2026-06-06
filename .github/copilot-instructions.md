# Copilot Instructions for Doc D AI Engine

## Setup & Prerequisites

- **Python 3.11+** required
- **Virtual environment**: All commands assume `.venv/` is initialized and activated
- **Dependencies**: FastAPI, Uvicorn, Pytest, httpx (see `requirements.txt`)

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

### Modular Agent Framework
The engine is built around a modular architecture for extensibility:

- **`/src/parsers/`** — Document parsing modules (e.g., `simple_parser.py` extracts key-value pairs)
- **`/src/agents/`** — AI agents (currently placeholder; intended for specialized task handlers)
- **`/src/core/`** — Core engine logic (currently placeholder; will contain base classes)
- **`/src/pipelines/`** — Workflow orchestration (not yet implemented)
- **`/src/services/`** — Business logic and integrations (not yet implemented)
- **`/src/utils/`** — Shared utilities (not yet implemented)

### FastAPI Application
- **Entry point**: `src/app.py`
- **Configuration**: `src/config.py` (Pydantic `Settings` loaded from `.env`)
- **Current endpoints**:
  - `GET /health` — Health check (returns `{"status": "ok"}`)
  - `POST /parse` — Parse text and extract key-value pairs (request body: `{"text": "..."}`)

### Environment Configuration
- Copy `.env.example` → `.env` before running
- Settings are loaded via Pydantic `BaseSettings` with type hints (e.g., `vector_db_url: str | None`)
- Common variables: `APP_HOST`, `APP_PORT`, `DEBUG`, `LOG_LEVEL`, `VECTOR_DB_URL`

## Key Conventions

### Type Hints
- **Always use type hints** in function signatures and class attributes (e.g., `def parse_key_values(text: str) -> Dict[str, str]`)
- Use **union syntax** for optional types: `str | None` instead of `Optional[str]`
- Import types from `typing` for complex types (Dict, List, Tuple, etc.)

### Testing
- Place tests in `tests/` directory mirroring the `src/` structure
- Use descriptive test names starting with `test_` (e.g., `test_parse_key_values_basic`)
- Tests use **Pydantic models** for request validation
- Use `httpx` for testing FastAPI endpoints (TestClient available in fastapi.testclient)

### Request/Response Models
- Define Pydantic `BaseModel` classes for all API request/response bodies
- Keep models in `src/app.py` or dedicated `models.py` file as the project scales
- Example: `class ParseRequest(BaseModel): text: str`

### Documentation
- Include **docstrings** for all functions and classes (one-liner minimum)
- Example: `"""Parse lines of the form `Key: Value` into a dict."""`

### Project Growth
- When adding new modules, follow the `/src/{domain}/` pattern (e.g., `src/compliance/`, `src/nemt/`)
- Create `__init__.py` in new directories for proper package structure
- Future integrations (vector DB, rules engine) should be abstracted as services in `/src/services/`

## Local Vector DB (Optional)
Chroma is pre-configured in `docker-compose.yml` for local development. To use:
1. Set `VECTOR_DB_URL=http://localhost:8001` in `.env`
2. Run `docker-compose up`

## Notes
- The project is intentionally minimal to support incremental growth
- All features mentioned in README (compliance, rural infrastructure, NEMT) are scaffolded for future implementation
