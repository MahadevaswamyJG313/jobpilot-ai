from fastapi import FastAPI

from app.core.settings import settings

app = FastAPI(
    title=settings.app_name,
    description="AI-powered job discovery, matching, and application assistant.",
    version=settings.app_version,
)


@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.app_name}"
    }