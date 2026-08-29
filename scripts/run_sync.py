import asyncio
import logging

from app.core.logger import setup_logger
from app.database.session import SessionLocal
from app.repositories.jobRepository import JobRepository
from app.services.jobService import JobService
from app.providers.remoteok_provider import RemoteOKProvider

setup_logger()
logger = logging.getLogger(__name__)


async def main():
    db = SessionLocal()
    try:
        repository = JobRepository(db)
        provider = RemoteOKProvider()
        service = JobService(repository, provider)

        logger.info("Starting RemoteOK job synchronization...")
        saved_jobs = await service.sync_jobs()
        logger.info("Synchronization complete.")
        logger.info("Total synchronized/processed jobs: %d", len(saved_jobs))
    except Exception as e:
        logger.exception("Failed to synchronize jobs: %s", str(e))
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(main())
