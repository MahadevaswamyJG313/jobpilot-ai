from typing import List
from sqlalchemy.orm import Session, joinedload
from app.models.applicationModel import JobApplication
from app.repositories.base_repository import BaseRepository
from app.common.enums import ApplicationStatus


class ApplicationRepository(BaseRepository):

    def __init__(self, db: Session):
        super().__init__(db)

    def create(self, application: JobApplication) -> JobApplication:
        self.db.add(application)
        self.db.commit()
        self.db.refresh(application)
        return application

    def get_by_id(self, application_id: int) -> JobApplication | None:
        return (
            self.db.query(JobApplication)
            .options(joinedload(JobApplication.job))
            .filter(JobApplication.id == application_id)
            .first()
        )

    def get_by_job_id(self, job_id: int) -> JobApplication | None:
        return (
            self.db.query(JobApplication)
            .options(joinedload(JobApplication.job))
            .filter(JobApplication.job_id == job_id)
            .first()
        )

    def list(self, status: ApplicationStatus | None = None) -> List[JobApplication]:
        query = self.db.query(JobApplication).options(joinedload(JobApplication.job))
        if status:
            query = query.filter(JobApplication.status == status)
        return query.all()

    def update(self, application: JobApplication) -> JobApplication:
        self.db.commit()
        self.db.refresh(application)
        return application

    def delete(self, application: JobApplication) -> None:
        self.db.delete(application)
        self.db.commit()
