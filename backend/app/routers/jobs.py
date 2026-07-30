from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user, get_current_admin
from app.models.user import User
from app.schemas.job import JobCreate, JobUpdate, JobResponse
from app.services.job import JobService

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)

@router.post("", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def create_job_api(
    job_in: JobCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    service = JobService(db)
    return service.create_job(
        creator_public_id=str(current_admin.public_id),
        **job_in.model_dump()
    )

@router.get("", response_model=List[JobResponse])
def list_jobs_api(
    company: str | None = None,
    location: str | None = None,
    keyword: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = JobService(db)
    if company:
        return service.get_jobs_by_company(company)
    elif location:
        return service.get_jobs_by_location(location)
    elif keyword:
        return service.search_jobs(keyword)
    return service.get_all_jobs()

@router.get("/active", response_model=List[JobResponse])
def get_active_jobs_api(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = JobService(db)
    return service.get_active_jobs()

@router.get("/{public_id}", response_model=JobResponse)
def get_job_api(
    public_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = JobService(db)
    job = service.get_job(public_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    return job

@router.put("/{public_id}", response_model=JobResponse)
def update_job_api(
    public_id: str,
    job_in: JobUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    service = JobService(db)
    try:
        return service.update_job(
            public_id=public_id,
            **job_in.model_dump(exclude_unset=True)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.delete("/{public_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job_api(
    public_id: str,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    service = JobService(db)
    try:
        service.delete_job(public_id)
        return
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
