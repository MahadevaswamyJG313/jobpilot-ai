import logging

from fastapi import FastAPI

from app.api.v1.health import router as health_router
from app.controllers.job_router import router as jobs_router
from app.controllers.application_router import router as application_router
from app.core.lifespan import lifespan
from app.core.logger import setup_logger
from app.core.settings import settings

setup_logger()

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    description="AI-powered job discovery, matching, and application assistant.",
    version=settings.app_version,
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(jobs_router, prefix="/api/v1")
app.include_router(application_router, prefix="/api/v1")


@app.get("/")
async def root():
    logger.info("Root endpoint accessed")

    return {
        "message": f"Welcome to {settings.app_name}"
    }