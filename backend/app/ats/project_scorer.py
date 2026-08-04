"""
Project Scorer – ATS Project Quality Analysis
=============================================
Analyzes and scores project quality for resume quality ATS evaluation.
Evaluates project completeness, description quality, technical details, and measurable impact.
"""

import re


class ProjectScorer:
    """Analyzes and scores projects for resume quality ATS evaluation."""

    # Technical indicators that show project depth
    TECHNICAL_INDICATORS = {
        "technologies": ["python", "java", "javascript", "react", "angular", "vue", "nodejs", "django", "flask", "spring", "docker", "kubernetes", "aws", "azure", "gcp", "sql", "nosql", "mongodb", "postgresql", "mysql", "redis", "git", "ci/cd", "jenkins", "tensorflow", "pytorch", "machine learning", "ai", "deep learning"],
        "tools": ["git", "github", "gitlab", "jira", "confluence", "slack", "vscode", "intellij", "eclipse", "docker", "kubernetes", "terraform", "ansible"],
        "methodologies": ["agile", "scrum", "kanban", "tdd", "bdd", "devops", "ci/cd", "microservices", "monolith", "rest api", "graphql", "grpc"],
    }

    # Impact indicators (measurable results)
    IMPACT_INDICATORS = {
        "metrics": ["%", "percent", "increase", "decrease", "reduction", "improvement", "growth", "scale", "users", "customers", "clients", "revenue", "cost", "budget", "time", "faster", "quicker", "sooner"],
        "achievements": ["launched", "deployed", "released", "published", "delivered", "completed", "finished", "shipped", "implemented", "developed", "built", "created", "designed"],
    }

    @staticmethod
    def get_project_analysis(resume_analysis: dict) -> dict:
        """
        Analyze project quality and calculate project score.

        Args:
            resume_analysis: Dict containing resume analysis data with keys:
                - projects: list of project dicts with keys: title, description, technologies, role, duration

        Returns:
            Dict with project analysis results including:
                - overall_project_score: Overall project quality score (0-100)
                - completeness_score: Score for information completeness
                - description_quality_score: Score for description quality
                - technical_depth_score: Score for technical details
                - impact_score: Score for measurable impact
                - project_issues: List of identified project issues
                - project_recommendations: List of improvement recommendations
        """
        projects = resume_analysis.get("projects", [])

        if not projects or len(projects) == 0:
            return {
                "overall_project_score": 0.0,
                "completeness_score": 0.0,
                "description_quality_score": 0.0,
                "technical_depth_score": 0.0,
                "impact_score": 0.0,
                "project_issues": ["No projects provided"],
                "project_recommendations": ["Add a projects section to showcase your practical work and achievements"],
            }

        issues = []
        recommendations = []

        # Calculate individual scores
        completeness_score = ProjectScorer._calculate_completeness(projects, issues, recommendations)
        description_quality_score = ProjectScorer._calculate_description_quality(projects, issues, recommendations)
        technical_depth_score = ProjectScorer._calculate_technical_depth(projects, issues, recommendations)
        impact_score = ProjectScorer._calculate_impact(projects, issues, recommendations)

        # Calculate overall project score (weighted average)
        overall_score = (
            completeness_score * 0.25 +
            description_quality_score * 0.30 +
            technical_depth_score * 0.25 +
            impact_score * 0.20
        )

        return {
            "overall_project_score": round(overall_score, 2),
            "completeness_score": round(completeness_score, 2),
            "description_quality_score": round(description_quality_score, 2),
            "technical_depth_score": round(technical_depth_score, 2),
            "impact_score": round(impact_score, 2),
            "project_issues": issues,
            "project_recommendations": recommendations,
        }

    @staticmethod
    def _calculate_completeness(projects: list, issues: list, recommendations: list) -> float:
        """
        Calculate project completeness score based on information provided.

        Args:
            projects: List of project dicts
            issues: List to append identified issues
            recommendations: List to append recommendations

        Returns:
            Completeness score (0-100)
        """
        if not projects:
            return 0.0

        total_score = 0
        for project in projects:
            if isinstance(project, dict):
                score = 0
                # Check for required fields
                if project.get("title"):
                    score += 30
                else:
                    issues.append("Project entry missing title")
                    recommendations.append("Include project titles for all project entries")

                if project.get("description") and len(project["description"]) > 20:
                    score += 30
                else:
                    issues.append("Project entry missing or too short description")
                    recommendations.append("Add detailed descriptions for all project entries")

                if project.get("technologies") and len(project["technologies"]) > 0:
                    score += 20
                else:
                    recommendations.append("Include technologies used for each project")

                if project.get("role") or project.get("duration"):
                    score += 20
                else:
                    recommendations.append("Include your role and project duration for project entries")

                total_score += score

        # Average score across all projects
        avg_score = total_score / len(projects)
        return round(avg_score, 2)

    @staticmethod
    def _calculate_description_quality(projects: list, issues: list, recommendations: list) -> float:
        """
        Calculate description quality score based on detail and structure.

        Args:
            projects: List of project dicts
            issues: List to append identified issues
            recommendations: List to append recommendations

        Returns:
            Description quality score (0-100)
        """
        if not projects:
            return 0.0

        total_score = 0
        for project in projects:
            if isinstance(project, dict):
                description = project.get("description", "")
                score = 0

                # Check description length
                if len(description) < 20:
                    issues.append("Project description too short")
                    score += 0
                elif len(description) < 50:
                    score += 30
                    recommendations.append("Expand project descriptions with more details about objectives and outcomes")
                elif len(description) < 150:
                    score += 70
                else:
                    score += 100

                # Check for structured format (problem-solution-impact pattern)
                has_problem = any(word in description.lower() for word in ["problem", "challenge", "issue", "need"])
                has_solution = any(word in description.lower() for word in ["solution", "approach", "method", "implemented", "developed", "built"])
                has_result = any(word in description.lower() for word in ["result", "outcome", "achieved", "delivered", "launched", "released"])

                if has_problem and has_solution and has_result:
                    score += 20
                elif has_solution and has_result:
                    score += 10
                else:
                    recommendations.append("Structure project descriptions with problem-solution-impact format")

                total_score += min(score, 100)

        # Average score across all projects
        avg_score = total_score / len(projects)
        return round(avg_score, 2)

    @staticmethod
    def _calculate_technical_depth(projects: list, issues: list, recommendations: list) -> float:
        """
        Calculate technical depth score based on technologies and tools mentioned.

        Args:
            projects: List of project dicts
            issues: List to append identified issues
            recommendations: List to append recommendations

        Returns:
            Technical depth score (0-100)
        """
        if not projects:
            return 0.0

        total_score = 0
        has_technical_details = False

        for project in projects:
            if isinstance(project, dict):
                score = 0
                description = project.get("description", "").lower()
                technologies = project.get("technologies", [])

                # Check for technologies list
                if technologies and len(technologies) > 0:
                    score += 40
                    has_technical_details = True
                else:
                    recommendations.append("List technologies used in each project")

                # Check for technical keywords in description
                tech_count = 0
                for category, keywords in ProjectScorer.TECHNICAL_INDICATORS.items():
                    for keyword in keywords:
                        if keyword in description:
                            tech_count += 1
                            has_technical_details = True

                if tech_count >= 3:
                    score += 60
                elif tech_count >= 1:
                    score += 30
                else:
                    recommendations.append("Mention specific technologies, tools, and methodologies used in projects")

                total_score += score

        if not has_technical_details:
            issues.append("No technical details found in project descriptions")

        # Average score across all projects
        avg_score = total_score / len(projects)
        return round(avg_score, 2)

    @staticmethod
    def _calculate_impact(projects: list, issues: list, recommendations: list) -> float:
        """
        Calculate impact score based on measurable results and achievements.

        Args:
            projects: List of project dicts
            issues: List to append identified issues
            recommendations: List to append recommendations

        Returns:
            Impact score (0-100)
        """
        if not projects:
            return 0.0

        total_score = 0
        has_impact = False

        for project in projects:
            if isinstance(project, dict):
                description = project.get("description", "").lower()
                score = 0

                # Check for impact indicators
                impact_count = 0
                for category, indicators in ProjectScorer.IMPACT_INDICATORS.items():
                    for indicator in indicators:
                        if indicator in description:
                            impact_count += 1
                            has_impact = True

                if impact_count >= 3:
                    score += 100
                elif impact_count >= 2:
                    score += 70
                elif impact_count >= 1:
                    score += 40
                else:
                    recommendations.append("Add measurable impact and results to project descriptions (e.g., 'increased user engagement by 30%')")

                total_score += score

        if not has_impact:
            issues.append("No measurable impact found in project descriptions")

        # Average score across all projects
        avg_score = total_score / len(projects)
        return round(avg_score, 2)
