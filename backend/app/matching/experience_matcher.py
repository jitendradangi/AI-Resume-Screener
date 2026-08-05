"""
Experience Matcher – Job-Resume Experience Compatibility Analysis
================================================================
Compares candidate experience with job experience requirements.
Calculates total experience duration and evaluates compatibility.
"""

import re
from typing import Any


class ExperienceMatcher:
    """Analyzes experience compatibility between resumes and job requirements."""

    # Experience level mappings
    EXPERIENCE_LEVELS = {
        "entry level": 0,
        "junior": 1,
        "mid level": 3,
        "mid-level": 3,
        "senior": 5,
        "lead": 7,
        "manager": 8,
        "director": 10,
        "principal": 12,
    }

    @staticmethod
    def calculate_years_of_experience(experience_data: list[dict[str, Any]]) -> float:
        """
        Calculate total years of experience from resume experience entries.

        Args:
            experience_data: List of experience entries from resume analysis

        Returns:
            Total years of experience (float)
        """
        if not experience_data:
            return 0.0

        total_years = 0.0

        for exp in experience_data:
            if not isinstance(exp, dict):
                continue

            # Try to get start and end years
            start_year = exp.get("start")
            end_year = exp.get("end")

            if start_year and end_year:
                try:
                    start = int(start_year)
                    if end_year.lower() in ["present", "current", "now"]:
                        from datetime import datetime
                        end = datetime.now().year
                    else:
                        end = int(end_year)

                    years = end - start
                    if years > 0:
                        total_years += years
                except (ValueError, AttributeError):
                    pass
            elif start_year:
                # If only start year, assume 1 year minimum
                try:
                    start = int(start_year)
                    from datetime import datetime
                    current_year = datetime.now().year
                    years = current_year - start
                    if years > 0:
                        total_years += years
                except (ValueError, AttributeError):
                    pass

        return round(total_years, 1)

    @staticmethod
    def parse_job_experience_requirement(job_experience: str | None) -> dict[str, Any]:
        """
        Parse job experience requirement into structured data.

        Args:
            job_experience: Raw experience requirement string from job

        Returns:
            Dict with parsed experience requirements:
                - min_years: Minimum years required
                - max_years: Maximum years (if specified)
                - level: Experience level (if specified)
                - requirement_type: 'years' or 'level'
        """
        if not job_experience:
            return {
                "min_years": 0,
                "max_years": None,
                "level": None,
                "requirement_type": None,
            }

        # Try to extract years (e.g., "5+ years", "3-5 years", "5 years")
        year_patterns = [
            r"(\d+)\+?\s*years?",
            r"(\d+)\s*-\s*(\d+)\s*years?",
            r"(\d+)\s*years?",
        ]

        for pattern in year_patterns:
            match = re.search(pattern, job_experience, re.IGNORECASE)
            if match:
                groups = match.groups()
                if len(groups) == 2:  # Range pattern
                    try:
                        min_years = int(groups[0])
                        max_years = int(groups[1])
                        return {
                            "min_years": min_years,
                            "max_years": max_years,
                            "level": None,
                            "requirement_type": "years",
                        }
                    except ValueError:
                        pass
                else:  # Single value pattern
                    try:
                        years = int(groups[0])
                        return {
                            "min_years": years,
                            "max_years": None,
                            "level": None,
                            "requirement_type": "years",
                        }
                    except ValueError:
                        pass

        # Try to extract experience level
        exp_lower = job_experience.lower()
        for level, years in ExperienceMatcher.EXPERIENCE_LEVELS.items():
            if level in exp_lower:
                return {
                    "min_years": years,
                    "max_years": None,
                    "level": level,
                    "requirement_type": "level",
                }

        # Default: couldn't parse
        return {
            "min_years": 0,
            "max_years": None,
            "level": None,
            "requirement_type": None,
        }

    @staticmethod
    def compare_experience(
        resume_experience: list[dict[str, Any]],
        job_experience: str | None,
    ) -> dict[str, Any]:
        """
        Compare candidate experience with job requirements.

        Args:
            resume_experience: List of experience entries from resume
            job_experience: Experience requirement string from job

        Returns:
            Dict with experience comparison including:
                - candidate_years: Total years of candidate experience
                - required_min_years: Minimum years required
                - required_max_years: Maximum years (if specified)
                - required_level: Required experience level
                - years_difference: Difference between candidate and required years
                - meets_requirement: Boolean if candidate meets requirement
                - experience_match_score: Score (0-100)
                - experience_breakdown: Detailed breakdown
        """
        # Calculate candidate experience
        candidate_years = ExperienceMatcher.calculate_years_of_experience(resume_experience)

        # Parse job requirement
        job_req = ExperienceMatcher.parse_job_experience_requirement(job_experience)
        required_min = job_req["min_years"]
        required_max = job_req["max_years"]
        required_level = job_req["level"]

        # Calculate difference
        years_difference = candidate_years - required_min

        # Determine if requirement is met
        meets_requirement = candidate_years >= required_min

        # Check if exceeds maximum (if specified)
        exceeds_max = False
        if required_max and candidate_years > required_max:
            exceeds_max = True

        # Calculate experience match score
        experience_score = ExperienceMatcher._calculate_experience_score(
            candidate_years,
            required_min,
            required_max,
            required_level,
        )

        return {
            "candidate_years": candidate_years,
            "required_min_years": required_min,
            "required_max_years": required_max,
            "required_level": required_level,
            "years_difference": round(years_difference, 1),
            "meets_requirement": meets_requirement,
            "exceeds_max": exceeds_max,
            "experience_match_score": experience_score,
            "experience_breakdown": {
                "requirement_type": job_req["requirement_type"],
                "overqualified": years_difference > 2,
                "underqualified": years_difference < -1,
                "well_matched": abs(years_difference) <= 2,
            }
        }

    @staticmethod
    def _calculate_experience_score(
        candidate_years: float,
        required_min: int,
        required_max: int | None,
        required_level: str | None,
    ) -> int:
        """
        Calculate experience match score (0-100).

        Scoring logic:
        - 100 points: Exact match or within +/- 1 year
        - 80-90 points: Within +/- 2 years
        - 60-70 points: Meets minimum but off by 2-3 years
        - 40-50 points: Underqualified by 1-2 years
        - 20-30 points: Underqualified by 3-5 years
        - 0-10 points: Significantly underqualified or overqualified
        """
        if required_min == 0:
            # No requirement - give full credit for having experience
            return min(int(candidate_years * 10), 100)

        difference = candidate_years - required_min

        # Check for overqualification
        if required_max and candidate_years > required_max:
            over_diff = candidate_years - required_max
            if over_diff > 5:
                return 30  # Too overqualified
            elif over_diff > 2:
                return 50  # Somewhat overqualified
            else:
                return 70  # Slightly overqualified

        # Check for underqualification
        if difference < -5:
            return 10  # Significantly underqualified
        elif difference < -3:
            return 30  # Underqualified by 3-5 years
        elif difference < -1:
            return 50  # Underqualified by 1-2 years
        elif difference < 0:
            return 70  # Slightly underqualified
        elif difference <= 1:
            return 100  # Perfect match
        elif difference <= 2:
            return 90  # Excellent match
        elif difference <= 4:
            return 80  # Good match
        else:
            return 70  # More experienced than required (good)

    @staticmethod
    def get_experience_match_rating(score: int) -> str:
        """
        Get qualitative rating based on experience match score.

        Args:
            score: Experience match score (0-100)

        Returns:
            Qualitative rating string
        """
        if score >= 90:
            return "Excellent Experience Match"
        elif score >= 75:
            return "Strong Experience Match"
        elif score >= 60:
            return "Good Experience Match"
        elif score >= 40:
            return "Fair Experience Match"
        elif score >= 20:
            return "Weak Experience Match"
        else:
            return "Poor Experience Match"

    @staticmethod
    def get_experience_insights(
        resume_experience: list[dict[str, Any]],
        job_experience: str | None,
    ) -> dict[str, Any]:
        """
        Generate detailed insights about experience compatibility.

        Args:
            resume_experience: List of experience entries from resume
            job_experience: Experience requirement string from job

        Returns:
            Dict with insights including recommendations
        """
        comparison = ExperienceMatcher.compare_experience(resume_experience, job_experience)

        insights = {
            "recommendation": "",
            "strengths": [],
            "concerns": [],
        }

        candidate_years = comparison["candidate_years"]
        required_min = comparison["required_min_years"]
        years_diff = comparison["years_difference"]

        if comparison["meets_requirement"]:
            if comparison["exceeds_max"]:
                insights["recommendation"] = "Candidate is overqualified but experienced."
                insights["concerns"].append("May be overqualified for the role")
            elif comparison["experience_breakdown"]["well_matched"]:
                insights["recommendation"] = "Candidate's experience level is an excellent match."
                insights["strengths"].append("Experience level matches requirements perfectly")
            else:
                insights["recommendation"] = "Candidate meets experience requirements."
                insights["strengths"].append(f"{candidate_years} years of experience meets requirement of {required_min}+ years")
        else:
            deficit = abs(years_diff)
            insights["recommendation"] = f"Candidate is {deficit:.1f} years short of experience requirement."
            insights["concerns"].append(f"Missing {deficit:.1f} years of required experience")

        # Additional insights based on experience data
        if candidate_years >= 10:
            insights["strengths"].append("Substantial industry experience")
        elif candidate_years >= 5:
            insights["strengths"].append("Strong professional experience")
        elif candidate_years >= 3:
            insights["strengths"].append("Solid mid-level experience")

        if not resume_experience:
            insights["concerns"].append("No work experience data available")

        return insights
