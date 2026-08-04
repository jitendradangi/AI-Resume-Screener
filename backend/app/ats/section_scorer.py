"""
Section Scorer – ATS Section Completeness Analysis
==================================================
Analyzes and scores resume section completeness for resume quality ATS evaluation.
Evaluates presence of standard ATS sections: Summary, Skills, Experience, Education, Projects, Certifications.
"""

import re


class SectionScorer:
    """Analyzes and scores resume section completeness for resume quality ATS evaluation."""

    # Standard ATS sections that resumes should contain
    STANDARD_SECTIONS = {
        "summary": {
            "names": ["summary", "profile", "objective", "about", "professional summary", "career summary"],
            "importance": "high",
            "description": "Professional summary or career objective"
        },
        "skills": {
            "names": ["skills", "technical skills", "competencies", "expertise", "technologies", "core skills"],
            "importance": "high",
            "description": "Skills section"
        },
        "experience": {
            "names": ["experience", "work experience", "employment", "work history", "professional experience", "career history"],
            "importance": "high",
            "description": "Work experience section"
        },
        "education": {
            "names": ["education", "academic", "qualifications", "educational background", "academic background"],
            "importance": "high",
            "description": "Education section"
        },
        "projects": {
            "names": ["projects", "portfolio", "work samples", "key projects", "project experience"],
            "importance": "medium",
            "description": "Projects section"
        },
        "certifications": {
            "names": ["certifications", "certificates", "credentials", "licenses", "professional certifications"],
            "importance": "medium",
            "description": "Certifications section"
        },
    }

    @staticmethod
    def get_section_analysis(resume_analysis: dict) -> dict:
        """
        Analyze resume section completeness and calculate section score.

        Args:
            resume_analysis: Dict containing resume analysis data with keys:
                - skills: list of skills
                - experience: list of experience dicts
                - projects: list of project dicts
                - education: list of education dicts
                - raw_text: raw resume text

        Returns:
            Dict with section analysis results including:
                - overall_section_score: Overall section completeness score (0-100)
                - missing_sections: List of missing high-importance sections
                - present_sections: List of sections that are present
                - optional_sections_present: List of optional sections present
                - section_issues: List of identified section issues
                - section_recommendations: List of improvement recommendations
        """
        missing_sections = []
        present_sections = []
        optional_sections_present = []
        issues = []
        recommendations = []

        # Check for high-importance sections
        # Skills
        if resume_analysis.get("skills") and len(resume_analysis["skills"]) > 0:
            present_sections.append("skills")
        else:
            missing_sections.append("skills")
            issues.append("Missing skills section")
            recommendations.append("Add a skills section to highlight your technical and soft skills")

        # Experience
        if resume_analysis.get("experience") and len(resume_analysis["experience"]) > 0:
            present_sections.append("experience")
        else:
            missing_sections.append("experience")
            issues.append("Missing experience section")
            recommendations.append("Add a work experience section with your employment history")

        # Education
        if resume_analysis.get("education") and len(resume_analysis["education"]) > 0:
            present_sections.append("education")
        else:
            missing_sections.append("education")
            issues.append("Missing education section")
            recommendations.append("Add an education section with your academic background")

        # Projects (medium importance)
        if resume_analysis.get("projects") and len(resume_analysis["projects"]) > 0:
            present_sections.append("projects")
            optional_sections_present.append("projects")
        else:
            recommendations.append("Consider adding a projects section to showcase your practical work")

        # Check for summary in raw text
        raw_text = resume_analysis.get("raw_text", "").lower()
        summary_found = False
        for summary_name in SectionScorer.STANDARD_SECTIONS["summary"]["names"]:
            if summary_name in raw_text:
                present_sections.append("summary")
                summary_found = True
                break

        if not summary_found:
            missing_sections.append("summary")
            issues.append("Missing professional summary section")
            recommendations.append("Add a professional summary at the top of your resume to provide an overview")

        # Check for certifications in raw text (medium importance)
        certifications_found = False
        for cert_name in SectionScorer.STANDARD_SECTIONS["certifications"]["names"]:
            if cert_name in raw_text:
                present_sections.append("certifications")
                optional_sections_present.append("certifications")
                certifications_found = True
                break

        if not certifications_found:
            recommendations.append("Consider adding a certifications section if you have relevant professional certifications")

        # Calculate section score
        # High-importance sections: summary, skills, experience, education (4 sections)
        # Medium-importance sections: projects, certifications (2 sections)
        high_importance_present = len([s for s in present_sections if SectionScorer.STANDARD_SECTIONS.get(s, {}).get("importance") == "high"])
        medium_importance_present = len([s for s in present_sections if SectionScorer.STANDARD_SECTIONS.get(s, {}).get("importance") == "medium"])

        # Score calculation: High importance sections carry more weight
        # 4 high-importance sections * 20 points each = 80 points max
        # 2 medium-importance sections * 10 points each = 20 points max
        # Total = 100 points
        high_importance_score = (high_importance_present / 4) * 80
        medium_importance_score = (medium_importance_present / 2) * 10
        overall_score = high_importance_score + medium_importance_score

        return {
            "overall_section_score": round(overall_score, 2),
            "missing_sections": missing_sections,
            "present_sections": present_sections,
            "optional_sections_present": optional_sections_present,
            "section_issues": issues,
            "section_recommendations": recommendations,
        }

    @staticmethod
    def detect_section_in_text(raw_text: str, section_names: list[str]) -> bool:
        """
        Detect if a section exists in the raw text based on section names.

        Args:
            raw_text: Raw resume text
            section_names: List of possible section names to look for

        Returns:
            True if section is found, False otherwise
        """
        if not raw_text:
            return False

        text_lower = raw_text.lower()
        for section_name in section_names:
            # Look for section name as a standalone word/phrase (not part of another word)
            pattern = r'\b' + re.escape(section_name) + r'\b'
            if re.search(pattern, text_lower):
                return True

        return False

    @staticmethod
    def get_section_content_quality(resume_analysis: dict, section_type: str) -> dict:
        """
        Evaluate the quality of content within a specific section.

        Args:
            resume_analysis: Resume analysis data
            section_type: Type of section to evaluate (skills, experience, education, projects)

        Returns:
            Dict with quality metrics for the section
        """
        quality = {
            "has_content": False,
            "item_count": 0,
            "detail_level": "none",
            "score": 0.0
        }

        if section_type == "skills":
            skills = resume_analysis.get("skills", [])
            if skills and len(skills) > 0:
                quality["has_content"] = True
                quality["item_count"] = len(skills)
                if len(skills) >= 10:
                    quality["detail_level"] = "high"
                    quality["score"] = 100.0
                elif len(skills) >= 5:
                    quality["detail_level"] = "medium"
                    quality["score"] = 70.0
                else:
                    quality["detail_level"] = "low"
                    quality["score"] = 40.0

        elif section_type == "experience":
            experiences = resume_analysis.get("experience", [])
            if experiences and len(experiences) > 0:
                quality["has_content"] = True
                quality["item_count"] = len(experiences)
                detailed_count = 0
                for exp in experiences:
                    if isinstance(exp, dict):
                        desc = exp.get("description", "")
                        if desc and len(desc) > 50:
                            detailed_count += 1

                if detailed_count == len(experiences) and len(experiences) >= 2:
                    quality["detail_level"] = "high"
                    quality["score"] = 100.0
                elif detailed_count >= len(experiences) / 2:
                    quality["detail_level"] = "medium"
                    quality["score"] = 70.0
                else:
                    quality["detail_level"] = "low"
                    quality["score"] = 40.0

        elif section_type == "education":
            education = resume_analysis.get("education", [])
            if education and len(education) > 0:
                quality["has_content"] = True
                quality["item_count"] = len(education)
                complete_count = 0
                for edu in education:
                    if isinstance(edu, dict):
                        if edu.get("degree") and edu.get("institution"):
                            complete_count += 1

                if complete_count == len(education):
                    quality["detail_level"] = "high"
                    quality["score"] = 100.0
                elif complete_count >= len(education) / 2:
                    quality["detail_level"] = "medium"
                    quality["score"] = 70.0
                else:
                    quality["detail_level"] = "low"
                    quality["score"] = 40.0

        elif section_type == "projects":
            projects = resume_analysis.get("projects", [])
            if projects and len(projects) > 0:
                quality["has_content"] = True
                quality["item_count"] = len(projects)
                detailed_count = 0
                for proj in projects:
                    if isinstance(proj, dict):
                        desc = proj.get("description", "")
                        if desc and len(desc) > 30:
                            detailed_count += 1

                if detailed_count == len(projects) and len(projects) >= 2:
                    quality["detail_level"] = "high"
                    quality["score"] = 100.0
                elif detailed_count >= len(projects) / 2:
                    quality["detail_level"] = "medium"
                    quality["score"] = 70.0
                else:
                    quality["detail_level"] = "low"
                    quality["score"] = 40.0

        return quality
