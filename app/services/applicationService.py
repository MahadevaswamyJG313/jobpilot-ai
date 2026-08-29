from datetime import datetime
from typing import List
from app.models.applicationModel import JobApplication
from app.repositories.applicationRepository import ApplicationRepository
from app.repositories.jobRepository import JobRepository
from app.services.base_service import BaseService
from app.common.enums import ApplicationStatus


class ApplicationService(BaseService):

    def __init__(self, repository: ApplicationRepository, job_repository: JobRepository):
        self.repository = repository
        self.job_repository = job_repository

    def track_job_status(
        self,
        job_id: int,
        status: ApplicationStatus,
        notes: str | None = None,
    ) -> JobApplication:
        # Validate that the job exists
        job = self.job_repository.get_by_id(job_id)
        if not job:
            raise ValueError(f"Job with ID {job_id} does not exist.")

        existing = self.repository.get_by_job_id(job_id)

        if existing:
            # Update values
            if status == ApplicationStatus.APPLIED and existing.status != ApplicationStatus.APPLIED:
                existing.applied_at = datetime.utcnow()
            elif status != ApplicationStatus.APPLIED:
                existing.applied_at = None

            existing.status = status
            if notes is not None:
                existing.notes = notes

            return self.repository.update(existing)
        else:
            # Create new tracking record
            applied_at = datetime.utcnow() if status == ApplicationStatus.APPLIED else None
            app_record = JobApplication(
                job_id=job_id,
                status=status,
                applied_at=applied_at,
                notes=notes,
            )
            return self.repository.create(app_record)

    def get_application_by_id(self, application_id: int) -> JobApplication | None:
        return self.repository.get_by_id(application_id)

    def get_application_by_job_id(self, job_id: int) -> JobApplication | None:
        return self.repository.get_by_job_id(job_id)

    def list_applications(self, status: ApplicationStatus | None = None) -> List[JobApplication]:
        return self.repository.list(status=status)

    def delete_application(self, application_id: int) -> bool:
        application = self.repository.get_by_id(application_id)
        if not application:
            return False
        self.repository.delete(application)
        return True
