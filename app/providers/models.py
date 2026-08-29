from pydantic import BaseModel

from app.common.enums import JobSource


class ProviderJob(BaseModel):
    title: str
    company_name: str
    location: str

    is_remote: bool = False

    salary_min: float | None = None
    salary_max: float | None = None
    salary_currency: str | None = None
    salary_period: str | None = None

    source: JobSource

    job_url: str

    description: str | None = None