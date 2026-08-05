"""
Education Matcher – Job-Resume Education Compatibility Analysis
================================================================
Compares candidate education with job education requirements.
Normalizes degrees, evaluates hierarchy, and calculates match scores.
"""

import re
from typing import Any


class EducationMatcher:
    """Analyzes education compatibility between resumes and job requirements."""

    # Degree hierarchy (higher value = higher level)
    DEGREE_HIERARCHY = {
        "phd": 6,
        "doctorate": 6,
        "doctor of philosophy": 6,
        "md": 6,
        "medical doctor": 6,
        "jd": 6,
        "juris doctor": 6,
        "mba": 5,
        "master of business administration": 5,
        "master": 4,
        "master's": 4,
        "m.sc": 4,
        "msc": 4,
        "m.s": 4,
        "ms": 4,
        "m.tech": 4,
        "meng": 4,
        "m.eng": 4,
        "ma": 4,
        "m.a": 4,
        "master of arts": 4,
        "master of science": 4,
        "master of engineering": 4,
        "bachelor": 3,
        "bachelor's": 3,
        "b.sc": 3,
        "bsc": 3,
        "b.s": 3,
        "bs": 3,
        "b.tech": 3,
        "beng": 3,
        "b.eng": 3,
        "ba": 3,
        "b.a": 3,
        "bachelor of arts": 3,
        "bachelor of science": 3,
        "bachelor of engineering": 3,
        "bachelor of technology": 3,
        "associate": 2,
        "associate's": 2,
        "a.a": 2,
        "aa": 2,
        "a.s": 2,
        "as": 2,
        "diploma": 1,
        "certificate": 1,
        "certification": 1,
        "high school": 0,
        "ged": 0,
        "secondary": 0,
    }

    # Degree normalization mappings
    DEGREE_ALIASES = {
        "b.tech": ["bachelor of technology", "btech"],
        "m.tech": ["master of technology", "mtech"],
        "b.e": ["bachelor of engineering", "beng", "bachelor's in engineering"],
        "m.e": ["master of engineering", "meng", "master's in engineering"],
        "b.sc": ["bachelor of science", "bsc", "b.s", "bs", "bachelor's in science"],
        "m.sc": ["master of science", "msc", "m.s", "ms", "master's in science"],
        "b.a": ["bachelor of arts", "ba", "bachelor's in arts"],
        "m.a": ["master of arts", "ma", "master's in arts"],
        "mba": ["master of business administration", "m.b.a"],
        "phd": ["doctor of philosophy", "ph.d", "doctorate"],
    }

    # Field of study relevance mappings (can be expanded)
    RELEVANT_FIELDS = {
        "computer science": ["cs", "computing", "computer engineering", "software engineering"],
        "engineering": ["mechanical", "electrical", "civil", "chemical", "industrial"],
        "business": ["management", "finance", "marketing", "economics"],
        "data science": ["analytics", "machine learning", "ai", "artificial intelligence"],
        "mathematics": ["math", "statistics", "applied mathematics"],
    }

    @staticmethod
    def normalize_degree(degree: str) -> str:
        """
        Normalize a degree name to its canonical form.

        Args:
            degree: Raw degree name string

        Returns:
            Normalized degree name (lowercase, canonical form)
        """
        if not degree:
            return ""

        # Convert to lowercase and strip whitespace
        normalized = degree.lower().strip()
        
        # Remove special characters and extra spaces
        normalized = re.sub(r'[^\w\s\-\.\']', '', normalized)
        normalized = re.sub(r'\s+', ' ', normalized)
        
        # Check against aliases
        for canonical, aliases in EducationMatcher.DEGREE_ALIASES.items():
            if normalized in [alias.lower() for alias in aliases]:
                return canonical
            if normalized == canonical:
                return canonical
        
        # Try to match against hierarchy keys
        for degree_key in EducationMatcher.DEGREE_HIERARCHY.keys():
            if degree_key in normalized:
                return degree_key
        
        return normalized

    @staticmethod
    def get_degree_level(degree: str) -> int:
        """
        Get the hierarchy level of a degree.

        Args:
            degree: Degree name (normalized or raw)

        Returns:
            Integer level (0-6), 0 if not found
        """
        normalized = EducationMatcher.normalize_degree(degree)
        return EducationMatcher.DEGREE_HIERARCHY.get(normalized, 0)

    @staticmethod
    def get_highest_degree(education_data: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Get the highest degree from education data.

        Args:
            education_data: List of education entries from resume analysis

        Returns:
            Dict with highest degree info:
                - degree: Degree name
                - level: Hierarchy level
                - institution: Institution name
                - field: Field of study
        """
        if not education_data:
            return {
                "degree": None,
                "level": 0,
                "institution": None,
                "field": None,
            }

        highest_degree = {
            "degree": None,
            "level": 0,
            "institution": None,
            "field": None,
        }

        for edu in education_data:
            if not isinstance(edu, dict):
                continue

            degree_str = edu.get("degree", "")
            if not degree_str:
                continue

            level = EducationMatcher.get_degree_level(degree_str)
            
            if level > highest_degree["level"]:
                highest_degree = {
                    "degree": EducationMatcher.normalize_degree(degree_str),
                    "level": level,
                    "institution": edu.get("institution"),
                    "field": edu.get("field") or edu.get("details"),
                }

        return highest_degree

    @staticmethod
    def parse_job_education_requirement(job_education: str | None) -> dict[str, Any]:
        """
        Parse job education requirement into structured data.

        Args:
            job_education: Raw education requirement string from job

        Returns:
            Dict with parsed education requirements:
                - min_level: Minimum required level
                - required_degree: Specific degree required (if any)
                - preferred_degree: Preferred degree (if any)
                - required_field: Required field of study (if any)
        """
        if not job_education:
            return {
                "min_level": 0,
                "required_degree": None,
                "preferred_degree": None,
                "required_field": None,
            }

        req_lower = job_education.lower()
        
        # Try to find specific degree requirements
        for degree, level in EducationMatcher.DEGREE_HIERARCHY.items():
            if degree in req_lower:
                return {
                    "min_level": level,
                    "required_degree": degree,
                    "preferred_degree": None,
                    "required_field": None,
                }

        # Try to find "or higher" patterns
        for degree, level in EducationMatcher.DEGREE_HIERARCHY.items():
            if f"{degree} or higher" in req_lower or f"{degree}+" in req_lower:
                return {
                    "min_level": level,
                    "required_degree": degree,
                    "preferred_degree": None,
                    "required_field": None,
                }

        # Try to find "bachelor's degree" etc.
        if "bachelor" in req_lower or "bachelor's" in req_lower:
            return {
                "min_level": 3,
                "required_degree": "bachelor",
                "preferred_degree": None,
                "required_field": None,
            }
        elif "master" in req_lower or "master's" in req_lower:
            return {
                "min_level": 4,
                "required_degree": "master",
                "preferred_degree": None,
                "required_field": None,
            }
        elif "phd" in req_lower or "doctorate" in req_lower:
            return {
                "min_level": 6,
                "required_degree": "phd",
                "preferred_degree": None,
                "required_field": None,
            }

        # Default: couldn't parse
        return {
            "min_level": 0,
            "required_degree": None,
            "preferred_degree": None,
            "required_field": None,
        }

    @staticmethod
    def compare_education(
        resume_education: list[dict[str, Any]],
        job_education: str | None,
    ) -> dict[str, Any]:
        """
        Compare candidate education with job requirements.

        Args:
            resume_education: List of education entries from resume
            job_education: Education requirement string from job

        Returns:
            Dict with education comparison including:
                - candidate_degree: Highest degree from resume
                - candidate_level: Level of candidate's degree
                - required_degree: Required degree from job
                - required_level: Required minimum level
                - meets_requirement: Boolean if candidate meets requirement
                - exceeds_requirement: Boolean if candidate exceeds requirement
                - education_match_score: Score (0-100)
                - education_breakdown: Detailed breakdown
        """
        # Get candidate's highest degree
        candidate_info = EducationMatcher.get_highest_degree(resume_education)
        candidate_degree = candidate_info["degree"]
        candidate_level = candidate_info["level"]

        # Parse job requirement
        job_req = EducationMatcher.parse_job_education_requirement(job_education)
        required_degree = job_req["required_degree"]
        required_level = job_req["min_level"]

        # Determine if requirement is met
        meets_requirement = candidate_level >= required_level
        exceeds_requirement = candidate_level > required_level

        # Calculate education match score
        education_score = EducationMatcher._calculate_education_score(
            candidate_level,
            required_level,
            candidate_degree,
            required_degree,
        )

        return {
            "candidate_degree": candidate_degree,
            "candidate_level": candidate_level,
            "required_degree": required_degree,
            "required_level": required_level,
            "meets_requirement": meets_requirement,
            "exceeds_requirement": exceeds_requirement,
            "education_match_score": education_score,
            "education_breakdown": {
                "has_education": candidate_level > 0,
                "level_difference": candidate_level - required_level,
                "exact_match": candidate_degree == required_degree if required_degree else False,
            }
        }

    @staticmethod
    def _calculate_education_score(
        candidate_level: int,
        required_level: int,
        candidate_degree: str | None,
        required_degree: str | None,
    ) -> int:
        """
        Calculate education match score (0-100).

        Scoring logic:
        - 100 points: Exact degree match or exceeds by 1 level
        - 90 points: Exceeds requirement by 2+ levels
        - 80 points: Meets minimum with higher degree
        - 70 points: Meets minimum with exact degree
        - 50 points: Meets minimum but degree type mismatch
        - 30 points: One level below requirement
        - 10 points: Two or more levels below requirement
        - 0 points: No education or significantly below
        """
        if required_level == 0:
            # No requirement - give credit for having education
            if candidate_level >= 3:
                return 80  # Has at least bachelor's
            elif candidate_level >= 1:
                return 50  # Has some education
            else:
                return 0  # No education

        level_diff = candidate_level - required_level

        if level_diff >= 2:
            return 90  # Significantly exceeds requirement
        elif level_diff == 1:
            return 100  # Exceeds by one level (ideal)
        elif level_diff == 0:
            if candidate_degree == required_degree:
                return 70  # Exact match
            else:
                return 50  # Meets minimum but different degree type
        elif level_diff == -1:
            return 30  # One level below
        elif level_diff == -2:
            return 10  # Two levels below
        else:
            return 0  # Significantly below or no education

    @staticmethod
    def get_education_match_rating(score: int) -> str:
        """
        Get qualitative rating based on education match score.

        Args:
            score: Education match score (0-100)

        Returns:
            Qualitative rating string
        """
        if score >= 90:
            return "Excellent Education Match"
        elif score >= 75:
            return "Strong Education Match"
        elif score >= 60:
            return "Good Education Match"
        elif score >= 40:
            return "Fair Education Match"
        elif score >= 20:
            return "Weak Education Match"
        else:
            return "Poor Education Match"

    @staticmethod
    def get_education_insights(
        resume_education: list[dict[str, Any]],
        job_education: str | None,
    ) -> dict[str, Any]:
        """
        Generate detailed insights about education compatibility.

        Args:
            resume_education: List of education entries from resume
            job_education: Education requirement string from job

        Returns:
            Dict with insights including recommendations
        """
        comparison = EducationMatcher.compare_education(resume_education, job_education)

        insights = {
            "recommendation": "",
            "strengths": [],
            "concerns": [],
        }

        candidate_degree = comparison["candidate_degree"]
        required_degree = comparison["required_degree"]
        meets_req = comparison["meets_requirement"]
        exceeds = comparison["exceeds_requirement"]

        if candidate_degree:
            if exceeds:
                insights["recommendation"] = f"Candidate exceeds education requirement with {candidate_degree.title()}."
                insights["strengths"].append(f"Has {candidate_degree.title()} which exceeds requirement")
            elif meets_req:
                insights["recommendation"] = f"Candidate meets education requirement with {candidate_degree.title()}."
                insights["strengths"].append(f"Has required {candidate_degree.title()}")
            else:
                insights["recommendation"] = f"Candidate's education ({candidate_degree.title()}) is below requirement."
                insights["concerns"].append(f"Education level below requirement")
        else:
            insights["recommendation"] = "No education data available."
            insights["concerns"].append("No education information provided")

        # Additional insights
        if comparison["candidate_level"] >= 6:
            insights["strengths"].append("Doctoral level education")
        elif comparison["candidate_level"] >= 4:
            insights["strengths"].append("Advanced degree")
        elif comparison["candidate_level"] >= 3:
            insights["strengths"].append("Bachelor's degree")

        return insights
