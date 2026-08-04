from app.models import Job
from app.providers.models import ProviderJob


class JobMapper:
    """Maps ProviderJob objects to Job database models."""

    @staticmethod
    def to_model(provider_job: ProviderJob) -> Job:
        return Job(
            title=provider_job.title,
            company_name=provider_job.company_name,
            location=provider_job.location,
            is_remote=provider_job.is_remote,
            salary_min=provider_job.salary_min,
            salary_max=provider_job.salary_max,
            salary_currency=provider_job.salary_currency,
            salary_period=provider_job.salary_period,
            source=provider_job.source,
            job_url=provider_job.job_url,
            description=provider_job.description,
        )