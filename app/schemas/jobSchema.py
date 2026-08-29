from datetime import datetime
from pydantic import BaseModel
from app.common.enums import JobSource


class JobResponse(BaseModel):
    id: int
    title: str
    company_name: str
    location: str
    source: JobSource
    job_url: str
    description: str | None = None
    created_at: datetime
    updated_at: datetime
    salary_min: float | None = None
    salary_max: float | None = None
    salary_currency: str | None = None
    salary_period: str | None = None
    is_remote: bool

    model_config = {
        "from_attributes": True,
    }
