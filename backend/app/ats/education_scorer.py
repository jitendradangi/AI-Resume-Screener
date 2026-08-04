"""
EducationScorer – ATS Education Quality Analysis
================================================
Normalizes degrees and evaluates education quality for resume ATS scoring.
Assesses education level, field relevance, completeness, and presentation.
"""

import re


class EducationScorer:
    """Analyzes and scores education for resume quality ATS evaluation."""

    # Degree level hierarchy (higher number = higher level)
    DEGREE_LEVELS = {
        "high school": 1,
        "secondary school": 1,
        "ged": 1,
        "diploma": 2,
        "associate": 2,
        "associate degree": 2,
        "bachelor": 3,
        "bachelor's": 3,
        "bachelor degree": 3,
        "bachelor of science": 3,
        "bachelor of arts": 3,
        "b.sc": 3,
        "b.a": 3,
        "bs": 3,
        "ba": 3,
        "master": 4,
        "master's": 4,
        "master degree": 4,
        "master of science": 4,
        "master of arts": 4,
        "master of business administration": 4,
        "mba": 4,
        "m.sc": 4,
        "m.a": 4,
        "ms": 4,
        "ma": 4,
        "phd": 5,
        "doctorate": 5,
        "doctoral": 5,
        "doctor of philosophy": 5,
        "doctor of science": 5,
        "doctor of medicine": 5,
        "md": 5,
        "professor": 6,
    }

    # Field of study categories for relevance assessment
    FIELD_CATEGORIES = {
        # Computer Science & IT
        "computer science": ["cs", "computing", "information technology", "it", "software engineering"],
        "data science": ["machine learning", "artificial intelligence", "ai", "analytics"],
        "cybersecurity": ["information security", "network security", "security"],
        
        # Engineering
        "electrical engineering": ["ee", "electronics"],
        "mechanical engineering": ["me"],
        "civil engineering": ["ce"],
        "chemical engineering": ["che"],
        "software engineering": ["se", "software development"],
        
        # Business
        "business administration": ["business", "management", "bba", "mba"],
        "finance": ["financial", "accounting", "economics"],
        "marketing": ["advertising", "sales", "branding"],
        
        # Sciences
        "mathematics": ["math", "stats", "statistics"],
        "physics": ["physical science"],
        "chemistry": ["chemical science"],
        "biology": ["life science", "biological"],
        
        # Arts & Humanities
        "english": ["literature", "writing", "communication"],
        "psychology": ["human behavior", "mental health"],
    }

    # Degree normalization mappings
    DEGREE_ALIASES = {
        "bachelor of science": ["b.sc", "bs", "b.s", "bsc"],
        "bachelor of arts": ["b.a", "ba", "b.a."],
        "master of science": ["m.sc", "ms", "m.s", "msc"],
        "master of arts": ["m.a", "ma", "m.a."],
        "master of business administration": ["mba", "m.b.a"],
        "doctor of philosophy": ["phd", "ph.d", "doctorate"],
        "associate degree": ["associate", "a.a", "a.s", "associate's"],
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
        for canonical, aliases in EducationScorer.DEGREE_ALIASES.items():
            if normalized in [alias.lower() for alias in aliases]:
                return canonical
            if normalized == canonical:
                return canonical
        
        return normalized

    @staticmethod
    def get_degree_level(degree: str) -> int:
        """
        Get the education level of a degree.

        Args:
            degree: Degree name string

        Returns:
            Integer level (1-6, higher = more advanced)
        """
        normalized = EducationScorer.normalize_degree(degree)
        
        for degree_name, level in EducationScorer.DEGREE_LEVELS.items():
            if normalized == degree_name or degree_name in normalized:
                return level
        
        return 0

    @staticmethod
    def normalize_field_of_study(field: str) -> str:
        """
        Normalize a field of study to its canonical category.

        Args:
            field: Raw field of study string

        Returns:
            Normalized field/category name
        """
        if not field:
            return ""

        normalized = field.lower().strip()
        normalized = re.sub(r'[^\w\s]', '', normalized)
        normalized = re.sub(r'\s+', ' ', normalized)
        
        # Check against field categories
        for category, variations in EducationScorer.FIELD_CATEGORIES.items():
            if normalized in [var.lower() for var in variations]:
                return category
            if category in normalized or normalized in category:
                return category
        
        return normalized

    @staticmethod
    def calculate_education_level_score(resume_degrees: list[dict]) -> float:
        """
        Calculate education level score based on highest degree.

        Args:
            resume_degrees: List of degree dicts

        Returns:
            Level score (0-100)
        """
        if not resume_degrees:
            return 0.0

        # Find highest degree level
        highest_level = 0
        for deg in resume_degrees:
            if isinstance(deg, dict):
                degree_name = deg.get("degree", "")
                level = EducationScorer.get_degree_level(degree_name)
                if level > highest_level:
                    highest_level = level

        # Score based on level (Bachelor's = 60, Master's = 80, PhD = 100)
        if highest_level >= 5:
            return 100.0
        elif highest_level == 4:
            return 80.0
        elif highest_level == 3:
            return 60.0
        elif highest_level == 2:
            return 40.0
        elif highest_level == 1:
            return 20.0
        else:
            return 0.0

    @staticmethod
    def calculate_education_completeness(resume_degrees: list[dict]) -> float:
        """
        Calculate education completeness score based on information provided.

        Args:
            resume_degrees: List of degree dicts

        Returns:
            Completeness score (0-100)
        """
        if not resume_degrees:
            return 0.0

        total_score = 0
        for deg in resume_degrees:
            if isinstance(deg, dict):
                score = 0
                # Check for required fields
                if deg.get("degree"):
                    score += 30
                if deg.get("field_of_study") or deg.get("field"):
                    score += 25
                if deg.get("institution"):
                    score += 25
                if deg.get("start_year") or deg.get("end_year"):
                    score += 20
                total_score += score

        # Average score across all degrees
        avg_score = total_score / len(resume_degrees)
        return round(avg_score, 2)

    @staticmethod
    def calculate_field_relevance(resume_degrees: list[dict]) -> float:
        """
        Calculate field of study relevance score.

        Args:
            resume_degrees: List of degree dicts

        Returns:
            Relevance score (0-100)
        """
        if not resume_degrees:
            return 0.0

        relevant_count = 0
        for deg in resume_degrees:
            if isinstance(deg, dict):
                field = deg.get("field_of_study") or deg.get("field", "")
                if field:
                    normalized = EducationScorer.normalize_field_of_study(field)
                    # Check if field matches a known category
                    for category in EducationScorer.FIELD_CATEGORIES.keys():
                        if normalized == category:
                            relevant_count += 1
                            break

        # Score based on proportion of relevant fields
        relevance = (relevant_count / len(resume_degrees)) * 100
        return round(relevance, 2)

    @staticmethod
    def calculate_education_presentation(resume_degrees: list[dict]) -> float:
        """
        Calculate education presentation score based on formatting and detail.

        Args:
            resume_degrees: List of degree dicts

        Returns:
            Presentation score (0-100)
        """
        if not resume_degrees:
            return 0.0

        score = 0.0

        # Check for multiple degrees (indicates comprehensive education)
        if len(resume_degrees) >= 1:
            score += 40.0
        if len(resume_degrees) >= 2:
            score += 20.0

        # Check for chronological order (years present)
        has_years = any(
            deg.get("start_year") or deg.get("end_year")
            for deg in resume_degrees
            if isinstance(deg, dict)
        )
        if has_years:
            score += 20.0

        # Check for grades/GPA (indicates academic performance)
        has_grade = any(
            deg.get("grade") or deg.get("gpa")
            for deg in resume_degrees
            if isinstance(deg, dict)
        )
        if has_grade:
            score += 20.0

        return round(score, 2)

    @staticmethod
    def extract_education_from_resume_analysis(resume_analysis: dict) -> list[dict]:
        """
        Extract education from resume analysis data.

        Args:
            resume_analysis: Dict containing resume analysis data with education field

        Returns:
            List of education dicts with degree, field, institution keys
        """
        education_list = []
        
        education = resume_analysis.get("education", [])
        if isinstance(education, list):
            for edu in education:
                if isinstance(edu, dict):
                    education_list.append({
                        "degree": edu.get("degree", ""),
                        "field_of_study": edu.get("field_of_study", ""),
                        "institution": edu.get("institution", ""),
                        "start_year": edu.get("start_year"),
                        "end_year": edu.get("end_year"),
                        "grade": edu.get("grade"),
                    })
        
        return education_list

    @staticmethod
    def get_education_analysis(resume_analysis: dict) -> dict:
        """
        Perform complete education quality analysis for resume.

        Args:
            resume_analysis: Resume analysis data

        Returns:
            Dict containing:
                - education_count: number of education entries
                - highest_degree: highest degree obtained
                - highest_degree_level: level of highest degree
                - education_level_score: level score (0-100)
                - education_completeness: completeness score (0-100)
                - field_relevance: relevance score (0-100)
                - education_presentation: presentation score (0-100)
                - overall_education_score: combined education score (0-100)
        """
        resume_degrees = EducationScorer.extract_education_from_resume_analysis(resume_analysis)

        # Find highest degree
        highest_degree = None
        highest_level = 0
        for deg in resume_degrees:
            if isinstance(deg, dict):
                degree_name = deg.get("degree", "")
                level = EducationScorer.get_degree_level(degree_name)
                if level > highest_level:
                    highest_level = level
                    highest_degree = degree_name

        level_score = EducationScorer.calculate_education_level_score(resume_degrees)
        completeness_score = EducationScorer.calculate_education_completeness(resume_degrees)
        relevance_score = EducationScorer.calculate_field_relevance(resume_degrees)
        presentation_score = EducationScorer.calculate_education_presentation(resume_degrees)

        # Overall education score: 35% level, 25% completeness, 25% relevance, 15% presentation
        overall_score = (
            level_score * 0.35 +
            completeness_score * 0.25 +
            relevance_score * 0.25 +
            presentation_score * 0.15
        )

        return {
            "education_count": len(resume_degrees),
            "highest_degree": highest_degree,
            "highest_degree_level": highest_level,
            "education_level_score": level_score,
            "education_completeness": completeness_score,
            "field_relevance": relevance_score,
            "education_presentation": presentation_score,
            "overall_education_score": round(overall_score, 2),
        }
