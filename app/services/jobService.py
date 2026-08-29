from typing import List
from app.mappers.jobMapper import JobMapper
from app.models.jobModel import Job
from app.repositories.jobRepository import JobRepository
from app.services.base_service import BaseService
from app.providers.base import JobProvider


class JobService(BaseService):

    def __init__(self, repository: JobRepository, provider: JobProvider):
        self.repository = repository
        self.provider = provider

    def create_job(self, job: Job) -> Job:
        existing = self.repository.get_by_url(job.job_url)

        if existing:
            return existing

        return self.repository.create(job)

    def get_jobs(self) -> List[Job]:
        return self.repository.list()

    def get_job_by_url(self, job_url: str) -> Job | None:
        return self.repository.get_by_url(job_url)

    def search_jobs(
        self,
        q: str | None = None,
        location: str | None = None,
        is_remote: bool | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Job]:
        return self.repository.search(
            q=q,
            location=location,
            is_remote=is_remote,
            limit=limit,
            offset=offset,
        )

    def get_job_by_id(self, job_id: int) -> Job | None:
        return self.repository.get_by_id(job_id)

    async def sync_jobs(self) -> List[Job]:
        provider_jobs = await self.provider.fetch_jobs()

        saved = []

        for provider_job in provider_jobs:
            existing = self.repository.get_by_url(provider_job.job_url)
            if not existing:
                job = JobMapper.to_model(provider_job)
                new_job = self.repository.create(job)
                saved.append(new_job)

        return saved
