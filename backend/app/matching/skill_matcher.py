"""
Skill Matcher – Job-Resume Skill Compatibility Analysis
=====================================================
Compares resume skills with job required skills to determine candidate-job compatibility.
Normalizes skills, handles aliases, and calculates match scores.
"""

import re


class SkillMatcher:
    """Analyzes skill compatibility between resumes and job requirements."""

    # Skill normalization mappings - common variations
    SKILL_ALIASES = {
        # Programming Languages
        "javascript": ["js", "ecmascript", "es6", "es2015"],
        "typescript": ["ts"],
        "python": ["py", "python3"],
        "java": ["java se", "java ee"],
        "c#": ["csharp", "c-sharp"],
        "c++": ["cpp", "c-plus-plus"],
        "go": ["golang", "go-lang"],
        "rust": ["rust-lang"],
        
        # Frameworks & Libraries
        "react": ["reactjs", "react.js", "reactjs", "react.js"],
        "angular": ["angularjs", "angular.js", "angular2", "angular 2+"],
        "vue": ["vuejs", "vue.js", "vuejs"],
        "nodejs": ["node.js", "node", "node-js"],
        "express": ["express.js", "expressjs"],
        "django": ["django-rest-framework", "drf"],
        "flask": ["flask-restful"],
        "spring": ["spring boot", "springboot"],
        
        # Databases
        "postgresql": ["postgres", "psql"],
        "mysql": ["mysql-server"],
        "mongodb": ["mongo", "mongo-db"],
        "sql server": ["mssql", "microsoft sql server"],
        "oracle": ["oracle db", "oracle database"],
        
        # Cloud & DevOps
        "aws": ["amazon web services", "amazon aws"],
        "azure": ["microsoft azure"],
        "gcp": ["google cloud platform", "google cloud"],
        "docker": ["docker-container", "containers"],
        "kubernetes": ["k8s", "k8"],
        "terraform": ["tf", "infrastructure as code", "iac"],
        
        # Tools & Platforms
        "git": ["version control", "vcs"],
        "jenkins": ["ci/cd", "cicd", "continuous integration"],
        "jira": ["jira software", "atlassian jira"],
        
        # Data Science & ML
        "machine learning": ["ml", "machine-learning"],
        "deep learning": ["dl", "deep-learning"],
        "data science": ["ds", "data-science"],
        "tensorflow": ["tf"],
        "pytorch": ["torch"],
        "scikit-learn": ["sklearn", "scikit"],
        
        # Web Technologies
        "html": ["html5", "hyper text markup language"],
        "css": ["css3", "cascading style sheets"],
        "rest api": ["rest", "restful", "restful api"],
        "graphql": ["gql", "graph ql"],
        
        # Testing
        "selenium": ["webdriver", "browser automation"],
        "jest": ["jest testing", "jestjs"],
        
        # Security
        "oauth": ["oauth2", "oauth 2.0"],
        "jwt": ["json web token"],
    }

    @staticmethod
    def normalize_skill(skill: str) -> str:
        """
        Normalize a skill name to its canonical form.

        Args:
            skill: Raw skill name string

        Returns:
            Normalized skill name (lowercase, canonical form)
        """
        if not skill:
            return ""

        # Convert to lowercase and strip whitespace
        normalized = skill.lower().strip()
        
        # Remove special characters and extra spaces
        normalized = re.sub(r'[^\w\s\-\+]', '', normalized)
        normalized = re.sub(r'\s+', ' ', normalized)
        
        # Check against aliases
        for canonical, aliases in SkillMatcher.SKILL_ALIASES.items():
            if normalized in [alias.lower() for alias in aliases]:
                return canonical
            if normalized == canonical:
                return canonical
        
        return normalized

    @staticmethod
    def normalize_skills(skills: list[str]) -> set[str]:
        """
        Normalize a list of skills to their canonical forms.

        Args:
            skills: List of raw skill names

        Returns:
            Set of normalized skill names
        """
        normalized = set()
        for skill in skills:
            if isinstance(skill, str):
                norm_skill = SkillMatcher.normalize_skill(skill)
                if norm_skill:
                    normalized.add(norm_skill)
            elif isinstance(skill, dict):
                norm_skill = SkillMatcher.normalize_skill(skill.get("name", ""))
                if norm_skill:
                    normalized.add(norm_skill)
        return normalized

    @staticmethod
    def compare_skills(
        resume_skills: list[str],
        required_skills: list[str],
        preferred_skills: list[str] | None = None,
    ) -> dict:
        """
        Compare resume skills with job requirements.

        Args:
            resume_skills: List of skills from resume
            required_skills: List of required skills from job
            preferred_skills: Optional list of preferred skills from job

        Returns:
            Dict with skill matching analysis including:
                - matched_required_skills: Skills in resume that match required skills
                - missing_required_skills: Required skills not in resume
                - matched_preferred_skills: Skills in resume that match preferred skills
                - extra_skills: Skills in resume not in job requirements
                - skill_match_score: Overall skill match score (0-100)
                - skill_match_breakdown: Detailed scoring breakdown
        """
        # Normalize all skills
        normalized_resume = SkillMatcher.normalize_skills(resume_skills)
        normalized_required = SkillMatcher.normalize_skills(required_skills)
        normalized_preferred = SkillMatcher.normalize_skills(preferred_skills or [])

        # Find matched required skills
        matched_required = normalized_resume.intersection(normalized_required)
        missing_required = normalized_required - normalized_resume

        # Find matched preferred skills
        matched_preferred = normalized_resume.intersection(normalized_preferred)

        # Find extra skills (resume skills not in requirements)
        all_job_skills = normalized_required.union(normalized_preferred)
        extra_skills = normalized_resume - all_job_skills

        # Calculate skill match score
        # Required skills are more important than preferred
        required_count = len(normalized_required)
        if required_count > 0:
            required_score = (len(matched_required) / required_count) * 70  # 70% weight
        else:
            required_score = 0

        preferred_count = len(normalized_preferred)
        if preferred_count > 0:
            preferred_score = (len(matched_preferred) / preferred_count) * 30  # 30% weight
        else:
            preferred_score = 0

        # Bonus for having extra relevant skills
        extra_bonus = min(len(extra_skills) * 2, 10)  # Up to 10% bonus

        overall_score = min(required_score + preferred_score + extra_bonus, 100)

        return {
            "matched_required_skills": sorted(list(matched_required)),
            "missing_required_skills": sorted(list(missing_required)),
            "matched_preferred_skills": sorted(list(matched_preferred)),
            "extra_skills": sorted(list(extra_skills)),
            "skill_match_score": round(overall_score, 2),
            "skill_match_breakdown": {
                "required_count": required_count,
                "matched_required_count": len(matched_required),
                "required_coverage": round((len(matched_required) / required_count) * 100, 2) if required_count > 0 else 0,
                "preferred_count": preferred_count,
                "matched_preferred_count": len(matched_preferred),
                "preferred_coverage": round((len(matched_preferred) / preferred_count) * 100, 2) if preferred_count > 0 else 0,
                "extra_skills_count": len(extra_skills),
                "score_breakdown": {
                    "required_score": round(required_score, 2),
                    "preferred_score": round(preferred_score, 2),
                    "extra_bonus": round(extra_bonus, 2),
                }
            }
        }

    @staticmethod
    def get_skill_match_rating(score: float) -> str:
        """
        Get a qualitative rating based on skill match score.

        Args:
            score: Skill match score (0-100)

        Returns:
            Qualitative rating string
        """
        if score >= 90:
            return "Excellent Match"
        elif score >= 75:
            return "Strong Match"
        elif score >= 60:
            return "Good Match"
        elif score >= 40:
            return "Fair Match"
        elif score >= 20:
            return "Weak Match"
        else:
            return "Poor Match"

    @staticmethod
    def get_skill_gap_analysis(
        resume_skills: list[str],
        required_skills: list[str],
    ) -> dict:
        """
        Analyze skill gaps and provide recommendations.

        Args:
            resume_skills: List of skills from resume
            required_skills: List of required skills from job

        Returns:
            Dict with gap analysis including recommendations for skill development
        """
        comparison = SkillMatcher.compare_skills(resume_skills, required_skills)
        
        missing = comparison["missing_required_skills"]
        
        # Prioritize missing skills by importance (technical skills first)
        technical_missing = []
        other_missing = []
        
        tech_keywords = ["python", "java", "javascript", "react", "angular", "vue", "nodejs", 
                        "django", "flask", "spring", "aws", "docker", "kubernetes", "sql", "mongodb"]
        
        for skill in missing:
            if any(tech in skill.lower() for tech in tech_keywords):
                technical_missing.append(skill)
            else:
                other_missing.append(skill)
        
        return {
            "priority_missing_skills": technical_missing,
            "other_missing_skills": other_missing,
            "recommendations": SkillMatcher._generate_skill_recommendations(missing),
            "learning_priority": "high" if len(technical_missing) > 0 else "medium"
        }

    @staticmethod
    def _generate_skill_recommendations(missing_skills: list[str]) -> list[str]:
        """Generate learning recommendations for missing skills."""
        if not missing_skills:
            return []
        
        recommendations = []
        
        for skill in missing_skills[:5]:  # Limit to top 5 missing skills
            recommendations.append(f"Consider learning {skill.title()}")
        
        if len(missing_skills) > 5:
            recommendations.append(f"And {len(missing_skills) - 5} more skills")
        
        return recommendations
