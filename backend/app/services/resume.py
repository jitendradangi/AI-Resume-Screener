from sqlalchemy.orm import Session

from app.models.resume import Resume
from app.repositories.resume import resume_repository
from app.repositories.user import user_repository
from app.repositories.resume_analysis import resume_analysis_repository
from app.services.base import BaseService
from pathlib import Path
from app.parsers.resume_parser import ResumeParser
from app.ai.resume_analyzer import ResumeAnalyzer



class ResumeService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db)

    def create_resume(
        self,
        user_public_id: str,
        filename: str,
        original_filename: str,
        filepath: str,
        filetype: str,
        filesize: int,
    ) -> Resume:
        user = user_repository.get_by_public_id(self.db, user_public_id)
        if not user:
            raise ValueError("User not found.")

        return resume_repository.create(
            self.db,
            user_id=user.id,
            filename=filename,
            original_filename=original_filename,
            filepath=filepath,
            filetype=filetype,
            filesize=filesize,
        )

    def update_resume(
        self,
        public_id: str,
        filename: str,
        original_filename: str,
        filepath: str,
        filetype: str,
        filesize: int,
        user_id: int,
    ) -> Resume:
        resume = resume_repository.get_by_public_id(self.db, public_id)
        if not resume:
            raise ValueError("Resume not found.")
        if resume.user_id != user_id:
            raise PermissionError("Unauthorized to update this resume.")

        import os
        if resume.filepath and os.path.exists(resume.filepath):
            try:
                os.remove(resume.filepath)
            except Exception:
                pass

        from app.models.enums import ProcessingStatus
        from datetime import datetime, UTC
        return resume_repository.update(
            self.db,
            resume,
            filename=filename,
            original_filename=original_filename,
            filepath=filepath,
            filetype=filetype,
            filesize=filesize,
            processing_status=ProcessingStatus.PENDING,
            processing_error=None,
            updated_at=datetime.now(UTC),
        )

    def delete_resume(
        self,
        public_id: str,
        user_id: int,
    ) -> None:
        resume = resume_repository.get_by_public_id(self.db, public_id)
        if not resume:
            raise ValueError("Resume not found.")
        if resume.user_id != user_id:
            raise PermissionError("Unauthorized to delete this resume.")
        
        import os
        if resume.filepath and os.path.exists(resume.filepath):
            try:
                os.remove(resume.filepath)
            except Exception:
                pass

        resume_repository.delete(self.db, resume)

    def get_resume(
        self,
        public_id: str,
    ) -> Resume | None:
        return resume_repository.get_by_public_id(
            self.db,
            public_id,
        )

    def get_user_resumes(
        self,
        user_public_id: str,
    ) -> list[Resume]:

        user = user_repository.get_by_public_id(
            self.db,
            user_public_id,
        )

        if not user:
            raise ValueError("User not found.")

        return resume_repository.get_by_user(
            self.db,
            user.id,
        )

    def get_latest_resume(
        self,
        user_public_id: str,
    ) -> Resume | None:

        user = user_repository.get_by_public_id(
            self.db,
            user_public_id,
        )

        if not user:
            raise ValueError("User not found.")

        return resume_repository.get_latest_by_user(
            self.db,
            user.id,
        )

    def parse_resume(
        self,
        public_id: str,
    ) -> str:

      resume = self.get_resume(public_id)

      if resume is None:
        raise ValueError("Resume not found.")

      extracted_text = ResumeParser.parse(resume.filepath)

      return extracted_text

    def parse_resume_sections(
        self,
        public_id: str,
    ) -> dict:
        resume = self.get_resume(public_id)
        if resume is None:
            raise ValueError("Resume not found.")

        extracted_text = ResumeParser.parse(resume.filepath)
        from app.parsers.section_parse import SectionParser
        return SectionParser.parse_sections(extracted_text)

    def extract_resume_information(
        self,
        public_id: str,
    ) -> dict:
        """
        Parse the resume file and return fully structured JSON data covering
        skills, education, experience, projects, certifications, and languages.
        """
        resume = self.get_resume(public_id)
        if resume is None:
            raise ValueError("Resume not found.")

        extracted_text = ResumeParser.parse(resume.filepath)
        from app.parsers.information_extractor import InformationExtractor
        return InformationExtractor.extract_resume_data(extracted_text)

    def analyze_resume(
        self,
        public_id: str,
    ) -> dict:
        """
        Parse the resume file, extract structured information, and persist it to the database.
        Returns the analysis data including the public_id of the analysis.
        """
        resume = self.get_resume(public_id)
        if resume is None:
            raise ValueError("Resume not found.")

        extracted_text = ResumeParser.parse(resume.filepath)
        from app.parsers.information_extractor import InformationExtractor
        parsed_data = InformationExtractor.extract_resume_data(extracted_text)

        existing_analysis = resume_analysis_repository.get_by_resume(self.db, resume.id)

        if existing_analysis:
            analysis = resume_analysis_repository.update_analysis(
                self.db,
                existing_analysis,
                raw_text=extracted_text,
                parsed_data=parsed_data,
                summary=parsed_data.get("summary"),
                skills=parsed_data.get("skills"),
                education=parsed_data.get("education"),
                experience=parsed_data.get("experience"),
                projects=parsed_data.get("projects"),
                certifications=parsed_data.get("certifications"),
                languages=parsed_data.get("languages"),
            )
        else:
            analysis = resume_analysis_repository.create_analysis(
                self.db,
                resume_id=resume.id,
                raw_text=extracted_text,
                parsed_data=parsed_data,
                summary=parsed_data.get("summary"),
                skills=parsed_data.get("skills"),
                education=parsed_data.get("education"),
                experience=parsed_data.get("experience"),
                projects=parsed_data.get("projects"),
                certifications=parsed_data.get("certifications"),
                languages=parsed_data.get("languages"),
            )

        return {
            "public_id": str(analysis.public_id),
            "resume_public_id": public_id,
            "data": parsed_data,
        }

    def run_ai_analysis(
        self,
        public_id: str,
    ) -> dict:
        """
        Step 6 – Gemini AI analysis flow:
          1. Parse the resume file to extract raw text.
          2. Run InformationExtractor to build structured data.
          3. Call ResumeAnalyzer.analyze_resume() → Gemini prompt + JSON parse.
          4. Upsert the AI result into the resume_analysis.ai_analysis column.

        Returns a dict with:
          - analysis_public_id : str  – public_id of the ResumeAnalysis row
          - resume_public_id   : str  – the resume's public_id
          - ai_analysis        : dict – full Gemini response (score, strengths, …)
        """
        resume = self.get_resume(public_id)
        if resume is None:
            raise ValueError("Resume not found.")

        # 1. Parse raw text
        extracted_text = ResumeParser.parse(resume.filepath)

        # 2. Extract structured information
        from app.parsers.information_extractor import InformationExtractor
        parsed_data = InformationExtractor.extract_resume_data(extracted_text)

        # 3. Call Gemini (Step 4 prompt → Step 5 JSON parse)
        ai_result = ResumeAnalyzer.analyze_resume(extracted_text, parsed_data)

        # 4. Upsert into DB
        existing_analysis = resume_analysis_repository.get_by_resume(self.db, resume.id)

        if existing_analysis:
            analysis = resume_analysis_repository.update_analysis(
                self.db,
                existing_analysis,
                # Keep parsed fields up-to-date too
                raw_text=extracted_text,
                parsed_data=parsed_data,
                summary=parsed_data.get("summary"),
                skills=parsed_data.get("skills"),
                education=parsed_data.get("education"),
                experience=parsed_data.get("experience"),
                projects=parsed_data.get("projects"),
                certifications=parsed_data.get("certifications"),
                languages=parsed_data.get("languages"),
                ai_analysis=ai_result,
            )
        else:
            analysis = resume_analysis_repository.create_analysis(
                self.db,
                resume_id=resume.id,
                raw_text=extracted_text,
                parsed_data=parsed_data,
                summary=parsed_data.get("summary"),
                skills=parsed_data.get("skills"),
                education=parsed_data.get("education"),
                experience=parsed_data.get("experience"),
                projects=parsed_data.get("projects"),
                certifications=parsed_data.get("certifications"),
                languages=parsed_data.get("languages"),
                ai_analysis=ai_result,
            )

        return {
            "analysis_public_id": str(analysis.public_id),
            "resume_public_id": public_id,
            "ai_analysis": ai_result,
        }


resume_service = ResumeService