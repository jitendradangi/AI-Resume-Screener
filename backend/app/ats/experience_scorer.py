"""
Experience Scorer – ATS Experience Quality Analysis
==================================================
Analyzes and scores work experience quality for resume quality ATS evaluation.
Evaluates experience completeness, description quality, quantifiable achievements, and career progression.
"""

import re


class ExperienceScorer:
    """Analyzes and scores work experience for resume quality ATS evaluation."""

    # Action verbs that indicate strong experience descriptions
    ACTION_VERBS = {
        "led", "managed", "developed", "implemented", "created", "designed", "built",
        "optimized", "improved", "increased", "decreased", "reduced", "achieved", "delivered",
        "launched", "deployed", "engineered", "architected", "coordinated", "organized",
        "executed", "supervised", "mentored", "trained", "collaborated", "partnered",
        "negotiated", "closed", "won", "secured", "established", "founded", "scaled",
        "automated", "streamlined", "modernized", "refactored", "migrated", "integrated",
    }

    # Metrics indicators (quantifiable achievements)
    METRIC_INDICATORS = {
        "percent": ["%", "percent", "percentage"],
        "currency": ["$", "€", "£", "usd", "eur", "gbp", "budget", "revenue", "sales", "cost"],
        "time": ["months", "years", "weeks", "days", "hours", "faster", "quicker", "sooner"],
        "count": ["users", "customers", "clients", "employees", "team", "members", "projects", "products"],
        "scale": ["scale", "growth", "increase", "decrease", "reduction", "improvement", "efficiency"],
    }

    @staticmethod
    def get_experience_analysis(resume_analysis: dict) -> dict:
        """
        Analyze work experience quality and calculate experience score.

        Args:
            resume_analysis: Dict containing resume analysis data with keys:
                - experience: list of experience dicts with keys: title, company, description, start_date, end_date

        Returns:
            Dict with experience analysis results including:
                - overall_experience_score: Overall experience quality score (0-100)
                - completeness_score: Score for information completeness
                - description_quality_score: Score for description quality
                - achievements_score: Score for quantifiable achievements
                - progression_score: Score for career progression
                - experience_issues: List of identified experience issues
                - experience_recommendations: List of improvement recommendations
        """
        experiences = resume_analysis.get("experience", [])

        if not experiences or len(experiences) == 0:
            return {
                "overall_experience_score": 0.0,
                "completeness_score": 0.0,
                "description_quality_score": 0.0,
                "achievements_score": 0.0,
                "progression_score": 0.0,
                "experience_issues": ["No work experience provided"],
                "experience_recommendations": ["Add work experience with job titles, companies, and detailed descriptions"],
            }

        issues = []
        recommendations = []

        # Calculate individual scores
        completeness_score = ExperienceScorer._calculate_completeness(experiences, issues, recommendations)
        description_quality_score = ExperienceScorer._calculate_description_quality(experiences, issues, recommendations)
        achievements_score = ExperienceScorer._calculate_achievements(experiences, issues, recommendations)
        progression_score = ExperienceScorer._calculate_progression(experiences, issues, recommendations)

        # Calculate overall experience score (weighted average)
        overall_score = (
            completeness_score * 0.30 +
            description_quality_score * 0.30 +
            achievements_score * 0.25 +
            progression_score * 0.15
        )

        return {
            "overall_experience_score": round(overall_score, 2),
            "completeness_score": round(completeness_score, 2),
            "description_quality_score": round(description_quality_score, 2),
            "achievements_score": round(achievements_score, 2),
            "progression_score": round(progression_score, 2),
            "experience_issues": issues,
            "experience_recommendations": recommendations,
        }

    @staticmethod
    def _calculate_completeness(experiences: list, issues: list, recommendations: list) -> float:
        """
        Calculate experience completeness score based on information provided.

        Args:
            experiences: List of experience dicts
            issues: List to append identified issues
            recommendations: List to append recommendations

        Returns:
            Completeness score (0-100)
        """
        if not experiences:
            return 0.0

        total_score = 0
        for exp in experiences:
            if isinstance(exp, dict):
                score = 0
                # Check for required fields
                if exp.get("title"):
                    score += 25
                else:
                    issues.append(f"Experience entry missing job title")
                    recommendations.append("Include job titles for all work experience entries")

                if exp.get("company"):
                    score += 25
                else:
                    issues.append(f"Experience entry missing company name")
                    recommendations.append("Include company names for all work experience entries")

                if exp.get("start_date") or exp.get("end_date"):
                    score += 25
                else:
                    recommendations.append("Include employment dates (start/end) for all work experience entries")

                if exp.get("description") and len(exp["description"]) > 20:
                    score += 25
                else:
                    issues.append(f"Experience entry missing or too short description")
                    recommendations.append("Add detailed descriptions for all work experience entries")

                total_score += score

        # Average score across all experiences
        avg_score = total_score / len(experiences)
        return round(avg_score, 2)

    @staticmethod
    def _calculate_description_quality(experiences: list, issues: list, recommendations: list) -> float:
        """
        Calculate description quality score based on detail and action verbs.

        Args:
            experiences: List of experience dicts
            issues: List to append identified issues
            recommendations: List to append recommendations

        Returns:
            Description quality score (0-100)
        """
        if not experiences:
            return 0.0

        total_score = 0
        for exp in experiences:
            if isinstance(exp, dict):
                description = exp.get("description", "")
                score = 0

                # Check description length
                if len(description) < 20:
                    issues.append(f"Experience description too short")
                    score += 0
                elif len(description) < 50:
                    score += 30
                    recommendations.append("Expand experience descriptions with more details about responsibilities and achievements")
                elif len(description) < 150:
                    score += 70
                else:
                    score += 100

                # Check for action verbs
                action_verb_count = 0
                words = re.findall(r'\b\w+\b', description.lower())
                for word in words:
                    if word in ExperienceScorer.ACTION_VERBS:
                        action_verb_count += 1

                if action_verb_count >= 3:
                    score += 20
                elif action_verb_count >= 1:
                    score += 10
                else:
                    recommendations.append("Use action verbs (led, developed, managed, etc.) to describe your experience")

                # Check for bullet points or structured format
                if "•" in description or "-" in description or "*" in description:
                    score += 10
                else:
                    recommendations.append("Use bullet points to structure experience descriptions")

                total_score += min(score, 100)

        # Average score across all experiences
        avg_score = total_score / len(experiences)
        return round(avg_score, 2)

    @staticmethod
    def _calculate_achievements(experiences: list, issues: list, recommendations: list) -> float:
        """
        Calculate achievements score based on quantifiable metrics.

        Args:
            experiences: List of experience dicts
            issues: List to append identified issues
            recommendations: List to append recommendations

        Returns:
            Achievements score (0-100)
        """
        if not experiences:
            return 0.0

        total_score = 0
        has_metrics = False

        for exp in experiences:
            if isinstance(exp, dict):
                description = exp.get("description", "").lower()
                score = 0

                # Check for metric indicators
                metric_count = 0
                for category, indicators in ExperienceScorer.METRIC_INDICATORS.items():
                    for indicator in indicators:
                        if indicator in description:
                            metric_count += 1
                            has_metrics = True

                if metric_count >= 3:
                    score += 100
                elif metric_count >= 2:
                    score += 70
                elif metric_count >= 1:
                    score += 40
                else:
                    recommendations.append("Add quantifiable achievements (e.g., 'increased sales by 20%', 'managed team of 10')")

                total_score += score

        if not has_metrics:
            issues.append("No quantifiable achievements found in experience descriptions")

        # Average score across all experiences
        avg_score = total_score / len(experiences)
        return round(avg_score, 2)

    @staticmethod
    def _calculate_progression(experiences: list, issues: list, recommendations: list) -> float:
        """
        Calculate career progression score based on title advancement and responsibility growth.

        Args:
            experiences: List of experience dicts
            issues: List to append identified issues
            recommendations: List to append recommendations

        Returns:
            Progression score (0-100)
        """
        if not experiences or len(experiences) < 2:
            # Can't assess progression with fewer than 2 experiences
            return 50.0

        score = 0

        # Check for title progression (simple heuristic)
        seniority_keywords = {
            "senior": 3,
            "lead": 3,
            "principal": 4,
            "manager": 3,
            "director": 4,
            "head": 4,
            "chief": 5,
            "vp": 4,
            "vice president": 4,
            "junior": 1,
            "intern": 0,
            "associate": 1,
            "assistant": 1,
        }

        seniority_levels = []
        for exp in experiences:
            if isinstance(exp, dict):
                title = exp.get("title", "").lower()
                level = 2  # Default mid-level
                for keyword, level_value in seniority_keywords.items():
                    if keyword in title:
                        level = level_value
                        break
                seniority_levels.append(level)

        # Check if seniority generally increases over time
        if len(seniority_levels) >= 2:
            progression_count = 0
            for i in range(1, len(seniority_levels)):
                if seniority_levels[i] > seniority_levels[i-1]:
                    progression_count += 1

            if progression_count >= len(seniority_levels) - 1:
                score += 100
            elif progression_count >= 1:
                score += 60
            else:
                recommendations.append("Highlight career progression and promotions in your experience section")
        else:
            score += 50

        # Check for increasing responsibility (longer descriptions = more responsibility)
        description_lengths = []
        for exp in experiences:
            if isinstance(exp, dict):
                desc = exp.get("description", "")
                description_lengths.append(len(desc))

        if len(description_lengths) >= 2:
            # Check if later descriptions are generally longer
            increasing_length = 0
            for i in range(1, len(description_lengths)):
                if description_lengths[i] > description_lengths[i-1]:
                    increasing_length += 1

            if increasing_length >= len(description_lengths) / 2:
                score += 20

        return round(min(score, 100), 2)
