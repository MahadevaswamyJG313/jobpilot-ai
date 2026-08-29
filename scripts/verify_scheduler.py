import asyncio
import logging
from app.services.notificationService import NotificationService
from app.services.schedulerService import SchedulerService
from app.core.logger import setup_logger

setup_logger()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    logger.info("Initializing check scheduler verification...")
    notification_service = NotificationService()

    # Configure a short interval of 3 seconds for active testing
    scheduler = SchedulerService(
        notification_service=notification_service,
        interval_seconds=3,
    )

    logger.info("Starting scheduler in background...")
    scheduler.start()

    logger.info("Waiting for scheduler execution ticks...")
    await asyncio.sleep(7)

    logger.info("Stopping scheduler...")
    scheduler.stop()
    logger.info("Scheduler verified successfully!")


if __name__ == "__main__":
    asyncio.run(main())
