"""
Recommendation Engine – Sprint 9 Task 9
======================================
Calculates match scores for all available jobs and returns top recommendations.
"""

from typing import Any, List


class RecommendationEngine:
    """Generates job recommendations based on resume-job matching."""

    @staticmethod
    def generate_recommendations(
        resume_skills: list[str],
        resume_experience: list,
        resume_education: list,
        resume_projects: list,
        resume_raw_text: str,
        ats_score: float | None,
        jobs: List[Any],
        top_n: int = 10,
        min_match: float | None = None,
    ) -> List[dict[str, Any]]:
        """
        Generate job recommendations by matching resume against all jobs.

        Args:
            resume_skills: List of skills from resume
            resume_experience: List of experience entries from resume
            resume_education: List of education entries from resume
            resume_projects: List of projects from resume
            resume_raw_text: Raw resume text
            ats_score: ATS quality score (optional)
            jobs: List of job objects
            top_n: Number of top recommendations to return
            min_match: Minimum match score threshold (optional)

        Returns:
            List of job recommendations sorted by match score:
                - job: Job object
                - job_public_id: Job public ID
                - title: Job title
                - company: Company name
                - location: Job location
                - overall_match: Overall match score
                - match_level: Match level
                - component_scores: Component score breakdown
        """
        from app.matching.skill_matcher import SkillMatcher
        from app.matching.experience_matcher import ExperienceMatcher
        from app.matching.education_matcher import EducationMatcher
        from app.matching.project_matcher import ProjectMatcher
        from app.matching.overall_matcher import OverallMatcher

        recommendations = []

        for job in jobs:
            # Get job requirements
            job_required_skills = job.parsed_required_skills if job.parsed_required_skills else job.required_skills
            job_preferred_skills = job.parsed_preferred_skills if job.parsed_preferred_skills else []
            job_experience = job.parsed_required_experience if job.parsed_required_experience else job.experience
            job_education = job.parsed_required_education if job.parsed_required_education else job.education
            job_description = job.description or ""

            # Calculate component scores
            skill_comparison = SkillMatcher.compare_skills(
                resume_skills=resume_skills,
                required_skills=job_required_skills or [],
                preferred_skills=job_preferred_skills or [],
            )

            experience_comparison = ExperienceMatcher.compare_experience(
                resume_experience=resume_experience,
                job_experience=job_experience,
            )

            education_comparison = EducationMatcher.compare_education(
                resume_education=resume_education,
                job_education=job_education,
            )

            project_comparison = ProjectMatcher.compare_projects(
                resume_projects=resume_projects,
                job_required_skills=job_required_skills or [],
            )

            # Calculate overall score
            overall_result = OverallMatcher.calculate_overall_score(
                skill_score=skill_comparison["skill_match_score"],
                experience_score=experience_comparison["experience_match_score"],
                education_score=education_comparison["education_match_score"],
                project_score=project_comparison["project_match_score"],
                semantic_score=None,  # Skip semantic for bulk recommendations (performance)
                ats_score=ats_score,
            )

            # Apply minimum match filter
            if min_match is not None and overall_result["overall_match"] < min_match:
                continue

            recommendations.append({
                "job": job,
                "job_public_id": str(job.public_id),
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "overall_match": overall_result["overall_match"],
                "match_level": overall_result["match_level"],
                "component_scores": {
                    "skills": skill_comparison["skill_match_score"],
                    "experience": experience_comparison["experience_match_score"],
                    "education": education_comparison["education_match_score"],
                    "projects": project_comparison["project_match_score"],
                    "ats": ats_score,
                },
                "matched_skills": skill_comparison["matched_required_skills"],
                "missing_skills": skill_comparison["missing_required_skills"],
            })

        # Sort by overall match score (descending)
        recommendations.sort(key=lambda x: x["overall_match"], reverse=True)

        # Return top N
        return recommendations[:top_n]

    @staticmethod
    def get_recommendation_summary(recommendations: List[dict[str, Any]]) -> dict[str, Any]:
        """
        Generate a summary of the recommendations.

        Args:
            recommendations: List of job recommendations

        Returns:
            Dict with summary statistics
        """
        if not recommendations:
            return {
                "total_jobs": 0,
                "recommended_jobs": 0,
                "avg_match": 0,
                "highest_match": 0,
                "lowest_match": 0,
            }

        total_jobs = len(recommendations)
        matches = [r["overall_match"] for r in recommendations]

        return {
            "total_jobs": total_jobs,
            "recommended_jobs": total_jobs,
            "avg_match": round(sum(matches) / total_jobs, 1) if total_jobs > 0 else 0,
            "highest_match": max(matches) if matches else 0,
            "lowest_match": min(matches) if matches else 0,
        }

