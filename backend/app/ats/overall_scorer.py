"""
Overall Scorer – ATS Overall Score Calculation
==============================================
Calculates the overall ATS score by combining individual component scores.
Implements weighted scoring based on the importance of each resume quality aspect.
"""


class OverallScorer:
    """Calculates overall ATS score from individual component scores."""

    # Weight distribution for overall score calculation
    # Weights are based on relative importance for ATS systems
    SCORE_WEIGHTS = {
        "skills": 0.25,        # 25% - Skills are critical for matching
        "experience": 0.20,    # 20% - Experience shows practical application
        "education": 0.15,     # 15% - Education provides foundation
        "keyword": 0.15,       # 15% - Keywords enable ATS matching
        "format": 0.10,        # 10% - Format affects ATS parsing
        "section": 0.10,       # 10% - Section completeness ensures ATS readability
        "projects": 0.05,      # 5%  - Projects demonstrate practical skills
    }

    @staticmethod
    def calculate_overall_score(
        format_score: float,
        section_score: float,
        skills_score: float,
        experience_score: float,
        education_score: float,
        project_score: float,
        keyword_score: float,
    ) -> float:
        """
        Calculate overall ATS score using weighted average of component scores.

        Args:
            format_score: Format score (0-100)
            section_score: Section score (0-100)
            skills_score: Skills score (0-100)
            experience_score: Experience score (0-100)
            education_score: Education score (0-100)
            project_score: Project score (0-100)
            keyword_score: Keyword score (0-100)

        Returns:
            Overall ATS score (0-100) rounded to 2 decimal places
        """
        # Calculate weighted average
        overall_score = (
            skills_score * OverallScorer.SCORE_WEIGHTS["skills"] +
            experience_score * OverallScorer.SCORE_WEIGHTS["experience"] +
            education_score * OverallScorer.SCORE_WEIGHTS["education"] +
            keyword_score * OverallScorer.SCORE_WEIGHTS["keyword"] +
            format_score * OverallScorer.SCORE_WEIGHTS["format"] +
            section_score * OverallScorer.SCORE_WEIGHTS["section"] +
            project_score * OverallScorer.SCORE_WEIGHTS["projects"]
        )

        return round(overall_score, 2)

    @staticmethod
    def get_score_breakdown(
        format_score: float,
        section_score: float,
        skills_score: float,
        experience_score: float,
        education_score: float,
        project_score: float,
        keyword_score: float,
    ) -> dict:
        """
        Get detailed breakdown of how overall score is calculated.

        Args:
            format_score: Format score (0-100)
            section_score: Section score (0-100)
            skills_score: Skills score (0-100)
            experience_score: Experience score (0-100)
            education_score: Education score (0-100)
            project_score: Project score (0-100)
            keyword_score: Keyword score (0-100)

        Returns:
            Dict with score breakdown including weighted contributions
        """
        overall_score = OverallScorer.calculate_overall_score(
            format_score, section_score, skills_score,
            experience_score, education_score, project_score, keyword_score
        )

        return {
            "overall_score": overall_score,
            "score_breakdown": {
                "skills": {
                    "score": skills_score,
                    "weight": OverallScorer.SCORE_WEIGHTS["skills"],
                    "contribution": round(skills_score * OverallScorer.SCORE_WEIGHTS["skills"], 2)
                },
                "experience": {
                    "score": experience_score,
                    "weight": OverallScorer.SCORE_WEIGHTS["experience"],
                    "contribution": round(experience_score * OverallScorer.SCORE_WEIGHTS["experience"], 2)
                },
                "education": {
                    "score": education_score,
                    "weight": OverallScorer.SCORE_WEIGHTS["education"],
                    "contribution": round(education_score * OverallScorer.SCORE_WEIGHTS["education"], 2)
                },
                "keyword": {
                    "score": keyword_score,
                    "weight": OverallScorer.SCORE_WEIGHTS["keyword"],
                    "contribution": round(keyword_score * OverallScorer.SCORE_WEIGHTS["keyword"], 2)
                },
                "format": {
                    "score": format_score,
                    "weight": OverallScorer.SCORE_WEIGHTS["format"],
                    "contribution": round(format_score * OverallScorer.SCORE_WEIGHTS["format"], 2)
                },
                "section": {
                    "score": section_score,
                    "weight": OverallScorer.SCORE_WEIGHTS["section"],
                    "contribution": round(section_score * OverallScorer.SCORE_WEIGHTS["section"], 2)
                },
                "projects": {
                    "score": project_score,
                    "weight": OverallScorer.SCORE_WEIGHTS["projects"],
                    "contribution": round(project_score * OverallScorer.SCORE_WEIGHTS["projects"], 2)
                },
            },
            "score_weights": OverallScorer.SCORE_WEIGHTS.copy()
        }

    @staticmethod
    def get_score_rating(overall_score: float) -> str:
        """
        Get a qualitative rating based on overall score.

        Args:
            overall_score: Overall ATS score (0-100)

        Returns:
            Qualitative rating string
        """
        if overall_score >= 90:
            return "Excellent"
        elif overall_score >= 80:
            return "Very Good"
        elif overall_score >= 70:
            return "Good"
        elif overall_score >= 60:
            return "Fair"
        elif overall_score >= 50:
            return "Below Average"
        else:
            return "Poor"

    @staticmethod
    def get_improvement_priorities(
        format_score: float,
        section_score: float,
        skills_score: float,
        experience_score: float,
        education_score: float,
        project_score: float,
        keyword_score: float,
    ) -> list[str]:
        """
        Get prioritized list of areas to improve based on scores.

        Args:
            format_score: Format score (0-100)
            section_score: Section score (0-100)
            skills_score: Skills score (0-100)
            experience_score: Experience score (0-100)
            education_score: Education score (0-100)
            project_score: Project score (0-100)
            keyword_score: Keyword score (0-100)

        Returns:
            List of improvement priorities sorted by weight and score
        """
        scores = {
            "skills": skills_score,
            "experience": experience_score,
            "education": education_score,
            "keyword": keyword_score,
            "format": format_score,
            "section": section_score,
            "projects": project_score,
        }

        # Sort by (weight * (100 - score)) to prioritize high-weight, low-score areas
        priorities = []
        for component, score in scores.items():
            weight = OverallScorer.SCORE_WEIGHTS[component]
            priority_score = weight * (100 - score)
            priorities.append((component, score, priority_score))

        # Sort by priority score (descending)
        priorities.sort(key=lambda x: x[2], reverse=True)

        # Generate improvement suggestions
        suggestions = []
        for component, score, _ in priorities:
            if score < 70:
                suggestions.append(f"Improve {component} (current: {score:.1f}/100)")
            elif score < 85:
                suggestions.append(f"Enhance {component} (current: {score:.1f}/100)")

        return suggestions
