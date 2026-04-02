from fastapi import FastAPI
from app.api.v1.api import api_router

app = FastAPI(
    title="Jira Clone API",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Backend is running 🚀"}

app.include_router(api_router, prefix="/api/v1")