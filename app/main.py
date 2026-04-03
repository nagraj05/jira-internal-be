import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.core.config import settings


def _parse_origins(raw: str) -> list[str]:
    try:
        return json.loads(raw)
    except Exception:
        return [o.strip() for o in raw.split(",")]


app = FastAPI(
    title="Jira Internal API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_parse_origins(settings.ALLOWED_ORIGINS),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"message": "Backend is running 🚀"}

app.include_router(api_router, prefix="/api/v1")