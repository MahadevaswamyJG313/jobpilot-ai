from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from app.services.notificationService import NotificationService
from app.services.schedulerService import SchedulerService

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting JobPilot AI...")

    # Instantiate services and register background schedules (sync every 12 hours)
    notification_service = NotificationService()
    scheduler = SchedulerService(
        notification_service=notification_service,
        interval_seconds=43200,
    )
    app.state.scheduler = scheduler
    scheduler.start()

    yield

    logger.info("Shutting down JobPilot AI...")
    scheduler.stop()