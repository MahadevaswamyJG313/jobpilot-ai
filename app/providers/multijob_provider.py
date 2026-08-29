import asyncio
import logging
from app.providers.base import JobProvider
from app.providers.models import ProviderJob

logger = logging.getLogger(__name__)


class MultiJobProvider(JobProvider):
    """Composite provider aggregating jobs from multiple sub-providers concurrently."""

    def __init__(self, providers: list[JobProvider]):
        self.providers = providers

    async def fetch_jobs(self) -> list[ProviderJob]:
        logger.info(f"MultiJobProvider: Gathering jobs from {len(self.providers)} providers...")

        tasks = [provider.fetch_jobs() for provider in self.providers]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        combined_jobs = []
        seen_urls = set()

        for provider, res in zip(self.providers, results):
            if isinstance(res, Exception):
                logger.error(f"MultiJobProvider: Provider {provider.__class__.__name__} failed: {res}")
                continue

            for job in res:
                if job.job_url not in seen_urls:
                    seen_urls.add(job.job_url)
                    combined_jobs.append(job)

        logger.info(f"MultiJobProvider: Aggregated {len(combined_jobs)} unique jobs total.")
        return combined_jobs
