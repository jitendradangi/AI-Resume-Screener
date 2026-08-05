from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.job import JobCreate, JobUpdate, JobResponse
from app.services.job import job_service

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def create_job(
    job_in: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new job posting."""
    service = job_service(db)
    try:
        return service.create_job(
            user_public_id=str(current_user.public_id),
            **job_in.model_dump(),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[JobResponse])
def get_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all jobs for the current user."""
    service = job_service(db)
    try:
        return service.get_user_jobs(user_public_id=str(current_user.public_id))
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/open", response_model=List[JobResponse])
def get_open_jobs(
    db: Session = Depends(get_db),
):
    """Get all open jobs (public endpoint)."""
    service = job_service(db)
    return service.get_open_jobs()


@router.get("/search", response_model=List[JobResponse])
def search_jobs(
    title: str | None = None,
    company: str | None = None,
    location: str | None = None,
    db: Session = Depends(get_db),
):
    """Search jobs by title, company, or location."""
    service = job_service(db)
    return service.search_jobs(
        title=title,
        company=company,
        location=location,
    )


@router.get("/{public_id}", response_model=JobResponse)
def get_job(
    public_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific job by public ID."""
    service = job_service(db)
    job = service.get_job(public_id=public_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    if job.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized to access this job"
        )
    return job


@router.put("/{public_id}", response_model=JobResponse)
def update_job(
    public_id: str,
    job_in: JobUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a job posting."""
    service = job_service(db)
    try:
        return service.update_job(
            public_id=public_id,
            user_id=current_user.id,
            **job_in.model_dump(exclude_unset=True),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )


@router.delete("/{public_id}")
def delete_job(
    public_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a job posting."""
    service = job_service(db)
    try:
        service.delete_job(
            public_id=public_id,
            user_id=current_user.id,
        )
        return {"success": True, "message": "Job deleted successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )


@router.post("/{public_id}/parse")
def parse_job(
    public_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Parse job description and extract structured information."""
    service = job_service(db)
    try:
        return service.parse_job_description(public_id=public_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
