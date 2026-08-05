from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.job_match import JobMatchCreate, JobMatchResponse, JobRecommendation
from app.services.job_match import JobMatchService

router = APIRouter(
    prefix="/matches",
    tags=["Job Matches"],
    responses={
        401: {"description": "Unauthorized"},
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    }
)

@router.post(
    "",
    response_model=JobMatchResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a job match",
    description="Create a new match between a resume and a job with skill comparison analysis."
)
def create_match_api(
    match_in: JobMatchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a skill-based match between resume and job."""
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
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create match: {str(e)}"
        )

@router.get(
    "/resume/{resume_public_id}",
    response_model=List[JobMatchResponse],
    summary="Get all matches for a resume",
    description="Retrieve all job matches for a specific resume, sorted by match score."
)
def get_resume_matches_api(
    resume_public_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all matches for a specific resume."""
    service = JobMatchService(db)
    try:
        return service.get_resume_matches(resume_public_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve matches: {str(e)}"
        )

@router.get(
    "/job/{job_public_id}",
    response_model=List[JobMatchResponse],
    summary="Get all matches for a job",
    description="Retrieve all resume matches for a specific job, sorted by match score."
)
def get_job_matches_api(
    job_public_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all matches for a specific job."""
    service = JobMatchService(db)
    try:
        return service.get_job_matches(job_public_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve matches: {str(e)}"
        )

@router.get(
    "/recommendations/{resume_public_id}",
    response_model=List[JobRecommendation],
    summary="Get job recommendations",
    description="Get personalized job recommendations for a resume based on comprehensive matching analysis."
)
def get_job_recommendations_api(
    resume_public_id: str,
    top_n: int = Query(10, ge=1, le=50, description="Number of recommendations to return (1-50)"),
    min_match: float = Query(None, ge=0, le=100, description="Minimum match score threshold (0-100)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get job recommendations for a resume sorted by match score."""
    service = JobMatchService(db)
    try:
        return service.get_job_recommendations(
            resume_public_id=resume_public_id,
            top_n=top_n,
            min_match=min_match,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate recommendations: {str(e)}"
        )

@router.get(
    "/job/{job_public_id}",
    response_model=List[JobMatchResponse],
    summary="Get all matches for a job",
    description="Retrieve all resume matches for a specific job, sorted by match score."
)
def get_job_matches_api(
    job_public_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all matches for a specific job."""
    service = JobMatchService(db)
    try:
        return service.get_job_matches(job_public_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve matches: {str(e)}"
        )

@router.get(
    "/{resume_public_id}/{job_public_id}",
    response_model=JobMatchResponse,
    summary="Get a specific match",
    description="Retrieve a specific job match by resume and job public IDs."
)
def get_match_api(
    resume_public_id: str,
    job_public_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific match between resume and job."""
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
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve match: {str(e)}"
        )

@router.post(
    "/generate/{resume_public_id}/{job_public_id}",
    response_model=JobMatchResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate a comprehensive job match",
    description="Generate a full match analysis including skills, experience, education, projects, and semantic matching."
)
def generate_match_api(
    resume_public_id: str,
    job_public_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generate a comprehensive match between resume and job with all analysis components."""
    service = JobMatchService(db)
    try:
        return service.generate_skill_match(
            resume_public_id=resume_public_id,
            job_public_id=job_public_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate match: {str(e)}"
        )

@router.get(
    "/recommendations/{resume_public_id}",
    response_model=List[JobRecommendation],
    summary="Get job recommendations",
    description="Get personalized job recommendations for a resume based on comprehensive matching analysis."
)
def get_job_recommendations_api(
    resume_public_id: str,
    top_n: int = Query(10, ge=1, le=50, description="Number of recommendations to return (1-50)"),
    min_match: float = Query(None, ge=0, le=100, description="Minimum match score threshold (0-100)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get job recommendations for a resume sorted by match score."""
    service = JobMatchService(db)
    try:
        return service.get_job_recommendations(
            resume_public_id=resume_public_id,
            top_n=top_n,
            min_match=min_match,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate recommendations: {str(e)}"
        )
