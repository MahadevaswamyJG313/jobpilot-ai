import asyncio
import logging
from app.database.session import SessionLocal
from app.repositories.jobRepository import JobRepository
from app.services.jobService import JobService
from app.providers.remoteok_provider import RemoteOKProvider
from app.services.notificationService import NotificationService

logger = logging.getLogger(__name__)


class SchedulerService:

    def __init__(
        self,
        notification_service: NotificationService,
        interval_seconds: int = 3600,
    ):
        self.notification_service = notification_service
        self.interval_seconds = interval_seconds
        self._running = False
        self._task = None

    def start(self) -> None:
        """Start the background synchronization scheduler task loop."""
        if self._running:
            logger.warning("Scheduler is already running.")
            return

        self._running = True
        self._task = asyncio.create_task(self._loop())
        logger.info(
            f"Scheduler background service started with interval={self.interval_seconds}s."
        )

    def stop(self) -> None:
        """Stop the background synchronization scheduler task loop."""
        if not self._running:
            logger.warning("Scheduler is not running.")
            return

        self._running = False
        if self._task:
            self._task.cancel()
            logger.info("Scheduler background service cancel requested.")
        logger.info("Scheduler background service stopped.")

    async def _loop(self) -> None:
        """Continuous ingestion and notification loop."""
        await asyncio.sleep(2)

        while self._running:
            logger.info("Scheduler: Starting ingestion sync cycle...")
            db = SessionLocal()
            try:
                repository = JobRepository(db)
                provider = RemoteOKProvider()
                job_service = JobService(repository, provider)

                newly_saved_jobs = await job_service.sync_jobs()

                if newly_saved_jobs:
                    self.notification_service.notify_new_jobs(newly_saved_jobs)
                else:
                    logger.info("Scheduler: No new jobs found this cycle.")

            except asyncio.CancelledError:
                logger.info("Scheduler loop task canceled cleanly.")
                break
            except Exception as e:
                logger.exception(f"Scheduler error during sync cycle: {str(e)}")
            finally:
                db.close()

            try:
                await asyncio.sleep(self.interval_seconds)
            except asyncio.CancelledError:
                break
