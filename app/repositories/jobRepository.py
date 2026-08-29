from typing import List
from sqlalchemy.orm import Session

from app.models.jobModel import Job
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

    def list(self) -> List[Job]:
        return self.db.query(Job).all()

    def delete(self, job: Job) -> None:
        self.db.delete(job)
        self.db.commit()

    def get_by_id(self, job_id: int) -> Job | None:
        return self.db.query(Job).filter(Job.id == job_id).first()

    def search(
        self,
        q: str | None = None,
        location: str | None = None,
        is_remote: bool | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Job]:
        query = self.db.query(Job)

        if q:
            search_filter = (
                Job.title.ilike(f"%{q}%")
                | Job.company_name.ilike(f"%{q}%")
                | Job.description.ilike(f"%{q}%")
            )
            query = query.filter(search_filter)

        if location:
            query = query.filter(Job.location.ilike(f"%{location}%"))

        if is_remote is not None:
            query = query.filter(Job.is_remote == is_remote)

        return (
            query.order_by(Job.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
