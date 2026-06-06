from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel

from src.config import settings
from src.parsers.simple_parser import parse_key_values

app = FastAPI(title="Doc D AI Engine (minimal)")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}



class ParseRequest(BaseModel):
    text: str


@app.post("/parse")
async def parse_text(req: ParseRequest) -> dict[str, Any]:
    """Parse provided text and return extracted key/value pairs."""
    parsed = parse_key_values(req.text)
    return {"parsed": parsed}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.app_host, port=settings.app_port, reload=settings.debug)
