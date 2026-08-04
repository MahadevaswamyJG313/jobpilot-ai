import logging

from app.common.enums import JobSource
from app.core.logger import setup_logger
from app.mappers import JobMapper
from app.providers import ProviderJob

setup_logger()
logger = logging.getLogger(__name__)


def main():
    provider_job = ProviderJob(
        title="Python Backend Developer",
        company_name="OpenAI",
        location="Bengaluru",
        is_remote=True,
        salary_min=1800000,
        salary_max=2500000,
        salary_currency="INR",
        salary_period="YEAR",
        source=JobSource.MANUAL,
        job_url="https://example.com/job/python",
        description="Backend API Developer",
    )

    job = JobMapper.to_model(provider_job)

    logger.info("Mapped Job")
    logger.info("Title: %s", job.title)
    logger.info("Company: %s", job.company_name)
    logger.info("Source: %s", job.source.value)


if __name__ == "__main__":
    main()