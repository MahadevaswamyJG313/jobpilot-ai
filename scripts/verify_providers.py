import asyncio
import logging
from app.providers.remoteok_provider import RemoteOKProvider
from app.providers.linkedin_provider import LinkedInProvider
from app.providers.arbeitnow_provider import ArbeitnowProvider
from app.providers.multijob_provider import MultiJobProvider
from app.core.logger import setup_logger

setup_logger()
logger = logging.getLogger(__name__)


async def main():
    logger.info("Initializing multi-provider verification...")

    remoteok = RemoteOKProvider()
    linkedin = LinkedInProvider()
    arbeitnow = ArbeitnowProvider()
    multi = MultiJobProvider([remoteok, linkedin, arbeitnow])

    logger.info("--- Testing RemoteOKProvider ---")
    rem_jobs = await remoteok.fetch_jobs()
    logger.info(f"RemoteOK: fetched {len(rem_jobs)} jobs.")

    logger.info("--- Testing LinkedInProvider ---")
    li_jobs = await linkedin.fetch_jobs()
    logger.info(f"LinkedIn: fetched {len(li_jobs)} jobs.")

    logger.info("--- Testing ArbeitnowProvider ---")
    an_jobs = await arbeitnow.fetch_jobs()
    logger.info(f"Arbeitnow: fetched {len(an_jobs)} jobs.")

    logger.info("--- Testing MultiJobProvider aggregation ---")
    all_jobs = await multi.fetch_jobs()
    logger.info(f"MultiJobProvider aggregated total: {len(all_jobs)} jobs.")

    assert len(all_jobs) > 0, "Aggregation list should not be empty!"
    logger.info("All providers verified successfully!")


if __name__ == "__main__":
    asyncio.run(main())
