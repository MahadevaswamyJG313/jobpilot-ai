import logging

from app.common.enums import JobSource
from app.core.logger import setup_logger
from app.database.session import SessionLocal
from app.models import Job
from app.repositories import JobRepository
from app.services import JobService

setup_logger()
logger = logging.getLogger(__name__)


def main():
    db = SessionLocal()

    try:
        repository = JobRepository(db)
        service = JobService(repository)

        job = Job(
            title="Python API Developer",
            company_name="JobPilot",
            location="Bengaluru",
            is_remote=True,
            salary_min=1800000,
            salary_max=2500000,
            salary_currency="INR",
            salary_period="YEAR",
            source=JobSource.MANUAL,
            job_url="https://example.com/jobs/python-api",
            description="Python Backend Developer",
        )

        saved_job = service.create_job(job)

        logger.info("Saved Job ID: %s", saved_job.id)

        jobs = service.get_jobs()

        logger.info("Total Jobs: %d", len(jobs))

    finally:
        db.close()


if __name__ == "__main__":
    main()