from sqlalchemy.orm import Session
from typing import Any

from app.matching.skill_matcher import SkillMatcher
from app.matching.experience_matcher import ExperienceMatcher
from app.matching.education_matcher import EducationMatcher
from app.matching.project_matcher import ProjectMatcher
from app.matching.semantic_matcher import SemanticMatcher
from app.matching.overall_matcher import OverallMatcher
from app.matching.recommendation_engine import RecommendationEngine
from app.models.job_match import JobMatch
from app.repositories.job import job_repository
from app.repositories.job_match import job_match_repository
from app.repositories.resume import resume_repository
from app.repositories.resume_analysis import resume_analysis_repository
from app.repositories.ats_score import ats_score_repository
from app.services.base import BaseService


class JobMatchService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db)

    def create_match(
        self,
        resume_public_id: str,
        job_public_id: str,
        **match_data,
    ) -> JobMatch:
        resume = resume_repository.get_by_public_id(self.db, resume_public_id)
        if not resume:
            raise ValueError("Resume not found.")

        job = job_repository.get_by_public_id(self.db, job_public_id)
        if not job:
            raise ValueError("Job not found.")

        if job_match_repository.match_exists(self.db, resume.id, job.id):
            raise ValueError("Match already exists.")

        skills = match_data.pop("skills", None)
        if skills:
            if isinstance(skills, dict):
                match_data["matched_skills"] = skills.get("matched", [])
                match_data["missing_skills"] = skills.get("missing", [])
            else:
                match_data["matched_skills"] = skills.matched
                match_data["missing_skills"] = skills.missing

        return job_match_repository.create(
            self.db,
            resume_id=resume.id,
            job_id=job.id,
            **match_data,
        )

    def get_match(
        self,
        resume_public_id: str,
        job_public_id: str,
    ) -> JobMatch | None:

        resume = resume_repository.get_by_public_id(
            self.db,
            resume_public_id,
        )

        if not resume:
            raise ValueError("Resume not found.")

        job = job_repository.get_by_public_id(
            self.db,
            job_public_id,
        )

        if not job:
            raise ValueError("Job not found.")

        return job_match_repository.get_resume_job_match(
            self.db,
            resume.id,
            job.id,
        )

    def get_resume_matches(
        self,
        resume_public_id: str,
    ) -> list[JobMatch]:

        resume = resume_repository.get_by_public_id(
            self.db,
            resume_public_id,
        )

        if not resume:
            raise ValueError("Resume not found.")

        return job_match_repository.get_by_resume(
            self.db,
            resume.id,
        )

    def get_job_matches(
        self,
        job_public_id: str,
    ) -> list[JobMatch]:

        job = job_repository.get_by_public_id(
            self.db,
            job_public_id,
        )

        if not job:
            raise ValueError("Job not found.")

        return job_match_repository.get_by_job(
            self.db,
            job.id,
        )

    def get_top_matches(
        self,
        limit: int = 10,
    ) -> list[JobMatch]:

        return job_match_repository.get_top_matches(
            self.db,
            limit,
        )

    def generate_skill_match(
        self,
        resume_public_id: str,
        job_public_id: str,
    ) -> JobMatch:
        """
        Generate a skill-based match between resume and job.

        Args:
            resume_public_id: Public ID of the resume
            job_public_id: Public ID of the job

        Returns:
            Created JobMatch with skill comparison results
        """
        resume = resume_repository.get_by_public_id(self.db, resume_public_id)
        if not resume:
            raise ValueError("Resume not found.")

        job = job_repository.get_by_public_id(self.db, job_public_id)
        if not job:
            raise ValueError("Job not found.")

        if job_match_repository.match_exists(self.db, resume.id, job.id):
            raise ValueError("Match already exists.")

        # Get resume skills from resume analysis
        resume_analysis = resume_analysis_repository.get_by_resume(self.db, resume.id)
        if not resume_analysis:
            raise ValueError("Resume analysis not found. Please analyze the resume first.")

        resume_skills = resume_analysis.skills or []
        resume_experience = resume_analysis.experience or []
        resume_education = resume_analysis.education or []
        resume_projects = resume_analysis.projects or []
        resume_raw_text = resume_analysis.raw_text or ""

        # Get ATS score for this resume
        ats_analysis = ats_score_repository.get_by_resume(self.db, resume.id)
        ats_score = ats_analysis.overall_score if ats_analysis else None

        # Get job required skills (use parsed data if available, otherwise use required_skills field)
        job_required_skills = job.parsed_required_skills if job.parsed_required_skills else job.required_skills
        job_preferred_skills = job.parsed_preferred_skills if job.parsed_preferred_skills else []
        job_experience = job.parsed_required_experience if job.parsed_required_experience else job.experience
        job_education = job.parsed_required_education if job.parsed_required_education else job.education
        job_description = job.description or ""

        # Perform skill comparison
        skill_comparison = SkillMatcher.compare_skills(
            resume_skills=resume_skills,
            required_skills=job_required_skills or [],
            preferred_skills=job_preferred_skills or [],
        )

        # Perform experience comparison
        experience_comparison = ExperienceMatcher.compare_experience(
            resume_experience=resume_experience,
            job_experience=job_experience,
        )

        # Perform education comparison
        education_comparison = EducationMatcher.compare_education(
            resume_education=resume_education,
            job_education=job_education,
        )

        # Perform project comparison
        project_comparison = ProjectMatcher.compare_projects(
            resume_projects=resume_projects,
            job_required_skills=job_required_skills or [],
        )

        # Perform semantic comparison (optional, if both texts are available)
        semantic_score = None
        semantic_strengths = None
        semantic_weaknesses = None
        semantic_reason = None

        if resume_raw_text and job_description:
            try:
                extracted_data = {
                    "skills": resume_skills,
                    "experience": resume_experience,
                    "education": resume_education,
                    "projects": resume_projects,
                }
                semantic_comparison = SemanticMatcher.compare_semantic(
                    job_description=job_description,
                    resume_text=resume_raw_text,
                    extracted_data=extracted_data,
                )
                semantic_score = semantic_comparison["semantic_score"]
                semantic_strengths = semantic_comparison["strengths"]
                semantic_weaknesses = semantic_comparison["weaknesses"]
                semantic_reason = semantic_comparison["reason"]
            except Exception:
                # Semantic matching failed, continue without it
                pass

        # Calculate overall match score using OverallMatcher
        overall_result = OverallMatcher.calculate_overall_score(
            skill_score=skill_comparison["skill_match_score"],
            experience_score=experience_comparison["experience_match_score"],
            education_score=education_comparison["education_match_score"],
            project_score=project_comparison["project_match_score"],
            semantic_score=semantic_score,
            ats_score=ats_score,
        )

        overall_score = int(overall_result["overall_match"])
        match_level = overall_result["match_level"]

        # Generate recommendation using match level
        if skill_comparison["missing_required_skills"]:
            recommendation = f"{match_level}. Missing skills: {', '.join(skill_comparison['missing_required_skills'][:3])}"
        else:
            recommendation = f"{match_level}. All required skills matched."

        # Create the match record with detailed analysis
        return job_match_repository.create_skill_match(
            self.db,
            resume_id=resume.id,
            job_id=job.id,
            match_score=overall_score,  # Use overall score from OverallMatcher
            matched_skills=skill_comparison["matched_required_skills"],
            missing_skills=skill_comparison["missing_required_skills"],
            matched_preferred_skills=skill_comparison["matched_preferred_skills"],
            extra_skills=skill_comparison["extra_skills"],
            skill_match_breakdown=skill_comparison["skill_match_breakdown"],
            candidate_years=int(experience_comparison["candidate_years"]),
            required_min_years=experience_comparison["required_min_years"],
            required_max_years=experience_comparison["required_max_years"],
            experience_match_score=experience_comparison["experience_match_score"],
            experience_match_breakdown=experience_comparison["experience_breakdown"],
            candidate_degree=education_comparison["candidate_degree"],
            candidate_level=education_comparison["candidate_level"],
            required_degree=education_comparison["required_degree"],
            required_level=education_comparison["required_level"],
            education_match_score=education_comparison["education_match_score"],
            education_match_breakdown=education_comparison["education_breakdown"],
            has_projects=project_comparison["has_projects"],
            relevant_projects_count=project_comparison["relevant_projects_count"],
            total_projects_count=project_comparison["total_projects_count"],
            project_match_score=project_comparison["project_match_score"],
            project_match_breakdown=project_comparison["project_breakdown"],
            semantic_score=semantic_score,
            semantic_strengths=semantic_strengths,
            semantic_weaknesses=semantic_weaknesses,
            semantic_reason=semantic_reason,
            overall_match=overall_score,
            match_level=match_level,
            skill_match_score=int(skill_comparison["skill_match_score"]),
            experience_match_score=int(experience_comparison["experience_match_score"]),
            education_match_score=int(education_comparison["education_match_score"]),
            project_match_score=int(project_comparison["project_match_score"]),
            semantic_match_score=int(semantic_score) if semantic_score else None,
            ats_score=int(ats_score) if ats_score else None,
            recommendation=recommendation,
        )

    def match_resume_to_jobs(
        self,
        resume_public_id: str,
    ) -> list[JobMatch]:
        """
        Match a resume against all open jobs.

        Args:
            resume_public_id: Public ID of the resume

        Returns:
            List of JobMatch objects sorted by match score
        """
        resume = resume_repository.get_by_public_id(self.db, resume_public_id)
        if not resume:
            raise ValueError("Resume not found.")

        # Get all open jobs
        open_jobs = job_repository.get_open_jobs(self.db)

        matches = []
        for job in open_jobs:
            try:
                match = self.generate_skill_match(
                    resume_public_id=resume_public_id,
                    job_public_id=str(job.public_id),
                )
                matches.append(match)
            except ValueError:
                # Skip if match already exists or other error
                continue

        # Sort by match score descending
        matches.sort(key=lambda m: m.match_score, reverse=True)

        return matches

    def match_job_to_resumes(
        self,
        job_public_id: str,
    ) -> list[JobMatch]:
        """
        Match a job against all resumes.

        Args:
            job_public_id: Public ID of the job

        Returns:
            List of JobMatch objects sorted by match score
        """
        job = job_repository.get_by_public_id(self.db, job_public_id)
        if not job:
            raise ValueError("Job not found.")

        # Get all resumes with analysis
        all_resumes = resume_repository.get_all(self.db)

        matches = []
        for resume in all_resumes:
            resume_analysis = resume_analysis_repository.get_by_resume(self.db, resume.id)
            if not resume_analysis:
                continue  # Skip resumes without analysis

            try:
                match = self.generate_skill_match(
                    resume_public_id=str(resume.public_id),
                    job_public_id=job_public_id,
                )
                matches.append(match)
            except ValueError:
                # Skip if match already exists or other error
                continue

        # Sort by match score descending
        matches.sort(key=lambda m: m.match_score, reverse=True)

        return matches

    def get_job_recommendations(
        self,
        resume_public_id: str,
        top_n: int = 10,
        min_match: float | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get job recommendations for a resume.

        Args:
            resume_public_id: Public ID of the resume
            top_n: Number of top recommendations to return
            min_match: Minimum match score threshold (optional)

        Returns:
            List of job recommendations sorted by match score
        """
        resume = resume_repository.get_by_public_id(self.db, resume_public_id)
        if not resume:
            raise ValueError("Resume not found.")

        # Get resume analysis
        resume_analysis = resume_analysis_repository.get_by_resume(self.db, resume.id)
        if not resume_analysis:
            raise ValueError("Resume analysis not found. Please analyze the resume first.")

        # Get all open jobs
        open_jobs = job_repository.get_open_jobs(self.db)

        # Get ATS score
        ats_analysis = ats_score_repository.get_by_resume(self.db, resume.id)
        ats_score = ats_analysis.overall_score if ats_analysis else None

        # Generate recommendations
        recommendations = RecommendationEngine.generate_recommendations(
            resume_skills=resume_analysis.skills or [],
            resume_experience=resume_analysis.experience or [],
            resume_education=resume_analysis.education or [],
            resume_projects=resume_analysis.projects or [],
            resume_raw_text=resume_analysis.raw_text or "",
            ats_score=ats_score,
            jobs=open_jobs,
            top_n=top_n,
            min_match=min_match,
        )

        return recommendations


job_match_service = JobMatchService