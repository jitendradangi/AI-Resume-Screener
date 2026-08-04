"""
Format Scorer – ATS Format Quality Analysis
==========================================
Analyzes and scores resume format for resume quality ATS evaluation.
Evaluates document structure, section organization, readability, and ATS-friendliness.
"""

import re


class FormatScorer:
    """Analyzes and scores resume format for resume quality ATS evaluation."""

    # Minimum section counts for a well-formatted resume
    MINIMUM_SECTIONS = 3
    IDEAL_SECTIONS = 6

    # Section names to identify different parts of resume
    COMMON_SECTIONS = {
        "summary": ["summary", "profile", "objective", "about", "professional summary"],
        "experience": ["experience", "work experience", "employment", "work history", "professional experience"],
        "education": ["education", "academic", "qualifications", "educational background"],
        "skills": ["skills", "technical skills", "competencies", "expertise", "technologies"],
        "projects": ["projects", "portfolio", "work samples", "key projects"],
        "certifications": ["certifications", "certificates", "credentials", "licenses"],
        "languages": ["languages", "language proficiency"],
        "awards": ["awards", "honors", "achievements", "recognition"],
    }

    @staticmethod
    def get_format_analysis(resume_analysis: dict) -> dict:
        """
        Analyze resume format and calculate format quality score.

        Args:
            resume_analysis: Dict containing resume analysis data with keys:
                - skills: list of skills
                - experience: list of experience dicts
                - projects: list of project dicts
                - education: list of education dicts
                - raw_text: raw resume text

        Returns:
            Dict with format analysis results including:
                - overall_format_score: Overall format score (0-100)
                - section_structure_score: Score for section organization
                - readability_score: Score for text readability
                - completeness_score: Score for information completeness
                - format_issues: List of identified format issues
                - format_recommendations: List of improvement recommendations
        """
        issues = []
        recommendations = []

        # Calculate individual format scores
        section_score = FormatScorer._calculate_section_structure(resume_analysis, issues, recommendations)
        readability_score = FormatScorer._calculate_readability(resume_analysis, issues, recommendations)
        completeness_score = FormatScorer._calculate_completeness(resume_analysis, issues, recommendations)

        # Calculate overall format score (weighted average)
        overall_score = (
            section_score * 0.40 +
            readability_score * 0.35 +
            completeness_score * 0.25
        )

        return {
            "overall_format_score": round(overall_score, 2),
            "section_structure_score": round(section_score, 2),
            "readability_score": round(readability_score, 2),
            "completeness_score": round(completeness_score, 2),
            "format_issues": issues,
            "format_recommendations": recommendations,
        }

    @staticmethod
    def _calculate_section_structure(resume_analysis: dict, issues: list, recommendations: list) -> float:
        """
        Calculate section structure score based on organization and presence of key sections.

        Args:
            resume_analysis: Resume analysis data
            issues: List to append identified issues
            recommendations: List to append recommendations

        Returns:
            Section structure score (0-100)
        """
        score = 0.0
        sections_present = set()

        # Check for key sections
        if resume_analysis.get("experience") and len(resume_analysis["experience"]) > 0:
            sections_present.add("experience")
            score += 25.0
        else:
            issues.append("Missing or empty experience section")
            recommendations.append("Add detailed work experience with job titles, companies, and dates")

        if resume_analysis.get("education") and len(resume_analysis["education"]) > 0:
            sections_present.add("education")
            score += 25.0
        else:
            issues.append("Missing or empty education section")
            recommendations.append("Include education details with degrees, institutions, and graduation dates")

        if resume_analysis.get("skills") and len(resume_analysis["skills"]) > 0:
            sections_present.add("skills")
            score += 20.0
        else:
            issues.append("Missing or empty skills section")
            recommendations.append("Add a skills section highlighting relevant technical and soft skills")

        if resume_analysis.get("projects") and len(resume_analysis["projects"]) > 0:
            sections_present.add("projects")
            score += 15.0
        else:
            recommendations.append("Consider adding a projects section to showcase practical work")

        # Bonus for additional sections
        if len(sections_present) >= 4:
            score += 15.0

        return min(score, 100.0)

    @staticmethod
    def _calculate_readability(resume_analysis: dict, issues: list, recommendations: list) -> float:
        """
        Calculate readability score based on text structure and clarity.

        Args:
            resume_analysis: Resume analysis data
            issues: List to append identified issues
            recommendations: List to append recommendations

        Returns:
            Readability score (0-100)
        """
        score = 0.0
        raw_text = resume_analysis.get("raw_text", "")

        if not raw_text:
            issues.append("No raw text available for readability analysis")
            return 0.0

        # Check text length
        word_count = len(re.findall(r'\b\w+\b', raw_text))
        if word_count < 200:
            issues.append("Resume text is too short (less than 200 words)")
            recommendations.append("Expand your resume with more detailed descriptions of your experience and skills")
            score += 20.0
        elif word_count < 400:
            score += 50.0
        elif word_count <= 800:
            score += 100.0
        else:
            score += 80.0  # Too long might indicate verbosity
            recommendations.append("Consider condensing your resume to focus on most relevant information")

        # Check for proper paragraph structure
        paragraphs = [p.strip() for p in raw_text.split('\n\n') if p.strip()]
        if len(paragraphs) < 3:
            issues.append("Poor paragraph structure - resume lacks proper text organization")
            recommendations.append("Organize content into clear paragraphs for better readability")
            score -= 20.0
        else:
            score += 10.0

        # Check for bullet points or list items
        bullet_patterns = [r'•', r'-', r'\*', r'\d+\.', r'→']
        has_bullets = any(re.search(pattern, raw_text) for pattern in bullet_patterns)
        if has_bullets:
            score += 20.0
        else:
            recommendations.append("Use bullet points to list skills, responsibilities, and achievements")

        # Check for excessive capitalization (all caps)
        all_caps_words = re.findall(r'\b[A-Z]{2,}\b', raw_text)
        if len(all_caps_words) > 10:
            issues.append("Excessive use of ALL CAPS text")
            recommendations.append("Minimize use of all caps text for better readability")
            score -= 15.0

        return max(0.0, min(score, 100.0))

    @staticmethod
    def _calculate_completeness(resume_analysis: dict, issues: list, recommendations: list) -> float:
        """
        Calculate completeness score based on information density and detail level.

        Args:
            resume_analysis: Resume analysis data
            issues: List to append identified issues
            recommendations: List to append recommendations

        Returns:
            Completeness score (0-100)
        """
        score = 0.0

        # Check experience completeness
        experiences = resume_analysis.get("experience", [])
        if experiences:
            complete_exp = 0
            for exp in experiences:
                if isinstance(exp, dict):
                    if exp.get("title") and exp.get("company"):
                        complete_exp += 1
                    if exp.get("description") and len(exp["description"]) > 20:
                        complete_exp += 1
            exp_score = (complete_exp / (len(experiences) * 2)) * 100 if experiences else 0
            score += exp_score * 0.4
            if exp_score < 50:
                issues.append("Experience entries lack complete information")
                recommendations.append("Ensure each experience entry includes job title, company, and detailed description")
        else:
            issues.append("No experience information provided")
            recommendations.append("Add work experience with complete details for each position")

        # Check education completeness
        education = resume_analysis.get("education", [])
        if education:
            complete_edu = 0
            for edu in education:
                if isinstance(edu, dict):
                    if edu.get("degree") and edu.get("institution"):
                        complete_edu += 1
                    if edu.get("field_of_study") or edu.get("field"):
                        complete_edu += 1
            edu_score = (complete_edu / (len(education) * 2)) * 100 if education else 0
            score += edu_score * 0.3
            if edu_score < 50:
                issues.append("Education entries lack complete information")
                recommendations.append("Include degree, institution, and field of study for each education entry")
        else:
            issues.append("No education information provided")
            recommendations.append("Add education details with degree, institution, and field of study")

        # Check skills completeness
        skills = resume_analysis.get("skills", [])
        if skills and len(skills) >= 5:
            score += 30.0
        elif skills:
            score += 15.0
            recommendations.append("Add more skills to demonstrate broader expertise")
        else:
            issues.append("No skills information provided")
            recommendations.append("Add a comprehensive skills section")

        return round(score, 2)
