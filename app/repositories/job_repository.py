from sqlalchemy.orm import Session

from app.models.job import Job
from app.repositories.base_repository import BaseRepository


class JobRepository(BaseRepository):

    def __init__(self, db: Session):
        super().__init__(db)

    def create(self, job: Job) -> Job:
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def get_by_url(self, job_url: str) -> Job | None:
        return (
            self.db.query(Job)
            .filter(Job.job_url == job_url)
            .first()
        )

    def list(self) -> list[Job]:
        return self.db.query(Job).all()

    def delete(self, job: Job) -> None:
        self.db.delete(job)
        self.db.commit()