from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.dependencies.providers import get_job_provider
from app.providers.base import JobProvider
from app.schemas.jobSchema import JobResponse
from app.repositories.jobRepository import JobRepository
from app.services.jobService import JobService

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


def get_job_service(
    db: Session = Depends(get_db),
    provider: JobProvider = Depends(get_job_provider),
) -> JobService:
    repository = JobRepository(db)
    return JobService(repository, provider)


@router.get("", response_model=list[JobResponse])
async def search_jobs(
    q: str | None = Query(None, description="Search term for job title, company, or description"),
    location: str | None = Query(None, description="Filter by location"),
    is_remote: bool | None = Query(None, description="Filter by remote status"),
    limit: int = Query(50, ge=1, le=100, description="Page limit (1-100)"),
    offset: int = Query(0, ge=0, description="Page offset"),
    service: JobService = Depends(get_job_service),
):
    """Retrieve jobs with optional query, location, and remote filters via JobService."""
    return service.search_jobs(
        q=q,
        location=location,
        is_remote=is_remote,
        limit=limit,
        offset=offset,
    )


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: int,
    service: JobService = Depends(get_job_service),
):
    """Retrieve a single job details by its ID via JobService."""
    job = service.get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
