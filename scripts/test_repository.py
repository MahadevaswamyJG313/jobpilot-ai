import logging

from app.core.logger import setup_logger
from app.database.session import SessionLocal
from app.models import Job
from app.common.enums import JobSource
from app.repositories import JobRepository

setup_logger()
logger = logging.getLogger(__name__)


def main():
    db = SessionLocal()

    try:
        repo = JobRepository(db)

        job = Job(
            title="Backend Developer",
            company_name="OpenAI",
            location="Bengaluru",
            is_remote=True,
            salary_min=1500000,
            salary_max=2500000,
            salary_currency="INR",
            salary_period="YEAR",
            source=JobSource.MANUAL,
            job_url="https://example.com/jobs/backend",
            description="Backend Developer Position",
        )

        existing = repo.get_by_url(job.job_url)

        if existing is None:
            repo.create(job)
            logger.info("Job inserted successfully.")
        else:
            logger.info("Job already exists.")

        jobs = repo.list()

        logger.info("Total Jobs: %d", len(jobs))

        for item in jobs:
            logger.info(
                "%s | %s | %s",
                item.title,
                item.company_name,
                item.source.value,
            )

    finally:
        db.close()


if __name__ == "__main__":
    main()