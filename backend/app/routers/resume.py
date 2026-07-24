from pathlib import Path
import uuid
from typing import List

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.resume_service import resume_service
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.resume import ResumeResponse

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload", response_model=ResumeResponse)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = UPLOAD_DIR / unique_filename

    content = await file.read()
    with open(file_path, "wb") as buffer:
        buffer.write(content)

    resume = resume_service.create_resume(
       db=db,
       filename=unique_filename,
       original_filename=file.filename,
       filepath=str(file_path),
       filetype=file.content_type or "application/octet-stream",
       filesize=len(content),
       user_id=current_user.id,
    )

    return resume

@router.get(
    "/my-resumes",
    response_model=List[ResumeResponse]
)
def get_my_resumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return resume_service.get_user_resumes(
        db,
        current_user.id
    )

@router.delete("/{resume_id}")
def delete_resume_api(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return resume_service.delete_resume(
        db=db,
        resume_id=resume_id,
        user_id=current_user.id,
    )

