from pathlib import Path
import uuid
from typing import List

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.resume import ResumeResponse
from app.services.resume import ResumeService

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}
ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


@router.post("/upload", response_model=ResumeResponse)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Validate file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type '{file_ext}'. Only .pdf, .doc, .docx files are allowed."
        )

    # Validate content type
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid content type '{file.content_type}'. Only PDF and Word documents are accepted."
        )

    content = await file.read()

    # Validate file size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File size {len(content) // 1024}KB exceeds the maximum allowed size of 5MB."
        )

    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = UPLOAD_DIR / unique_filename

    with open(file_path, "wb") as buffer:
        buffer.write(content)

    service = ResumeService(db)
    resume = service.create_resume(
        user_public_id=str(current_user.public_id),
        filename=unique_filename,
        original_filename=file.filename,
        filepath=str(file_path),
        filetype=file.content_type or "application/octet-stream",
        filesize=len(content),
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
    service = ResumeService(db)
    return service.get_user_resumes(user_public_id=str(current_user.public_id))

@router.delete("/{resume_id}")
def delete_resume_api(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    try:
        service.delete_resume(resume_id=resume_id, user_id=current_user.id)
        return {"success": True, "message": "Resume deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
