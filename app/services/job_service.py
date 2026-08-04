from app.mappers import JobMapper
from app.models.job import Job
from app.repositories.job_repository import JobRepository
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

    def get_jobs(self) -> list[Job]:
        return self.repository.list()

    def get_job_by_url(self, job_url: str) -> Job | None:
        return self.repository.get_by_url(job_url)
    
    async def sync_jobs(self):

        provider_jobs = await self.provider.fetch_jobs()

        saved = []

        for provider_job in provider_jobs:

            job = JobMapper.to_model(provider_job)

            saved.append(
                self.create_job(job)
            )

        return saved