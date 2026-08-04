from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.repositories.resume import resume_repository
from app.repositories.resume_analysis import resume_analysis_repository
from app.schemas.ats_score import ATSScoreResponse
from app.services.ats_score import ATSScoreService

router = APIRouter(
    prefix="/ats-score",
    tags=["ATS Score"]
)


class ATSScoreCreateRequest(BaseModel):
    overall_score: float
    skills_score: float
    education_score: float
    experience_score: float
    projects_score: float
    format_score: float
    keyword_score: float
    missing_keywords: list[str] | None = None


@router.post("/{public_id}", response_model=ATSScoreResponse)
def create_ats_score(
    public_id: str,
    score_data: ATSScoreCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create an ATS score for a resume analysis.
    
    This endpoint calculates and stores the ATS score based on various criteria
    including skills, education, experience, projects, format, and keyword matching.
    """
    resume = resume_repository.get_by_public_id(db, public_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found.")
    
    if resume.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized to access this resume.")
    
    resume_analysis = resume_analysis_repository.get_by_resume(db, resume.id)
    if not resume_analysis:
        raise HTTPException(status_code=404, detail="Resume analysis not found. Please analyze the resume first.")
    
    service = ATSScoreService(db)
    
    try:
        score = service.generate_score(
            resume_analysis_public_id=str(resume_analysis.public_id),
            overall_score=score_data.overall_score,
            skills_score=score_data.skills_score,
            education_score=score_data.education_score,
            experience_score=score_data.experience_score,
            projects_score=score_data.projects_score,
            format_score=score_data.format_score,
            keyword_score=score_data.keyword_score,
            missing_keywords=score_data.missing_keywords,
        )
        return score
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{public_id}", response_model=ATSScoreResponse)
def get_ats_score(
    public_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get an ATS score by its public ID.
    """
    service = ATSScoreService(db)
    
    try:
        score = service.get_score(public_id)
        return score
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{public_id}", response_model=ATSScoreResponse)
def update_ats_score(
    public_id: str,
    score_data: ATSScoreCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update an existing ATS score.
    """
    service = ATSScoreService(db)
    
    try:
        score = service.update_score(
            public_id=public_id,
            overall_score=score_data.overall_score,
            skills_score=score_data.skills_score,
            education_score=score_data.education_score,
            experience_score=score_data.experience_score,
            projects_score=score_data.projects_score,
            format_score=score_data.format_score,
            keyword_score=score_data.keyword_score,
            missing_keywords=score_data.missing_keywords,
        )
        return score
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{public_id}")
def delete_ats_score(
    public_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete an ATS score.
    """
    service = ATSScoreService(db)
    
    try:
        service.delete_score(public_id)
        return {"success": True, "message": "ATS score deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
