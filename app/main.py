from fastapi import FastAPI
import logging

from app.core.logger import setup_logger
from app.core.settings import settings

setup_logger()

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    description="AI-powered job discovery, matching, and application assistant.",
    version=settings.app_version,
)


@app.get("/")
async def root():
    logger.info("Root endpoint accessed")

    return {
        "message": f"Welcome to {settings.app_name}"
    }