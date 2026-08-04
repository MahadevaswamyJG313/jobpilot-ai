import asyncio
import logging

from app.core.logger import setup_logger
from app.providers import MockProvider

setup_logger()
logger = logging.getLogger(__name__)


async def main():
    provider = MockProvider()

    jobs = await provider.fetch_jobs()

    logger.info("Jobs fetched: %d", len(jobs))

    for job in jobs:
        logger.info("%s | %s", job.title, job.company_name)


if __name__ == "__main__":
    asyncio.run(main())