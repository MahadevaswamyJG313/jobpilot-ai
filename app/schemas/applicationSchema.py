from datetime import datetime
from pydantic import BaseModel
from app.common.enums import ApplicationStatus
from app.schemas.jobSchema import JobResponse


class ApplicationBase(BaseModel):
    status: ApplicationStatus = ApplicationStatus.SAVED
    notes: str | None = None


class ApplicationCreate(ApplicationBase):
    job_id: int


class ApplicationUpdate(BaseModel):
    status: ApplicationStatus | None = None
    notes: str | None = None


class ApplicationResponse(ApplicationBase):
    id: int
    job_id: int
    applied_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
    job: JobResponse | None = None

    model_config = {
        "from_attributes": True,
    }
