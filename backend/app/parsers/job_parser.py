"""
Job Parser - Extracts structured information from job descriptions
"""

import re
from typing import Any


class JobParser:
    """Parses job description text into structured data."""

    # Section headers commonly found in job descriptions
    SECTION_PATTERNS = {
        "skills": [
            r"(?:required\s+)?skills?(?:\s*(?:required|qualifications|technologies|stack))?",
            r"technical\s+skills?",
            r"key\s+skills?",
            r"must\s+have",
            r"requirements\s*[:\n]",
        ],
        "experience": [
            r"experience(?:\s+requirements)?",
            r"work\s+experience",
            r"professional\s+experience",
            r"years\s+of\s+experience",
        ],
        "education": [
            r"education(?:\s+requirements)?",
            r"educational\s+requirements",
            r"qualifications",
            r"degree\s+requirements",
        ],
        "responsibilities": [
            r"responsibilities",
            r"duties",
            r"what\s+you['']ll\s+do",
            r"role\s+overview",
            r"job\s+summary",
        ],
        "preferred": [
            r"preferred\s+skills?",
            r"nice\s+to\s+have",
            r"bonus\s+points?",
            r"additional\s+skills?",
        ],
    }

    # Common skill indicators
    SKILL_INDICATORS = [
        r"proficient\s+in",
        r"experience\s+with",
        r"knowledge\s+of",
        r"familiar\s+with",
        r"expertise\s+in",
    ]

    # Experience patterns
    EXPERIENCE_PATTERNS = [
        r"(\d+)\+?\s*years?\s*(?:of\s*)?(?:experience)?",
        r"(\d+)\s*-\s*(\d+)\s*years?",
        r"entry\s*level",
        r"mid\s*level",
        r"senior\s*level",
        r"lead",
        r"manager",
    ]

    # Education patterns
    EDUCATION_PATTERNS = [
        r"(?:bachelor'?s?|b\.?s\.?c\.?|b\.?s\.?)\s*(?:degree)?",
        r"(?:master'?s?|m\.?s\.?c\.?|m\.?s\.?)\s*(?:degree)?",
        r"(?:phd|ph\.?d\.?|doctorate)",
        r"(?:mba|m\.?b\.?a\.?)",
        r"(?:associate'?s?|a\.?a\.?)\s*(?:degree)?",
        r"(?:diploma|certificate)",
        r"bachelor'?s?\s+degree",
        r"master'?s?\s+degree",
    ]

    @staticmethod
    def parse_job_description(job_description: str) -> dict[str, Any]:
        """
        Parse job description text into structured data.

        Args:
            job_description: Raw job description text

        Returns:
            Dict with extracted fields:
                - required_skills: list of required skills
                - required_experience: extracted experience requirements
                - required_education: extracted education requirements
                - responsibilities: list of responsibilities
                - preferred_skills: list of preferred skills
        """
        if not job_description:
            return {
                "required_skills": [],
                "required_experience": None,
                "required_education": None,
                "responsibilities": [],
                "preferred_skills": [],
            }

        # Normalize text
        text = job_description.strip()
        text = re.sub(r'\s+', ' ', text)

        # Extract each section
        required_skills = JobParser._extract_skills(text, required=True)
        preferred_skills = JobParser._extract_skills(text, required=False)
        required_experience = JobParser._extract_experience(text)
        required_education = JobParser._extract_education(text)
        responsibilities = JobParser._extract_responsibilities(text)

        return {
            "required_skills": required_skills,
            "required_experience": required_experience,
            "required_education": required_education,
            "responsibilities": responsibilities,
            "preferred_skills": preferred_skills,
        }

    @staticmethod
    def _extract_skills(text: str, required: bool = True) -> list[str]:
        """Extract skills from job description text."""
        skills = []

        # Try to find the skills section
        skills_section = JobParser._find_section(text, "skills")
        if not skills_section:
            skills_section = text  # If no section found, search entire text

        # Common skill keywords to look for
        tech_keywords = [
            "python", "java", "javascript", "typescript", "c\+\+", "c#", "go", "rust",
            "react", "angular", "vue", "nodejs", "django", "flask", "spring", "express",
            "sql", "nosql", "mongodb", "postgresql", "mysql", "redis", "elasticsearch",
            "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "git",
            "machine learning", "deep learning", "ai", "data science", "tensorflow", "pytorch",
            "html", "css", "rest api", "graphql", "microservices",
            "agile", "scrum", "ci/cd", "devops", "linux", "bash",
        ]

        # Look for skill keywords in the text
        text_lower = skills_section.lower()
        for keyword in tech_keywords:
            if keyword in text_lower:
                skills.append(keyword.title() if keyword.isalpha() else keyword)

        # Also extract from comma-separated lists
        comma_separated = re.findall(r'[A-Z][a-zA-Z\+\#\.]*\s*(?:,\s*[A-Z][a-zA-Z\+\#\.]*)+', skills_section)
        for match in comma_separated:
            items = [item.strip() for item in match.split(',')]
            for item in items:
                if len(item) >= 2 and item not in skills:
                    skills.append(item)

        # If looking for preferred skills, also check for "preferred" keywords
        if not required:
            preferred_section = JobParser._find_section(text, "preferred")
            if preferred_section:
                preferred_section_lower = preferred_section.lower()
                for keyword in tech_keywords:
                    if keyword in preferred_section_lower and keyword not in [s.lower() for s in skills]:
                        skills.append(keyword.title() if keyword.isalpha() else keyword)

        # Remove duplicates while preserving order
        seen = set()
        unique_skills = []
        for skill in skills:
            skill_lower = skill.lower()
            if skill_lower not in seen:
                seen.add(skill_lower)
                unique_skills.append(skill)

        return unique_skills

    @staticmethod
    def _extract_experience(text: str) -> str | None:
        """Extract experience requirements from job description."""
        experience_section = JobParser._find_section(text, "experience")
        if not experience_section:
            experience_section = text

        # Look for year patterns
        for pattern in JobParser.EXPERIENCE_PATTERNS:
            match = re.search(pattern, experience_section, re.IGNORECASE)
            if match:
                if match.groups():
                    return match.group(0).strip()

        # Look for level patterns
        if "entry level" in experience_section.lower():
            return "Entry Level"
        elif "mid level" in experience_section.lower() or "mid-level" in experience_section.lower():
            return "Mid Level"
        elif "senior" in experience_section.lower():
            return "Senior"
        elif "lead" in experience_section.lower():
            return "Lead"
        elif "manager" in experience_section.lower():
            return "Manager"

        return None

    @staticmethod
    def _extract_education(text: str) -> str | None:
        """Extract education requirements from job description."""
        education_section = JobParser._find_section(text, "education")
        if not education_section:
            education_section = text

        # Look for degree patterns
        for pattern in JobParser.EDUCATION_PATTERNS:
            match = re.search(pattern, education_section, re.IGNORECASE)
            if match:
                return match.group(0).strip()

        return None

    @staticmethod
    def _extract_responsibilities(text: str) -> list[str]:
        """Extract responsibilities from job description."""
        responsibilities_section = JobParser._find_section(text, "responsibilities")
        if not responsibilities_section:
            responsibilities_section = text

        responsibilities = []

        # Split by bullet points or numbered lists
        lines = responsibilities_section.split('\n')
        for line in lines:
            line = line.strip()
            # Remove bullet points
            line = re.sub(r'^[\*\-\•\d+\.]+\s*', '', line)
            # Filter out headers and very short lines
            if line and len(line) > 15 and not any(header in line.lower() for header in ["responsibilities", "duties", "what you'll", "role overview", "job summary"]):
                responsibilities.append(line)

        # If no bullet points found, try splitting by periods for simple descriptions
        if not responsibilities and len(responsibilities_section) < 500:
            sentences = re.split(r'[.!?]', responsibilities_section)
            for sentence in sentences:
                sentence = sentence.strip()
                # Filter out very short sentences and headers
                if sentence and len(sentence) > 20 and not any(header in sentence.lower() for header in ["responsibilities", "duties", "what you'll", "role overview", "job summary", "skills", "experience", "education"]):
                    responsibilities.append(sentence)

        return responsibilities[:10]  # Limit to top 10 responsibilities

    @staticmethod
    def _find_section(text: str, section_type: str) -> str | None:
        """Find a specific section in the job description text."""
        patterns = JobParser.SECTION_PATTERNS.get(section_type, [])
        text_lower = text.lower()

        for pattern in patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE)
            if match:
                start_pos = match.start()
                # Find the end of this section (next section header or end of text)
                end_pos = len(text)
                for other_section in JobParser.SECTION_PATTERNS:
                    if other_section != section_type:
                        for other_pattern in JobParser.SECTION_PATTERNS[other_section]:
                            other_match = re.search(other_pattern, text_lower[start_pos + 1:], re.IGNORECASE)
                            if other_match:
                                end_pos = start_pos + 1 + other_match.start()
                                break
                        if end_pos < len(text):
                            break

                section_text = text[start_pos:end_pos].strip()
                # Remove the header line
                lines = section_text.split('\n')
                if len(lines) > 1:
                    return '\n'.join(lines[1:]).strip()
                return section_text

        return None
