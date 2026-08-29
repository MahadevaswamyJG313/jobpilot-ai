import logging
import httpx
from app.common.enums import JobSource
from app.providers.base import JobProvider
from app.providers.models import ProviderJob

logger = logging.getLogger(__name__)


class ArbeitnowProvider(JobProvider):
    """Fetches public jobs from the official free Arbeitnow API board."""

    BASE_URL = "https://www.arbeitnow.com/api/job-board-api"

    async def fetch_jobs(self) -> list[ProviderJob]:
        logger.info("ArbeitnowProvider: Fetching live jobs...")
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(
                    self.BASE_URL,
                    headers={
                        "User-Agent": "JobPilotAI/0.1",
                    },
                )
                response.raise_for_status()
                payload = response.json()

                data = payload.get("data", [])
                logger.info(f"ArbeitnowProvider: Successfully fetched {len(data)} records.")

                jobs = []
                for item in data:
                    jobs.append(
                        ProviderJob(
                            title=item.get("title", "Unknown Role"),
                            company_name=item.get("company_name", "Unknown Company"),
                            location=item.get("location", "Remote"),
                            job_url=item.get("url", ""),
                            source=JobSource.ARBEITNOW,
                            description=item.get("description", "No description provided."),
                            is_remote=item.get("remote", True),
                        )
                    )
                return jobs

        except Exception as e:
            logger.error(f"ArbeitnowProvider: Fetch failed ({str(e)}). Returning empty payload.")
            return []
