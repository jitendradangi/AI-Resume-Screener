from sqlalchemy.orm import Session

from app.ats.education_scorer import EducationScorer
from app.ats.experience_scorer import ExperienceScorer
from app.ats.format_scorer import FormatScorer
from app.ats.keyword_extractor import KeywordExtractor
from app.ats.overall_scorer import OverallScorer
from app.ats.project_scorer import ProjectScorer
from app.ats.section_scorer import SectionScorer
from app.ats.skill_scorer import SkillScorer
from app.models.ats_score import ATSScore
from app.repositories.ats_score import ats_score_repository
from app.repositories.resume_analysis import resume_analysis_repository
from app.services.base import BaseService


class ATSScoreService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db)

    def generate_score(
        self,
        resume_analysis_public_id: str,
        overall_score: float,
        skills_score: float,
        education_score: float,
        experience_score: float,
        projects_score: float,
        format_score: float,
        section_score: float,
        keyword_score: float,
        missing_keywords: list | None = None,
        strengths: list | None = None,
        weaknesses: list | None = None,
        recommendations: list | None = None,
    ) -> ATSScore:
        """
        Generate ATS score with manual score inputs.

        Args:
            resume_analysis_public_id: Public ID of the resume analysis
            overall_score: Overall ATS score (0-100)
            skills_score: Skills score (0-100)
            education_score: Education score (0-100)
            experience_score: Experience score (0-100)
            projects_score: Projects score (0-100)
            format_score: Format score (0-100)
            section_score: Section score (0-100)
            keyword_score: Keyword score (0-100)
            missing_keywords: List of missing keywords
            strengths: List of strengths
            weaknesses: List of weaknesses
            recommendations: List of recommendations

        Returns:
            Created ATSScore
        """
        resume_analysis = resume_analysis_repository.get_by_public_id(
            self.db,
            resume_analysis_public_id,
        )
        if not resume_analysis:
            raise ValueError("Resume analysis not found.")

        if ats_score_repository.score_exists(self.db, resume_analysis.id):
            raise ValueError("ATS score already exists for this resume analysis.")

        return ats_score_repository.create_score(
            self.db,
            resume_analysis_id=resume_analysis.id,
            overall_score=overall_score,
            skills_score=skills_score,
            education_score=education_score,
            experience_score=experience_score,
            projects_score=projects_score,
            format_score=format_score,
            section_score=section_score,
            keyword_score=keyword_score,
            missing_keywords=missing_keywords,
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations,
        )

    def generate_score_auto(
        self,
        resume_analysis_public_id: str,
        experience_score: float,
        projects_score: float,
        format_score: float,
        section_score: float,
    ) -> ATSScore:
        """
        Generate ATS score with automatic resume quality analysis.

        Automatically calculates skills, keyword, and education scores based on resume quality.
        Experience, projects, format, and section scores are provided manually.

        Args:
            resume_analysis_public_id: Public ID of the resume analysis
            experience_score: Manual experience score (0-100)
            projects_score: Manual projects score (0-100)
            format_score: Manual format score (0-100)
            section_score: Manual section score (0-100)

        Returns:
            Created ATSScore with skills, keyword, and education scores calculated automatically
        """
        resume_analysis = resume_analysis_repository.get_by_public_id(
            self.db,
            resume_analysis_public_id,
        )
        if not resume_analysis:
            raise ValueError("Resume analysis not found.")

        if ats_score_repository.score_exists(self.db, resume_analysis.id):
            raise ValueError("ATS score already exists for this resume analysis.")

        # Build resume analysis dict for analysis
        resume_analysis_dict = {
            "skills": resume_analysis.skills or [],
            "experience": resume_analysis.experience or [],
            "projects": resume_analysis.projects or [],
            "education": resume_analysis.education or [],
            "raw_text": resume_analysis.raw_text or "",
        }

        # Perform skill quality analysis
        skill_analysis = SkillScorer.get_skill_analysis(resume_analysis_dict)

        # Perform keyword quality analysis
        keyword_analysis = KeywordExtractor.get_keyword_analysis(resume_analysis_dict)

        # Perform education quality analysis
        education_analysis = EducationScorer.get_education_analysis(resume_analysis_dict)

        # Calculate overall score (weighted average)
        # Skills: 25%, Keyword: 20%, Education: 20%, Experience: 15%, Projects: 10%, Format: 5%, Section: 5%
        overall_score = (
            skill_analysis["overall_skills_score"] * 0.25 +
            keyword_analysis["overall_keyword_score"] * 0.20 +
            education_analysis["overall_education_score"] * 0.20 +
            experience_score * 0.15 +
            projects_score * 0.10 +
            format_score * 0.05 +
            section_score * 0.05
        )

        return ats_score_repository.create_score(
            self.db,
            resume_analysis_id=resume_analysis.id,
            overall_score=round(overall_score, 2),
            skills_score=skill_analysis["overall_skills_score"],
            education_score=education_analysis["overall_education_score"],
            experience_score=experience_score,
            projects_score=projects_score,
            format_score=format_score,
            section_score=section_score,
            keyword_score=keyword_analysis["overall_keyword_score"],
            missing_keywords=None,  # No missing keywords in resume quality mode
            strengths=None,
            weaknesses=None,
            recommendations=None,
        )

    def generate_report(
        self,
        resume_analysis_public_id: str,
    ) -> ATSScore:
        """
        Generate ATS report with all individual scores calculated.

        This method implements the complete Sprint 8 ATS scoring system.
        All individual scorers are implemented: format, section, experience, education, skills, keyword, and projects.

        Args:
            resume_analysis_public_id: Public ID of the resume analysis

        Returns:
            Created ATSScore with all individual scores calculated
        """
        resume_analysis = resume_analysis_repository.get_by_public_id(
            self.db,
            resume_analysis_public_id,
        )
        if not resume_analysis:
            raise ValueError("Resume analysis not found.")

        if ats_score_repository.score_exists(self.db, resume_analysis.id):
            raise ValueError("ATS score already exists for this resume analysis.")

        # Build resume analysis dict for analysis
        resume_analysis_dict = {
            "skills": resume_analysis.skills or [],
            "experience": resume_analysis.experience or [],
            "projects": resume_analysis.projects or [],
            "education": resume_analysis.education or [],
            "raw_text": resume_analysis.raw_text or "",
        }

        # Perform format analysis
        format_analysis = FormatScorer.get_format_analysis(resume_analysis_dict)

        # Perform section analysis
        section_analysis = SectionScorer.get_section_analysis(resume_analysis_dict)

        # Perform experience analysis
        experience_analysis = ExperienceScorer.get_experience_analysis(resume_analysis_dict)

        # Perform education analysis
        education_analysis = EducationScorer.get_education_analysis(resume_analysis_dict)

        # Perform skills analysis
        skills_analysis = SkillScorer.get_skill_analysis(resume_analysis_dict)

        # Perform keyword analysis
        keyword_analysis = KeywordExtractor.get_keyword_analysis(resume_analysis_dict)

        # Perform project analysis
        project_analysis = ProjectScorer.get_project_analysis(resume_analysis_dict)

        # Collect all issues and recommendations
        all_issues = []
        all_recommendations = []

        # Add education-specific feedback if no education
        if education_analysis.get("education_count", 0) == 0:
            all_issues.append("No education information provided")
            all_recommendations.append("Add education details with degree, institution, and field of study")

        # Add skills-specific feedback if no skills
        if skills_analysis.get("skill_count", 0) == 0:
            all_issues.append("No skills information provided")
            all_recommendations.append("Add a comprehensive skills section highlighting technical and soft skills")

        # Add project-specific feedback if no projects
        if project_analysis.get("overall_project_score", 0) == 0:
            all_recommendations.append("Consider adding a projects section to showcase your practical work and achievements")

        # Calculate overall score using OverallScorer
        overall_score = OverallScorer.calculate_overall_score(
            format_score=format_analysis["overall_format_score"],
            section_score=section_analysis["overall_section_score"],
            skills_score=skills_analysis["overall_skills_score"],
            experience_score=experience_analysis["overall_experience_score"],
            education_score=education_analysis["overall_education_score"],
            project_score=project_analysis["overall_project_score"],
            keyword_score=keyword_analysis["overall_keyword_score"],
        )

        if format_analysis.get("format_issues"):
            all_issues.extend(format_analysis["format_issues"])
        if section_analysis.get("section_issues"):
            all_issues.extend(section_analysis["section_issues"])
        if experience_analysis.get("experience_issues"):
            all_issues.extend(experience_analysis["experience_issues"])
        if project_analysis.get("project_issues"):
            all_issues.extend(project_analysis["project_issues"])

        if format_analysis.get("format_recommendations"):
            all_recommendations.extend(format_analysis["format_recommendations"])
        if section_analysis.get("section_recommendations"):
            all_recommendations.extend(section_analysis["section_recommendations"])
        if experience_analysis.get("experience_recommendations"):
            all_recommendations.extend(experience_analysis["experience_recommendations"])
        if project_analysis.get("project_recommendations"):
            all_recommendations.extend(project_analysis["project_recommendations"])

        # Remove duplicates while preserving order
        if all_issues:
            all_issues = list(dict.fromkeys(all_issues))
        if all_recommendations:
            all_recommendations = list(dict.fromkeys(all_recommendations))

        return ats_score_repository.create_score(
            self.db,
            resume_analysis_id=resume_analysis.id,
            overall_score=overall_score,
            skills_score=skills_analysis["overall_skills_score"],
            education_score=education_analysis["overall_education_score"],
            experience_score=experience_analysis["overall_experience_score"],
            projects_score=project_analysis["overall_project_score"],
            format_score=format_analysis["overall_format_score"],
            section_score=section_analysis["overall_section_score"],
            keyword_score=keyword_analysis["overall_keyword_score"],
            missing_keywords=None,
            strengths=None,
            weaknesses=all_issues if all_issues else None,
            recommendations=all_recommendations if all_recommendations else None,
        )

    def get_score(
        self,
        public_id: str,
    ) -> ATSScore | None:
        score = ats_score_repository.get_by_public_id(self.db, public_id)
        if not score:
            raise ValueError("ATS score not found.")
        return score

    def get_score_by_resume_analysis(
        self,
        resume_analysis_public_id: str,
    ) -> ATSScore | None:
        resume_analysis = resume_analysis_repository.get_by_public_id(
            self.db,
            resume_analysis_public_id,
        )
        if not resume_analysis:
            raise ValueError("Resume analysis not found.")

        score = ats_score_repository.get_by_resume_analysis(
            self.db,
            resume_analysis.id,
        )
        if not score:
            raise ValueError("ATS score not found for this resume analysis.")
        return score

    def get_report(
        self,
        resume_analysis_public_id: str,
    ) -> ATSScore | None:
        """
        Get ATS report by resume analysis public ID.

        Args:
            resume_analysis_public_id: Public ID of the resume analysis

        Returns:
            ATSScore if found, None otherwise
        """
        return self.get_score_by_resume_analysis(resume_analysis_public_id)

    def update_report(
        self,
        resume_analysis_public_id: str,
        **score_data,
    ) -> ATSScore:
        """
        Update ATS report by resume analysis public ID.

        Args:
            resume_analysis_public_id: Public ID of the resume analysis
            **score_data: Score fields to update

        Returns:
            Updated ATSScore
        """
        resume_analysis = resume_analysis_repository.get_by_public_id(
            self.db,
            resume_analysis_public_id,
        )
        if not resume_analysis:
            raise ValueError("Resume analysis not found.")

        score = ats_score_repository.get_by_resume_analysis(
            self.db,
            resume_analysis.id,
        )
        if not score:
            raise ValueError("ATS score not found for this resume analysis.")

        return ats_score_repository.update_score(
            self.db,
            score,
            **score_data,
        )

    def update_score(
        self,
        public_id: str,
        overall_score: float | None = None,
        skills_score: float | None = None,
        education_score: float | None = None,
        experience_score: float | None = None,
        projects_score: float | None = None,
        format_score: float | None = None,
        section_score: float | None = None,
        keyword_score: float | None = None,
        missing_keywords: list | None = None,
        strengths: list | None = None,
        weaknesses: list | None = None,
        recommendations: list | None = None,
    ) -> ATSScore:
        score = ats_score_repository.get_by_public_id(self.db, public_id)
        if not score:
            raise ValueError("ATS score not found.")

        return ats_score_repository.update_score(
            self.db,
            score,
            overall_score=overall_score,
            skills_score=skills_score,
            education_score=education_score,
            experience_score=experience_score,
            projects_score=projects_score,
            format_score=format_score,
            section_score=section_score,
            keyword_score=keyword_score,
            missing_keywords=missing_keywords,
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations,
        )

    def delete_score(
        self,
        public_id: str,
    ) -> None:
        score = ats_score_repository.get_by_public_id(self.db, public_id)
        if not score:
            raise ValueError("ATS score not found.")

        ats_score_repository.delete(self.db, score)


ats_score_service = ATSScoreService
