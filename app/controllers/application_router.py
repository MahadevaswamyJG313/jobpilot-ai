from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.schemas.applicationSchema import ApplicationResponse, ApplicationCreate, ApplicationUpdate
from app.repositories.applicationRepository import ApplicationRepository
from app.repositories.jobRepository import JobRepository
from app.services.applicationService import ApplicationService
from app.common.enums import ApplicationStatus

router = APIRouter(
    prefix="/applications",
    tags=["Job Applications"],
)


def get_application_service(db: Session = Depends(get_db)) -> ApplicationService:
    repository = ApplicationRepository(db)
    job_repository = JobRepository(db)
    return ApplicationService(repository, job_repository)


@router.post("", response_model=ApplicationResponse, status_code=201)
async def track_application(
    payload: ApplicationCreate,
    service: ApplicationService = Depends(get_application_service),
):
    """Create or update tracking status of a job (SAVED, APPLIED, REJECTED, etc.)."""
    try:
        return service.track_job_status(
            job_id=payload.job_id,
            status=payload.status,
            notes=payload.notes,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[ApplicationResponse])
async def list_applications(
    status: ApplicationStatus | None = Query(None, description="Filter by status"),
    service: ApplicationService = Depends(get_application_service),
):
    """List tracked applications, optionally filtering by status."""
    return service.list_applications(status=status)


@router.get("/{application_id}", response_model=ApplicationResponse)
async def get_application(
    application_id: int,
    service: ApplicationService = Depends(get_application_service),
):
    """Retrieve detailed tracking details of a single application by ID."""
    app_record = service.get_application_by_id(application_id)
    if not app_record:
        raise HTTPException(status_code=404, detail="Application tracking record not found")
    return app_record


@router.put("/{application_id}", response_model=ApplicationResponse)
async def update_application(
    application_id: int,
    payload: ApplicationUpdate,
    service: ApplicationService = Depends(get_application_service),
):
    """Update tracking notes or status of an existing application."""
    app_record = service.get_application_by_id(application_id)
    if not app_record:
        raise HTTPException(status_code=404, detail="Application tracking record not found")
    try:
        return service.track_job_status(
            job_id=app_record.job_id,
            status=payload.status if payload.status is not None else app_record.status,
            notes=payload.notes if payload.notes is not None else app_record.notes,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{application_id}", status_code=204)
async def delete_application(
    application_id: int,
    service: ApplicationService = Depends(get_application_service),
):
    """Remove tracking records (cancels unsaved or status logs)."""
    success = service.delete_application(application_id)
    if not success:
        raise HTTPException(status_code=404, detail="Application tracking record not found")
