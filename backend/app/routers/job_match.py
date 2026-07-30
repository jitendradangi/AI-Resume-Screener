from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.job_match import JobMatchCreate, JobMatchResponse
from app.services.job_match import JobMatchService

router = APIRouter(
    prefix="/matches",
    tags=["Job Matches"]
)

@router.post("", response_model=JobMatchResponse, status_code=status.HTTP_201_CREATED)
def create_match_api(
    match_in: JobMatchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = JobMatchService(db)
    try:
        return service.create_match(
            resume_public_id=match_in.resume_public_id,
            job_public_id=match_in.job_public_id,
            **match_in.model_dump(exclude={"resume_public_id", "job_public_id"})
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/resume/{resume_public_id}", response_model=List[JobMatchResponse])
def get_resume_matches_api(
    resume_public_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = JobMatchService(db)
    try:
        return service.get_resume_matches(resume_public_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.get("/job/{job_public_id}", response_model=List[JobMatchResponse])
def get_job_matches_api(
    job_public_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = JobMatchService(db)
    try:
        return service.get_job_matches(job_public_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.get("/{resume_public_id}/{job_public_id}", response_model=JobMatchResponse)
def get_match_api(
    resume_public_id: str,
    job_public_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = JobMatchService(db)
    try:
        match = service.get_match(resume_public_id, job_public_id)
        if not match:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job match not found"
            )
        return match
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
