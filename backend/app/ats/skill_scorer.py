"""
SkillScorer – ATS Skill Quality Analysis
=========================================
Analyzes and scores skills for resume quality ATS evaluation.
Evaluates skill quantity, variety, relevance, and presentation quality.
"""

import re


class SkillScorer:
    """Analyzes and scores skills for resume quality ATS evaluation."""

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

    # Skill categories for relevance assessment
    SKILL_CATEGORIES = {
        "programming_languages": ["python", "java", "javascript", "typescript", "c++", "c#", "go", "rust", "swift", "kotlin"],
        "frameworks": ["react", "angular", "vue", "django", "flask", "spring", "express", "nodejs"],
        "databases": ["sql", "nosql", "mongodb", "postgresql", "mysql", "redis", "elasticsearch"],
        "cloud": ["aws", "azure", "gcp"],
        "devops": ["docker", "kubernetes", "terraform", "ansible", "jenkins", "git"],
        "data_science": ["machine learning", "deep learning", "nlp", "data science", "ai", "ml", "tensorflow", "pytorch"],
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
        for canonical, aliases in SkillScorer.SKILL_ALIASES.items():
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
                norm_skill = SkillScorer.normalize_skill(skill)
                if norm_skill:
                    normalized.add(norm_skill)
            elif isinstance(skill, dict):
                norm_skill = SkillScorer.normalize_skill(skill.get("name", ""))
                if norm_skill:
                    normalized.add(norm_skill)
        return normalized

    @staticmethod
    def calculate_skill_quantity(skills: list[str]) -> float:
        """
        Calculate skill quantity score based on number of skills.

        Args:
            skills: List of skills

        Returns:
            Quantity score (0-100)
        """
        if not skills:
            return 0.0

        # Ideal range: 10-20 skills
        count = len(set([SkillScorer.normalize_skill(s) for s in skills if isinstance(s, str)]))
        
        if count < 5:
            return 20.0
        elif count < 10:
            return 50.0
        elif count <= 20:
            return 100.0
        elif count <= 30:
            return 80.0
        else:
            return 60.0  # Too many skills may indicate lack of focus

    @staticmethod
    def calculate_skill_variety(normalized_skills: set[str]) -> float:
        """
        Calculate skill variety score based on diversity across categories.

        Args:
            normalized_skills: Set of normalized skills

        Returns:
            Variety score (0-100)
        """
        if not normalized_skills:
            return 0.0

        # Count categories represented
        categories_covered = 0
        for category, category_skills in SkillScorer.SKILL_CATEGORIES.items():
            if any(skill in normalized_skills for skill in category_skills):
                categories_covered += 1

        # More categories = higher score (max 6 categories)
        score = (categories_covered / 6) * 100
        return round(score, 2)

    @staticmethod
    def calculate_skill_relevance(normalized_skills: set[str]) -> float:
        """
        Calculate skill relevance based on recognized technical skills.

        Args:
            normalized_skills: Set of normalized skills

        Returns:
            Relevance score (0-100)
        """
        if not normalized_skills:
            return 0.0

        # Count recognized skills
        recognized_count = 0
        all_known_skills = set()
        for category_skills in SkillScorer.SKILL_CATEGORIES.values():
            all_known_skills.update(category_skills)
        
        for skill in normalized_skills:
            if skill in all_known_skills:
                recognized_count += 1

        # Percentage of recognized skills
        if len(normalized_skills) == 0:
            return 0.0
        
        relevance = (recognized_count / len(normalized_skills)) * 100
        return round(relevance, 2)

    @staticmethod
    def calculate_skill_presentation(resume_analysis: dict) -> float:
        """
        Evaluate how well skills are presented in the resume.

        Args:
            resume_analysis: Resume analysis data

        Returns:
            Presentation score (0-100)
        """
        score = 0.0

        # Check if skills section exists
        skills = resume_analysis.get("skills", [])
        if skills and len(skills) > 0:
            score += 40.0

        # Check if skills are in experience descriptions
        experiences = resume_analysis.get("experience", [])
        if experiences:
            has_skills_in_exp = False
            for exp in experiences:
                if isinstance(exp, dict):
                    desc = exp.get("description", "")
                    if desc and len(desc) > 50:
                        has_skills_in_exp = True
                        break
            if has_skills_in_exp:
                score += 30.0

        # Check if skills are in projects
        projects = resume_analysis.get("projects", [])
        if projects:
            has_tech_stack = False
            for project in projects:
                if isinstance(project, dict):
                    tech = project.get("technologies", [])
                    if tech and len(tech) > 0:
                        has_tech_stack = True
                        break
            if has_tech_stack:
                score += 30.0

        return round(score, 2)

    @staticmethod
    def extract_skills_from_resume_analysis(resume_analysis: dict) -> list[str]:
        """
        Extract skills from resume analysis data.

        Args:
            resume_analysis: Dict containing resume analysis data with skills field

        Returns:
            List of skill strings
        """
        skills = []
        
        # Extract from skills field
        analysis_skills = resume_analysis.get("skills", [])
        if isinstance(analysis_skills, list):
            for skill in analysis_skills:
                if isinstance(skill, str):
                    skills.append(skill)
                elif isinstance(skill, dict):
                    skills.append(skill.get("name", ""))
        
        # Extract from experience descriptions
        experiences = resume_analysis.get("experience", [])
        if isinstance(experiences, list):
            for exp in experiences:
                if isinstance(exp, dict):
                    description = exp.get("description", "")
                    if description:
                        # Extract potential skills from description
                        words = re.findall(r'\b[A-Z][a-z]+\b', description)
                        skills.extend(words)
        
        # Extract from projects
        projects = resume_analysis.get("projects", [])
        if isinstance(projects, list):
            for project in projects:
                if isinstance(project, dict):
                    technologies = project.get("technologies", [])
                    if isinstance(technologies, list):
                        skills.extend(technologies)
        
        return skills

    @staticmethod
    def get_skill_analysis(resume_analysis: dict) -> dict:
        """
        Perform complete skill quality analysis for resume.

        Args:
            resume_analysis: Resume analysis data

        Returns:
            Dict containing:
                - skills_normalized: set of normalized skills
                - skill_count: number of unique skills
                - skill_quantity: quantity score (0-100)
                - skill_variety: variety score (0-100)
                - skill_relevance: relevance score (0-100)
                - skill_presentation: presentation score (0-100)
                - overall_skills_score: combined skills score (0-100)
        """
        skills = SkillScorer.extract_skills_from_resume_analysis(resume_analysis)
        normalized_skills = SkillScorer.normalize_skills(skills)

        quantity_score = SkillScorer.calculate_skill_quantity(skills)
        variety_score = SkillScorer.calculate_skill_variety(normalized_skills)
        relevance_score = SkillScorer.calculate_skill_relevance(normalized_skills)
        presentation_score = SkillScorer.calculate_skill_presentation(resume_analysis)

        # Overall skills score: 25% quantity, 25% variety, 30% relevance, 20% presentation
        overall_score = (
            quantity_score * 0.25 +
            variety_score * 0.25 +
            relevance_score * 0.30 +
            presentation_score * 0.20
        )

        return {
            "skills_normalized": list(normalized_skills),
            "skill_count": len(normalized_skills),
            "skill_quantity": quantity_score,
            "skill_variety": variety_score,
            "skill_relevance": relevance_score,
            "skill_presentation": presentation_score,
            "overall_skills_score": round(overall_score, 2),
        }
