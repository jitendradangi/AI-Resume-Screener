"""
Overall Matcher – Sprint 9 Task 8
================================
Calculates the overall match score by combining all component scores
with weighted averaging. Provides match level classification and detailed breakdown.
"""

from typing import Any


class OverallMatcher:
    """Calculates overall match score from component scores."""

    # Weight distribution for overall match calculation
    WEIGHTS = {
        "skill_match": 0.35,      # 35%
        "experience_match": 0.20,  # 20%
        "semantic_match": 0.20,   # 20%
        "project_match": 0.10,     # 10%
        "education_match": 0.05,   # 5%
        "ats_score": 0.10,         # 10%
    }

    @staticmethod
    def calculate_overall_score(
        skill_score: float,
        experience_score: float,
        education_score: float,
        project_score: float,
        semantic_score: float | None = None,
        ats_score: float | None = None,
    ) -> dict[str, Any]:
        """
        Calculate overall match score using weighted averaging.

        Args:
            skill_score: Skill match score (0-100)
            experience_score: Experience match score (0-100)
            education_score: Education match score (0-100)
            project_score: Project match score (0-100)
            semantic_score: Semantic match score (0-100), optional
            ats_score: ATS quality score (0-100), optional

        Returns:
            Dict with overall match analysis:
                - overall_match: Overall score (0-100)
                - match_level: Qualitative match level
                - score_breakdown: Detailed component breakdown
                - contribution_breakdown: How much each component contributed
        """
        # Build component scores dict
        component_scores = {
            "skill_match": skill_score,
            "experience_match": experience_score,
            "education_match": education_score,
            "project_match": project_score,
        }

        # Add optional components
        if semantic_score is not None:
            component_scores["semantic_match"] = semantic_score
        if ats_score is not None:
            component_scores["ats_score"] = ats_score

        # Calculate weighted score
        total_weight = 0.0
        weighted_sum = 0.0
        contribution_breakdown = {}

        for component, score in component_scores.items():
            weight = OverallMatcher.WEIGHTS.get(component, 0)
            if weight > 0:
                contribution = score * weight
                weighted_sum += contribution
                total_weight += weight
                contribution_breakdown[component] = {
                    "score": score,
                    "weight": weight,
                    "contribution": round(contribution, 2),
                }

        # If semantic or ATS score is missing, redistribute weights
        if total_weight < 1.0:
            missing_weight = 1.0 - total_weight
            num_present = len([c for c in component_scores.keys() if c in OverallMatcher.WEIGHTS])
            if num_present > 0:
                redistribution = missing_weight / num_present
                weighted_sum = 0.0
                for component in component_scores.keys():
                    if component in OverallMatcher.WEIGHTS:
                        old_weight = OverallMatcher.WEIGHTS[component]
                        new_weight = old_weight + redistribution
                        contribution = component_scores[component] * new_weight
                        weighted_sum += contribution
                        contribution_breakdown[component] = {
                            "score": component_scores[component],
                            "weight": round(new_weight, 3),
                            "contribution": round(contribution, 2),
                        }
                total_weight = 1.0

        # Calculate final score
        overall_score = round(weighted_sum, 1) if total_weight > 0 else 0.0
        overall_score = min(max(overall_score, 0), 100)  # Clamp to 0-100

        # Get match level
        match_level = OverallMatcher.get_match_level(overall_score)

        return {
            "overall_match": overall_score,
            "match_level": match_level,
            "score_breakdown": component_scores,
            "contribution_breakdown": contribution_breakdown,
        }

    @staticmethod
    def get_match_level(score: float) -> str:
        """
        Convert score to user-friendly match level.

        Args:
            score: Overall match score (0-100)

        Returns:
            Match level string
        """
        if score >= 90:
            return "Excellent Match"
        elif score >= 75:
            return "Strong Match"
        elif score >= 60:
            return "Good Match"
        elif score >= 40:
            return "Partial Match"
        else:
            return "Poor Match"

    @staticmethod
    def get_score_breakdown(
        skill_score: float,
        experience_score: float,
        education_score: float,
        project_score: float,
        semantic_score: float | None = None,
        ats_score: float | None = None,
    ) -> dict[str, Any]:
        """
        Get detailed breakdown of component scores.

        Args:
            skill_score: Skill match score (0-100)
            experience_score: Experience match score (0-100)
            education_score: Education match score (0-100)
            project_score: Project match score (0-100)
            semantic_score: Semantic match score (0-100), optional
            ats_score: ATS quality score (0-100), optional

        Returns:
            Dict with component scores and their qualitative ratings
        """
        breakdown = {
            "skills": {
                "score": skill_score,
                "rating": OverallMatcher._get_component_rating(skill_score),
            },
            "experience": {
                "score": experience_score,
                "rating": OverallMatcher._get_component_rating(experience_score),
            },
            "education": {
                "score": education_score,
                "rating": OverallMatcher._get_component_rating(education_score),
            },
            "projects": {
                "score": project_score,
                "rating": OverallMatcher._get_component_rating(project_score),
            },
        }

        if semantic_score is not None:
            breakdown["semantic"] = {
                "score": semantic_score,
                "rating": OverallMatcher._get_component_rating(semantic_score),
            }

        if ats_score is not None:
            breakdown["ats"] = {
                "score": ats_score,
                "rating": OverallMatcher._get_component_rating(ats_score),
            }

        return breakdown

    @staticmethod
    def _get_component_rating(score: float) -> str:
        """Get qualitative rating for a component score."""
        if score >= 90:
            return "Excellent"
        elif score >= 75:
            return "Strong"
        elif score >= 60:
            return "Good"
        elif score >= 40:
            return "Fair"
        else:
            return "Poor"

    @staticmethod
    def get_improvement_priorities(
        skill_score: float,
        experience_score: float,
        education_score: float,
        project_score: float,
        semantic_score: float | None = None,
        ats_score: float | None = None,
    ) -> list[str]:
        """
        Generate improvement priorities based on component scores.

        Args:
            skill_score: Skill match score (0-100)
            experience_score: Experience match score (0-100)
            education_score: Education match score (0-100)
            project_score: Project match score (0-100)
            semantic_score: Semantic match score (0-100), optional
            ats_score: ATS quality score (0-100), optional

        Returns:
            List of improvement recommendations ordered by priority
        """
        priorities = []

        components = [
            ("skill_match", skill_score, "Skill match"),
            ("experience_match", experience_score, "Experience match"),
            ("education_match", education_score, "Education match"),
            ("project_match", project_score, "Project match"),
        ]

        if semantic_score is not None:
            components.append(("semantic_match", semantic_score, "Semantic match"))
        if ats_score is not None:
            components.append(("ats_score", ats_score, "ATS score"))

        # Sort by score (lowest first = highest priority)
        components.sort(key=lambda x: x[1])

        for component, score, name in components:
            if score < 40:
                priorities.append(f"Improve {name.lower()} (current: {score:.0f}/100)")
            elif score < 60:
                priorities.append(f"Enhance {name.lower()} (current: {score:.0f}/100)")

        return priorities[:5]  # Limit to top 5 priorities
