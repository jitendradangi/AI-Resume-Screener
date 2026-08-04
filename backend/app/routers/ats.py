from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.ats_score import ATSScoreResponse
from app.services.ats_score import ats_score_service

router = APIRouter(
    prefix="/resume",
    tags=["ATS Reports"]
)

@router.post("/{public_id}/ats", response_model=ATSScoreResponse, status_code=status.HTTP_201_CREATED)
def create_ats_report_api(
    public_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate ATS report for a resume analysis.
    All scores are initialized to 0.
    """
    service = ats_score_service(db)
    try:
        return service.generate_report(
            resume_analysis_public_id=public_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{public_id}/ats", response_model=ATSScoreResponse)
def get_ats_report_api(
    public_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get ATS report for a resume analysis.
    """
    service = ats_score_service(db)
    try:
        report = service.get_report(public_id)
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="ATS report not found"
            )
        return report
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.put("/{public_id}/ats", response_model=ATSScoreResponse)
def update_ats_report_api(
    public_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update ATS report for a resume analysis.
    This endpoint is a placeholder for future implementation.
    """
    service = ats_score_service(db)
    try:
        return service.update_report(
            resume_analysis_public_id=public_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
