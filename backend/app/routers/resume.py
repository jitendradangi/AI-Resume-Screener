from pathlib import Path
import uuid
from typing import List

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.repositories.resume import resume_repository
from app.repositories.resume_analysis import resume_analysis_repository
from app.schemas.ats_score import ATSScoreResponse
from app.schemas.resume import ResumeResponse
from app.schemas.resume_analysis import AIAnalysisResponse
from app.services.ats_score import ATSScoreService
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


class ATSScoreCreateRequest(BaseModel):
    overall_score: float
    skills_score: float
    education_score: float
    experience_score: float
    projects_score: float
    format_score: float
    keyword_score: float
    missing_keywords: list[str] | None = None


class ATSScoreAutoRequest(BaseModel):
    experience_score: float
    projects_score: float
    format_score: float


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

@router.get("/{public_id}", response_model=ResumeResponse)
def get_resume_details(
    public_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    resume = service.get_resume(public_id=public_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    if resume.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized to access this resume")
    return resume

@router.put("/{public_id}", response_model=ResumeResponse)
async def update_resume_api(
    public_id: str,
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
    try:
        updated_resume = service.update_resume(
            public_id=public_id,
            filename=unique_filename,
            original_filename=file.filename,
            filepath=str(file_path),
            filetype=file.content_type or "application/octet-stream",
            filesize=len(content),
            user_id=current_user.id,
        )
        return updated_resume
    except PermissionError as e:
        if file_path.exists():
            try:
                file_path.unlink()
            except Exception:
                pass
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        if file_path.exists():
            try:
                file_path.unlink()
            except Exception:
                pass
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{public_id}")
def delete_resume_api(
    public_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    try:
        service.delete_resume(public_id=public_id, user_id=current_user.id)
        return {"success": True, "message": "Resume deleted successfully"}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{public_id}/parse")
def parse_resume(
    public_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    service = ResumeService(db)

    try:

        text = service.parse_resume(public_id)

        return {
            "success": True,
            "message": "Resume parsed successfully.",
            "text": text,
        }

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

@router.post("/{public_id}/sections")
def parse_resume_sections(
    public_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    service = ResumeService(db)

    try:

        sections = service.parse_resume_sections(public_id)

        return {
            "success": True,
            "sections": sections,
        }

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@router.post("/{public_id}/extract")
def extract_resume_information(
    public_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Extract structured information from a resume and return it as JSON.

    Returns:
        summary        - professional summary / objective text
        skills         - list of skill strings
        education      - list of {degree, institution, field, start, end, grade}
        experience     - list of {title, company, start, end, responsibilities}
        projects       - list of {name, description, technologies, start, end}
        certifications - list of {name, issuer, year}
        languages      - list of {language, proficiency}
        raw_sections   - raw section text blocks (for debugging)
    """

    service = ResumeService(db)

    try:
        resume = service.get_resume(public_id)
        if resume is None:
            raise ValueError("Resume not found.")

        if resume.user_id != current_user.id:
            raise PermissionError("Unauthorized to access this resume.")

        data = service.extract_resume_information(public_id)

        return {
            "success": True,
            "public_id": public_id,
            "data": data,
        }

    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{public_id}/analyze")
def analyze_resume(
    public_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Analyze a resume by extracting structured information and persisting it to the database.
    This endpoint parses the resume, extracts all relevant information, and stores it
    for reuse in ATS scoring and job matching.

    Returns:
        public_id - the public_id of the created/updated analysis
        resume_public_id - the public_id of the resume
        data - the extracted structured data
    """
    service = ResumeService(db)

    try:
        resume = service.get_resume(public_id)
        if resume is None:
            raise ValueError("Resume not found.")

        if resume.user_id != current_user.id:
            raise PermissionError("Unauthorized to access this resume.")

        result = service.analyze_resume(public_id)

        return {
            "success": True,
            "message": "Resume analyzed and persisted successfully.",
            "result": result,
        }

    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# Step 7 – AI analysis endpoint
# ---------------------------------------------------------------------------

@router.post(
    "/{public_id}/ai-analysis",
    response_model=AIAnalysisResponse,
    summary="Run Gemini AI analysis on a resume",
    description=(
        "Parses the resume file, extracts structured information, sends it to "
        "Gemini for a deep ATS-style evaluation, persists the result to the database, "
        "and returns the full AI analysis (score, strengths, weaknesses, …)."
    ),
)
def run_ai_analysis(
    public_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)

    # Ownership check
    resume = service.get_resume(public_id)
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found.")
    if resume.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized to access this resume.")

    try:
        result = service.run_ai_analysis(public_id)
        return AIAnalysisResponse.from_service_result(result)

    except (ValueError, RuntimeError) as e:
        raise HTTPException(status_code=422, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{public_id}/ats-score", response_model=ATSScoreResponse)
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


@router.post("/{public_id}/ats-score/auto", response_model=ATSScoreResponse)
def create_ats_score_auto(
    public_id: str,
    score_data: ATSScoreAutoRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create an ATS score with automatic resume quality analysis.
    
    Automatically calculates skills, keyword, and education scores based on resume quality.
    Experience, projects, and format scores are provided manually.
    """
    resume = resume_repository.get_by_public_id(db, public_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found.")
    if resume.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized.")
    
    resume_analysis = resume_analysis_repository.get_by_resume(db, resume.id)
    if not resume_analysis:
        raise HTTPException(status_code=404, detail="Resume analysis not found. Please analyze the resume first.")
    
    service = ATSScoreService(db)
    
    try:
        score = service.generate_score_auto(
            resume_analysis_public_id=str(resume_analysis.public_id),
            experience_score=score_data.experience_score,
            projects_score=score_data.projects_score,
            format_score=score_data.format_score,
        )
        return score
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
