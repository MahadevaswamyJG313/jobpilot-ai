from app.common.enums import JobSource
from app.providers.base import JobProvider
from app.providers.models import ProviderJob


class MockProvider(JobProvider):
    """Temporary provider used for development and testing."""

    async def fetch_jobs(self) -> list[ProviderJob]:
        return [
            ProviderJob(
                title="Python Backend Developer",
                company_name="JobPilot AI",
                location="Bengaluru",
                is_remote=True,
                salary_min=1800000,
                salary_max=2500000,
                salary_currency="INR",
                salary_period="YEAR",
                source=JobSource.MANUAL,
                job_url="https://example.com/jobs/python-backend",
                description="Backend Developer",
            ),
            ProviderJob(
                title="Golang Backend Engineer",
                company_name="JobPilot AI",
                location="Remote",
                is_remote=True,
                salary_min=2200000,
                salary_max=3000000,
                salary_currency="INR",
                salary_period="YEAR",
                source=JobSource.MANUAL,
                job_url="https://example.com/jobs/golang-backend",
                description="Go Developer",
            ),
        ]