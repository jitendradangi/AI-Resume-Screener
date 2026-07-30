from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.ats_report import ATSReportCreate, ATSReportResponse
from app.services.ats_report import ATSReportService

router = APIRouter(
    prefix="/ats",
    tags=["ATS Reports"]
)

@router.post("/{resume_public_id}", response_model=ATSReportResponse, status_code=status.HTTP_201_CREATED)
def create_report_api(
    resume_public_id: str,
    report_in: ATSReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ATSReportService(db)
    try:
        return service.create_report(
            resume_public_id=resume_public_id,
            **report_in.model_dump()
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{resume_public_id}", response_model=ATSReportResponse)
def get_report_api(
    resume_public_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ATSReportService(db)
    try:
        report = service.get_report(resume_public_id)
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

@router.put("/{resume_public_id}", response_model=ATSReportResponse)
def update_report_api(
    resume_public_id: str,
    report_in: ATSReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ATSReportService(db)
    try:
        return service.update_report(
            resume_public_id=resume_public_id,
            **report_in.model_dump(exclude_unset=True)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
