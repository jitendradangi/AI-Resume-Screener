"""
KeywordExtractor – ATS Keyword Analysis
========================================
Extracts and analyzes keywords from resumes for resume quality ATS scoring.
Provides keyword density, variety, and relevance metrics for resume evaluation.
"""

import re
from collections import Counter


class KeywordExtractor:
    """Extracts and analyzes keywords for resume quality ATS scoring."""

    # Common technical keywords for resume quality assessment
    TECH_KEYWORDS = {
        "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
        "react", "angular", "vue", "nodejs", "django", "flask", "spring", "express",
        "sql", "nosql", "mongodb", "postgresql", "mysql", "redis", "elasticsearch",
        "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ansible",
        "git", "github", "gitlab", "ci/cd", "jenkins", "travis", "circleci",
        "machine learning", "deep learning", "nlp", "data science", "ai", "ml",
        "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy",
        "agile", "scrum", "kanban", "jira", "confluence", "slack",
        "rest api", "graphql", "microservices", "soa", "grpc",
        "html", "css", "sass", "less", "webpack", "vite",
        "linux", "unix", "bash", "shell", "powershell",
        "testing", "unit testing", "integration testing", "e2e", "selenium", "jest",
        "security", "oauth", "jwt", "authentication", "authorization",
    }

    # Common action verbs and soft skills
    SOFT_KEYWORDS = {
        "leadership", "communication", "teamwork", "problem solving",
        "analytical", "critical thinking", "collaboration", "adaptability",
        "time management", "organization", "planning", "strategic",
        "mentoring", "coaching", "presentation", "negotiation",
    }

    @staticmethod
    def extract_from_resume(resume_analysis: dict) -> set[str]:
        """
        Extract keywords from resume analysis data.

        Args:
            resume_analysis: Dict containing resume analysis data with keys:
                - skills: list of skills
                - experience: list of experience dicts
                - projects: list of project dicts
                - education: list of education dicts
                - raw_text: raw resume text

        Returns:
            Set of extracted keywords (normalized to lowercase)
        """
        keywords = set()

        # Extract from skills list
        skills = resume_analysis.get("skills", [])
        if isinstance(skills, list):
            for skill in skills:
                if isinstance(skill, str):
                    keywords.update(KeywordExtractor._normalize_keywords(skill))
                elif isinstance(skill, dict):
                    keywords.update(KeywordExtractor._normalize_keywords(skill.get("name", "")))

        # Extract from experience
        experiences = resume_analysis.get("experience", [])
        if isinstance(experiences, list):
            for exp in experiences:
                if isinstance(exp, dict):
                    description = exp.get("description", "")
                    keywords.update(KeywordExtractor._extract_text_keywords(description))

        # Extract from projects
        projects = resume_analysis.get("projects", [])
        if isinstance(projects, list):
            for project in projects:
                if isinstance(project, dict):
                    description = project.get("description", "")
                    technologies = project.get("technologies", [])
                    keywords.update(KeywordExtractor._extract_text_keywords(description))
                    if isinstance(technologies, list):
                        for tech in technologies:
                            keywords.update(KeywordExtractor._normalize_keywords(tech))

        # Extract from raw text as fallback
        raw_text = resume_analysis.get("raw_text", "")
        if raw_text:
            keywords.update(KeywordExtractor._extract_text_keywords(raw_text))

        return keywords

    @staticmethod
    def calculate_keyword_density(resume_keywords: set[str], raw_text: str) -> float:
        """
        Calculate keyword density in resume text.

        Args:
            resume_keywords: Set of extracted keywords
            raw_text: Raw resume text

        Returns:
            Keyword density score (0-100)
        """
        if not raw_text or not resume_keywords:
            return 0.0

        # Count total words in text
        words = re.findall(r'\b\w+\b', raw_text.lower())
        total_words = len(words)

        if total_words == 0:
            return 0.0

        # Count keyword occurrences
        keyword_count = 0
        text_lower = raw_text.lower()
        for keyword in resume_keywords:
            keyword_count += text_lower.count(keyword)

        # Calculate density (keywords per 100 words)
        density = (keyword_count / total_words) * 100

        # Cap at reasonable maximum (e.g., 15% density = 100 score)
        score = min((density / 15) * 100, 100)

        return round(score, 2)

    @staticmethod
    def calculate_keyword_variety(resume_keywords: set[str]) -> float:
        """
        Calculate keyword variety score based on number of unique keywords.

        Args:
            resume_keywords: Set of extracted keywords

        Returns:
            Variety score (0-100)
        """
        if not resume_keywords:
            return 0.0

        # More unique keywords = higher score (up to 30 keywords for max score)
        unique_count = len(resume_keywords)
        score = min((unique_count / 30) * 100, 100)

        return round(score, 2)

    @staticmethod
    def calculate_keyword_quality(resume_keywords: set[str]) -> dict:
        """
        Assess keyword quality based on technical vs soft skill balance.

        Args:
            resume_keywords: Set of extracted keywords

        Returns:
            Dict with tech_count, soft_count, and quality_score
        """
        if not resume_keywords:
            return {
                "tech_count": 0,
                "soft_count": 0,
                "quality_score": 0.0,
            }

        tech_count = len(resume_keywords.intersection(KeywordExtractor.TECH_KEYWORDS))
        soft_count = len(resume_keywords.intersection(KeywordExtractor.SOFT_KEYWORDS))

        # Quality score: balance of technical and soft skills
        # Ideal ratio: 70% technical, 30% soft
        total_relevant = tech_count + soft_count
        if total_relevant == 0:
            quality_score = 0.0
        else:
            tech_ratio = tech_count / total_relevant
            ideal_ratio = 0.7
            ratio_score = max(0, 1 - abs(tech_ratio - ideal_ratio) / ideal_ratio) * 100
            quantity_score = min((total_relevant / 20) * 100, 100)
            quality_score = (ratio_score * 0.6) + (quantity_score * 0.4)

        return {
            "tech_count": tech_count,
            "soft_count": soft_count,
            "quality_score": round(quality_score, 2),
        }

    @staticmethod
    def _normalize_keywords(text: str) -> set[str]:
        """
        Normalize text to extract individual keywords.

        Args:
            text: Input text string

        Returns:
            Set of normalized keywords (lowercase, alphanumeric)
        """
        if not text:
            return set()

        # Convert to lowercase
        text = text.lower()
        
        # Split by common separators
        keywords = re.split(r'[,;\/\|\-\s]+', text)
        
        # Remove empty strings and normalize
        normalized = set()
        for keyword in keywords:
            keyword = keyword.strip()
            if keyword and len(keyword) > 1:
                # Remove special characters but keep alphanumeric
                keyword = re.sub(r'[^a-z0-9]', '', keyword)
                if keyword:
                    normalized.add(keyword)
        
        return normalized

    @staticmethod
    def _extract_text_keywords(text: str) -> set[str]:
        """
        Extract keywords from text using predefined keyword lists.

        Args:
            text: Input text string

        Returns:
            Set of found keywords
        """
        if not text:
            return set()

        text_lower = text.lower()
        keywords = set()

        # Check for technical keywords
        for tech_keyword in KeywordExtractor.TECH_KEYWORDS:
            if tech_keyword in text_lower:
                keywords.add(tech_keyword.replace(' ', '_'))

        # Check for soft skill keywords
        for soft_keyword in KeywordExtractor.SOFT_KEYWORDS:
            if soft_keyword in text_lower:
                keywords.add(soft_keyword.replace(' ', '_'))

        # Extract individual words that might be keywords
        words = re.findall(r'\b[a-z]{3,}\b', text_lower)
        keywords.update(words)

        return keywords

    @staticmethod
    def get_keyword_analysis(resume_analysis: dict) -> dict:
        """
        Perform complete keyword analysis for resume quality assessment.

        Args:
            resume_analysis: Resume analysis data

        Returns:
            Dict containing:
                - resume_keywords: set of resume keywords
                - keyword_density: density score (0-100)
                - keyword_variety: variety score (0-100)
                - keyword_quality: dict with tech/soft counts and quality score
                - overall_keyword_score: combined keyword score (0-100)
        """
        resume_keywords = KeywordExtractor.extract_from_resume(resume_analysis)
        raw_text = resume_analysis.get("raw_text", "")

        density_score = KeywordExtractor.calculate_keyword_density(resume_keywords, raw_text)
        variety_score = KeywordExtractor.calculate_keyword_variety(resume_keywords)
        quality_analysis = KeywordExtractor.calculate_keyword_quality(resume_keywords)

        # Overall keyword score: 40% density, 30% variety, 30% quality
        overall_score = (
            density_score * 0.40 +
            variety_score * 0.30 +
            quality_analysis["quality_score"] * 0.30
        )

        return {
            "resume_keywords": list(resume_keywords),
            "keyword_count": len(resume_keywords),
            "keyword_density": density_score,
            "keyword_variety": variety_score,
            "keyword_quality": quality_analysis,
            "overall_keyword_score": round(overall_score, 2),
        }
