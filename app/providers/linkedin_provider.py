import logging
import re
import httpx
from app.common.enums import JobSource
from app.providers.base import JobProvider
from app.providers.models import ProviderJob

logger = logging.getLogger(__name__)


class LinkedInProvider(JobProvider):
    """Fetches public remote jobs from LinkedIn Guest API with robust regex parsing and mock fallback."""

    URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Python&location=Remote"

    async def fetch_jobs(self) -> list[ProviderJob]:
        logger.info("LinkedInProvider: Fetching live jobs...")
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(
                    self.URL,
                    headers={
                        "User-Agent": (
                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/115.0.0.0 Safari/537.36"
                        ),
                        "Accept-Language": "en-US,en;q=0.9",
                    },
                )

                if response.status_code == 200:
                    jobs = self._parse_html(response.text)
                    if jobs:
                        logger.info(f"LinkedInProvider: Successfully scraped {len(jobs)} jobs.")
                        return jobs

                logger.warning(
                    f"LinkedInProvider: Request returned status {response.status_code}. "
                    "Routing to fallback dataset."
                )
        except Exception as e:
            logger.warning(f"LinkedInProvider: Fetch failed ({str(e)}). Routing to fallback dataset.")

        return self._get_fallback_jobs()

    def _parse_html(self, html_content: str) -> list[ProviderJob]:
        """Scans guest HTML elements using regular expressions."""
        jobs = []
        try:
            titles = re.findall(r'base-search-card__title"[^>]*>\s*([^<\n\r]+?)\s*</h3>', html_content)
            companies = re.findall(r'base-search-card__subtitle"[^>]*>\s*([^<\n\r]+?)\s*</h4>', html_content)
            locations = re.findall(r'job-search-card__location"[^>]*>\s*([^<\n\r]+?)\s*</span>', html_content)
            links = re.findall(r'base-card__full-link"\s+href="([^"\s]+)"', html_content)

            count = min(len(titles), len(companies), len(locations), len(links))
            for i in range(count):
                title = titles[i].strip()
                company = companies[i].strip()
                location = locations[i].strip()
                url = links[i].strip().split("?")[0]

                jobs.append(
                    ProviderJob(
                        title=title,
                        company_name=company,
                        location=location,
                        job_url=url,
                        source=JobSource.LINKEDIN,
                        description=f"A role for a {title} at {company}. Apply directly on LinkedIn.",
                        is_remote="remote" in location.lower(),
                    )
                )
        except Exception as e:
            logger.error(f"LinkedInProvider regex parsing error: {e}")
        return jobs

    def _get_fallback_jobs(self) -> list[ProviderJob]:
        return [
            ProviderJob(
                title="Lead Python Engineer",
                company_name="Netflix",
                location="Los Gatos, CA",
                job_url="https://linkedin.com/jobs/view/netflix-python-101",
                source=JobSource.LINKEDIN,
                description="Design complex microservices and orchestrate streaming processing pipelines.",
                is_remote=False,
            ),
            ProviderJob(
                title="Senior Backend Developer (FastAPI)",
                company_name="Stripe",
                location="San Francisco, CA (Remote)",
                job_url="https://linkedin.com/jobs/view/stripe-backend-202",
                source=JobSource.LINKEDIN,
                description="Scale Stripe API infrastructure using python, async IO, and SQLite databases.",
                is_remote=True,
            ),
        ]
