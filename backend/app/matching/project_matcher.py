"""
Project Matcher – Job-Resume Project Compatibility Analysis
==========================================================
Compares candidate projects with job requirements.
Evaluates technology stack, relevance, and project quality.
"""

from typing import Any


class ProjectMatcher:
    """Analyzes project compatibility between resumes and job requirements."""

    @staticmethod
    def extract_project_technologies(projects: list[dict[str, Any]]) -> set[str]:
        """
        Extract all technologies used across all projects.

        Args:
            projects: List of project entries from resume analysis

        Returns:
            Set of technology names
        """
        if not projects:
            return set()

        technologies = set()

        for project in projects:
            if not isinstance(project, dict):
                continue

            # Get technologies from different possible fields
            tech_list = project.get("technologies")
            if isinstance(tech_list, list):
                for tech in tech_list:
                    if isinstance(tech, str):
                        technologies.add(tech.lower().strip())
            elif isinstance(tech_list, str):
                # Split by common separators
                for tech in tech_list.split(","):
                    technologies.add(tech.lower().strip())

            # Also check description for tech keywords
            description = project.get("description", "")
            if description:
                tech_keywords = ["python", "java", "javascript", "react", "angular", "vue", 
                               "nodejs", "django", "flask", "spring", "docker", "kubernetes",
                               "aws", "azure", "gcp", "sql", "mongodb", "postgresql", "mysql",
                               "tensorflow", "pytorch", "machine learning", "ai", "data science"]
                for keyword in tech_keywords:
                    if keyword in description.lower():
                        technologies.add(keyword)

        return technologies

    @staticmethod
    def evaluate_project_relevance(
        project: dict[str, Any],
        required_skills: list[str],
    ) -> dict[str, Any]:
        """
        Evaluate how relevant a single project is to job requirements.

        Args:
            project: Single project entry
            required_skills: List of required skills from job

        Returns:
            Dict with relevance analysis:
                - is_relevant: Boolean if project uses required skills
                - matching_technologies: List of matching technologies
                - relevance_score: Score (0-100)
                - has_technologies: Boolean if project has technology info
                - has_description: Boolean if project has description
        """
        if not isinstance(project, dict):
            return {
                "is_relevant": False,
                "matching_technologies": [],
                "relevance_score": 0,
                "has_technologies": False,
                "has_description": False,
            }

        # Get project technologies
        tech_list = project.get("technologies")
        project_techs = set()
        
        if isinstance(tech_list, list):
            for tech in tech_list:
                if isinstance(tech, str):
                    project_techs.add(tech.lower().strip())
        elif isinstance(tech_list, str):
            for tech in tech_list.split(","):
                project_techs.add(tech.lower().strip())

        # Check for matching technologies
        required_lower = [skill.lower() for skill in required_skills]
        matching_techs = [tech for tech in project_techs if tech in required_lower]

        # Calculate relevance score
        if not required_skills:
            relevance_score = 50  # Neutral if no requirements
        elif not matching_techs:
            relevance_score = 0
        else:
            # Score based on percentage of required skills used
            match_ratio = len(matching_techs) / len(required_skills)
            relevance_score = int(match_ratio * 100)

        # Check completeness
        has_technologies = bool(project_techs)
        has_description = bool(project.get("description"))

        return {
            "is_relevant": len(matching_techs) > 0,
            "matching_technologies": matching_techs,
            "relevance_score": relevance_score,
            "has_technologies": has_technologies,
            "has_description": has_description,
        }

    @staticmethod
    def count_relevant_projects(
        projects: list[dict[str, Any]],
        required_skills: list[str],
    ) -> dict[str, Any]:
        """
        Count and analyze relevant projects.

        Args:
            projects: List of project entries from resume
            required_skills: List of required skills from job

        Returns:
            Dict with project analysis:
                - total_projects: Total number of projects
                - relevant_projects: Number of relevant projects
                - irrelevant_projects: Number of irrelevant projects
                - relevance_percentage: Percentage of relevant projects
                - relevant_project_details: List of relevant project info
        """
        if not projects:
            return {
                "total_projects": 0,
                "relevant_projects": 0,
                "irrelevant_projects": 0,
                "relevance_percentage": 0,
                "relevant_project_details": [],
            }

        relevant_count = 0
        relevant_details = []

        for project in projects:
            if not isinstance(project, dict):
                continue

            relevance = ProjectMatcher.evaluate_project_relevance(project, required_skills)
            
            if relevance["is_relevant"]:
                relevant_count += 1
                relevant_details.append({
                    "title": project.get("title", "Untitled"),
                    "matching_technologies": relevance["matching_technologies"],
                    "relevance_score": relevance["relevance_score"],
                })

        total = len(projects)
        relevance_pct = (relevant_count / total * 100) if total > 0 else 0

        return {
            "total_projects": total,
            "relevant_projects": relevant_count,
            "irrelevant_projects": total - relevant_count,
            "relevance_percentage": round(relevance_pct, 1),
            "relevant_project_details": relevant_details,
        }

    @staticmethod
    def check_project_completeness(projects: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Check how complete the project information is.

        Args:
            projects: List of project entries from resume

        Returns:
            Dict with completeness analysis:
                - complete_projects: Number of complete projects
                - incomplete_projects: Number of incomplete projects
                - avg_completeness_score: Average completeness score (0-100)
                - completeness_issues: List of common issues
        """
        if not projects:
            return {
                "complete_projects": 0,
                "incomplete_projects": 0,
                "avg_completeness_score": 0,
                "completeness_issues": [],
            }

        complete_count = 0
        total_score = 0
        issues = []

        for project in projects:
            if not isinstance(project, dict):
                continue

            score = 0
            project_issues = []

            # Check for title
            if project.get("title"):
                score += 25
            else:
                project_issues.append("Missing title")

            # Check for description
            if project.get("description") and len(project.get("description", "")) > 20:
                score += 25
            else:
                project_issues.append("Missing or short description")

            # Check for technologies
            if project.get("technologies"):
                score += 25
            else:
                project_issues.append("Missing technologies")

            # Check for role or duration
            if project.get("role") or project.get("duration"):
                score += 25
            else:
                project_issues.append("Missing role or duration")

            if score >= 75:
                complete_count += 1
            else:
                issues.extend(project_issues)

            total_score += score

        avg_score = total_score / len(projects) if projects else 0

        return {
            "complete_projects": complete_count,
            "incomplete_projects": len(projects) - complete_count,
            "avg_completeness_score": round(avg_score, 1),
            "completeness_issues": issues[:5],  # Limit to top 5 issues
        }

    @staticmethod
    def compare_projects(
        resume_projects: list[dict[str, Any]],
        job_required_skills: list[str],
    ) -> dict[str, Any]:
        """
        Compare candidate projects with job requirements.

        Args:
            resume_projects: List of project entries from resume
            job_required_skills: List of required skills from job

        Returns:
            Dict with project comparison including:
                - has_projects: Boolean if candidate has projects
                - project_technologies: All technologies from projects
                - relevant_projects_count: Number of relevant projects
                - total_projects_count: Total number of projects
                - project_relevance_percentage: Percentage of relevant projects
                - project_completeness_score: Average completeness score
                - project_match_score: Overall project match score (0-100)
                - project_breakdown: Detailed breakdown
        """
        # Extract all technologies
        project_technologies = ProjectMatcher.extract_project_technologies(resume_projects)

        # Count relevant projects
        relevance_analysis = ProjectMatcher.count_relevant_projects(
            resume_projects,
            job_required_skills,
        )

        # Check completeness
        completeness_analysis = ProjectMatcher.check_project_completeness(resume_projects)

        # Calculate overall project match score
        project_score = ProjectMatcher._calculate_project_score(
            resume_projects,
            job_required_skills,
            relevance_analysis,
            completeness_analysis,
        )

        return {
            "has_projects": len(resume_projects) > 0,
            "project_technologies": sorted(list(project_technologies)),
            "relevant_projects_count": relevance_analysis["relevant_projects"],
            "total_projects_count": relevance_analysis["total_projects"],
            "project_relevance_percentage": relevance_analysis["relevance_percentage"],
            "project_completeness_score": completeness_analysis["avg_completeness_score"],
            "project_match_score": project_score,
            "project_breakdown": {
                "relevant_projects": relevance_analysis["relevant_projects"],
                "irrelevant_projects": relevance_analysis["irrelevant_projects"],
                "complete_projects": completeness_analysis["complete_projects"],
                "incomplete_projects": completeness_analysis["incomplete_projects"],
                "matching_technologies_count": len([
                    tech for tech in project_technologies 
                    if tech in [s.lower() for s in job_required_skills]
                ]),
            }
        }

    @staticmethod
    def _calculate_project_score(
        projects: list[dict[str, Any]],
        required_skills: list[str],
        relevance_analysis: dict[str, Any],
        completeness_analysis: dict[str, Any],
    ) -> int:
        """
        Calculate overall project match score (0-100).

        Scoring logic:
        - 40%: Project relevance (percentage of relevant projects)
        - 30%: Technology coverage (percentage of required skills used)
        - 30%: Project completeness (average completeness score)
        """
        if not projects:
            return 0

        # Project relevance score (40%)
        relevance_pct = relevance_analysis["relevance_percentage"]
        relevance_score = relevance_pct * 0.4

        # Technology coverage score (30%)
        project_technologies = ProjectMatcher.extract_project_technologies(projects)
        if required_skills:
            required_lower = [s.lower() for s in required_skills]
            matching_techs = [t for t in project_technologies if t in required_lower]
            coverage_pct = (len(matching_techs) / len(required_skills)) * 100 if required_skills else 0
            tech_score = coverage_pct * 0.3
        else:
            tech_score = 30  # Full credit if no requirements

        # Completeness score (30%)
        completeness_score = completeness_analysis["avg_completeness_score"] * 0.3

        total_score = int(relevance_score + tech_score + completeness_score)
        return min(total_score, 100)

    @staticmethod
    def get_project_match_rating(score: int) -> str:
        """
        Get qualitative rating based on project match score.

        Args:
            score: Project match score (0-100)

        Returns:
            Qualitative rating string
        """
        if score >= 90:
            return "Excellent Project Match"
        elif score >= 75:
            return "Strong Project Match"
        elif score >= 60:
            return "Good Project Match"
        elif score >= 40:
            return "Fair Project Match"
        elif score >= 20:
            return "Weak Project Match"
        else:
            return "Poor Project Match"

    @staticmethod
    def get_project_insights(
        resume_projects: list[dict[str, Any]],
        job_required_skills: list[str],
    ) -> dict[str, Any]:
        """
        Generate detailed insights about project compatibility.

        Args:
            resume_projects: List of project entries from resume
            job_required_skills: List of required skills from job

        Returns:
            Dict with insights including recommendations
        """
        comparison = ProjectMatcher.compare_projects(resume_projects, job_required_skills)

        insights = {
            "recommendation": "",
            "strengths": [],
            "concerns": [],
        }

        total_projects = comparison["total_projects_count"]
        relevant_pct = comparison["project_relevance_percentage"]
        completeness = comparison["project_completeness_score"]

        if total_projects == 0:
            insights["recommendation"] = "No projects listed on resume."
            insights["concerns"].append("Missing project experience")
        elif relevant_pct >= 70:
            insights["recommendation"] = f"Candidate has {total_projects} projects with high relevance to job requirements."
            insights["strengths"].append(f"{relevant_pct:.0f}% of projects are relevant to job requirements")
        elif relevant_pct >= 40:
            insights["recommendation"] = f"Candidate has {total_projects} projects with moderate relevance."
            insights["strengths"].append(f"Some projects use required technologies")
        else:
            insights["recommendation"] = f"Candidate has {total_projects} projects but low relevance to job requirements."
            insights["concerns"].append("Projects don't use required technologies")

        # Completeness insights
        if completeness >= 75:
            insights["strengths"].append("Projects are well-documented")
        elif completeness >= 50:
            insights["strengths"].append("Projects have basic documentation")
        else:
            insights["concerns"].append("Projects lack detailed information")

        return insights
