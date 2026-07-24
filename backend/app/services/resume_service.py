from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.resume import Resume
import os


class ResumeService:

    def create_resume(
        self,
        db: Session,
        filename: str,
        filepath: str,
        user_id: int,
    ):
        resume = Resume(
            filename=filename,
            filepath=filepath,
            user_id=user_id,
        )

        from app.services.resume_processing_service import ResumeProcessingService
        ResumeProcessingService.process(resume)

        db.add(resume)
        db.commit()
        db.refresh(resume)

        return resume

    def get_user_resumes(
        self,
        db: Session,
        user_id: int,
    ):
        return (
            db.query(Resume)
            .filter(Resume.user_id == user_id)
            .order_by(Resume.uploaded_at.desc())
            .all()
        )

    def delete_resume(
        self,
        db: Session,
        resume_id: int,
        user_id: int,
    ):
        resume = (
            db.query(Resume)
            .filter(
                Resume.id == resume_id,
                Resume.user_id == user_id,
            )
            .first()
        )

        if not resume:
            raise HTTPException(
                status_code=404,
                detail="Resume not found",
            )

        if os.path.exists(resume.filepath):
            os.remove(resume.filepath)

        db.delete(resume)
        db.commit()

        return {"message": "Resume deleted successfully"}
     
    
resume_service = ResumeService()

    