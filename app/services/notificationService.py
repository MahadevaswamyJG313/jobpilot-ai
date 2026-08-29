import logging
from typing import List
from app.models.jobModel import Job
from app.services.base_service import BaseService

logger = logging.getLogger(__name__)


class NotificationService(BaseService):

    def notify_new_jobs(self, jobs: List[Job]) -> None:
        """Mock dispatcher formatting premium job alerts to user delivery streams."""
        if not jobs:
            logger.info("Scheduler check: No new jobs ingested to notify.")
            return

        logger.info(f"🔔 NOTIFICATION: Found {len(jobs)} new job(s) from scheduled sync!")
        for job in jobs:
            print(
                f"\n==================================================\n"
                f"🚨 NEW JOB INGESTED: {job.title}\n"
                f"   Company:  {job.company_name}\n"
                f"   Location: {job.location} (Remote: {job.is_remote})\n"
                f"   Source:   {job.source.value if job.source else 'Unknown'}\n"
                f"   URL:      {job.job_url}\n"
                f"==================================================\n"
            )
