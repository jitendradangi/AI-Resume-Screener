"""
Semantic Matcher – Sprint 9 Task 7
===================================
Uses Groq AI to perform semantic comparison between resumes and job descriptions.
Provides AI-powered insights beyond keyword matching.
"""

import json
import re
import warnings
from functools import lru_cache
from typing import Any

# Suppress the FutureWarning emitted by google-generativeai 0.8.x
with warnings.catch_warnings():
    warnings.simplefilter("ignore", FutureWarning)
    try:
        from groq import Groq
        from app.core.config import settings
        _client = Groq(api_key=settings.GROQ_API_KEY)
        _MODEL = "llama-3.3-70b-versatile"
        _GROQ_AVAILABLE = True
    except ImportError:
        _GROQ_AVAILABLE = False


# ---------------------------------------------------------------------------
# Semantic Matching Prompt
# ---------------------------------------------------------------------------

SEMANTIC_MATCH_PROMPT_TEMPLATE = """
You are an expert ATS (Applicant Tracking System) analyst with 15+ years of
experience in technical recruitment across software engineering, data science, and
product management roles.

You will be given:
  1. A job description with requirements
  2. A candidate's resume text
  3. Pre-extracted structured data from the resume

Your job is to perform a deep, semantic analysis of how well the candidate aligns
with the job requirements. Look beyond simple keyword matching and consider:
- Relevance of experience to the role
- Quality and impact of projects
- Career progression and growth
- Alignment with company culture and role expectations
- Potential for success in the position

---
## JOB DESCRIPTION
{job_description}

---
## CANDIDATE RESUME TEXT
{resume_text}

---
## PRE-EXTRACTED RESUME DATA
{extracted_data}

---
## OUTPUT FORMAT

Return ONLY a valid JSON object — no markdown, no extra text, no code fences.
The JSON must match this exact schema:

{{
  "semantic_score": <integer 0-100>,
  "strengths": [
    "<specific strength 1>",
    "<specific strength 2>",
    "<specific strength 3>"
  ],
  "weaknesses": [
    "<specific weakness 1>",
    "<specific weakness 2>"
  ],
  "reason": "<2-3 sentence explanation of why the candidate is or isn't a good match>"
}}

Scoring guidelines:
- 90-100: Excellent match - candidate exceeds expectations
- 75-89: Strong match - candidate is highly suitable
- 60-74: Good match - candidate meets requirements
- 40-59: Fair match - candidate has potential but has gaps
- 20-39: Weak match - candidate has significant gaps
- 0-19: Poor match - candidate is not suitable

Consider both technical alignment and soft skills/fit in your evaluation.
"""


class SemanticMatcher:
    """Uses Groq AI to perform semantic job-resume matching."""

    # Simple in-memory cache for semantic results
    _cache: dict[str, dict[str, Any]] = {}

    @staticmethod
    def _generate_cache_key(
        job_description: str,
        resume_text: str,
        extracted_data: dict,
    ) -> str:
        """Generate a cache key from input parameters."""
        import hashlib
        key_str = f"{job_description[:200]}|{resume_text[:200]}|{json.dumps(extracted_data, sort_keys=True)}"
        return hashlib.md5(key_str.encode()).hexdigest()

    @staticmethod
    def compare_semantic(
        job_description: str,
        resume_text: str,
        extracted_data: dict,
        use_cache: bool = True,
    ) -> dict:
        """
        Send job description and resume to Groq AI for semantic analysis.

        Args:
            job_description: Raw job description text
            resume_text: Raw resume text
            extracted_data: Structured dict from resume analysis
            use_cache: Whether to use cached results (default: True)

        Returns:
            Dict with semantic analysis:
                - semantic_score: Integer 0-100
                - strengths: List of strengths
                - weaknesses: List of weaknesses
                - reason: Explanation of match quality

        Raises:
            ValueError: If Groq AI returns an invalid/unparseable response
            RuntimeError: If the Groq API call fails
        """
        if not _GROQ_AVAILABLE:
            raise RuntimeError("Groq API is not available. Please install groq package and set GROQ_API_KEY environment variable.")

        # Check cache
        if use_cache:
            cache_key = SemanticMatcher._generate_cache_key(job_description, resume_text, extracted_data)
            if cache_key in SemanticMatcher._cache:
                return SemanticMatcher._cache[cache_key]

        prompt = SEMANTIC_MATCH_PROMPT_TEMPLATE.format(
            job_description=job_description,
            resume_text=resume_text,
            extracted_data=json.dumps(extracted_data, indent=2, ensure_ascii=False),
        )

        try:
            response = _client.chat.completions.create(
                model=_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert ATS analyst. Always respond with valid JSON only, no markdown or extra text."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2048,
                response_format={"type": "json_object"}
            )
        except Exception as exc:
            raise RuntimeError(f"Groq API call failed: {exc}") from exc

        result = SemanticMatcher.parse_response(response.choices[0].message.content)

        # Cache the result
        if use_cache:
            SemanticMatcher._cache[cache_key] = result

        return result

    @staticmethod
    def clear_cache() -> None:
        """Clear the semantic matching cache."""
        SemanticMatcher._cache.clear()

    @staticmethod
    def parse_response(response_text: str) -> dict:
        """
        Strip markdown code fences and parse Groq AI's JSON response.

        Args:
            response_text: Raw text returned by Groq AI

        Returns:
            Parsed dict matching the semantic match schema

        Raises:
            ValueError: If JSON is invalid or required keys are missing
        """
        # Remove ```json … ``` or ``` … ``` wrappers
        cleaned = re.sub(r"```(?:json)?", "", response_text).strip()

        # Remove any trailing ``` that may remain
        cleaned = cleaned.rstrip("`").strip()

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Groq AI returned an invalid JSON response: {exc}\n"
                f"Raw response (first 500 chars): {response_text[:500]}"
            ) from exc

        # Validate required keys
        required_keys = {"semantic_score", "strengths", "weaknesses", "reason"}
        missing = required_keys - data.keys()
        if missing:
            raise ValueError(
                f"Groq AI response is missing required keys: {missing}\n"
                f"Got keys: {list(data.keys())}"
            )

        # Validate semantic_score is an integer 0-100
        if not isinstance(data["semantic_score"], int):
            try:
                data["semantic_score"] = int(data["semantic_score"])
            except (ValueError, TypeError):
                raise ValueError(
                    f"semantic_score must be an integer, got {type(data['semantic_score'])}"
                )

        # Ensure score is in valid range
        data["semantic_score"] = max(0, min(100, data["semantic_score"]))

        # Ensure strengths and weaknesses are lists
        if not isinstance(data["strengths"], list):
            data["strengths"] = [str(data["strengths"])] if data["strengths"] else []
        if not isinstance(data["weaknesses"], list):
            data["weaknesses"] = [str(data["weaknesses"])] if data["weaknesses"] else []

        return data

    @staticmethod
    def get_semantic_match_rating(score: int) -> str:
        """
        Get qualitative rating based on semantic match score.

        Args:
            score: Semantic match score (0-100)

        Returns:
            Qualitative rating string
        """
        if score >= 90:
            return "Excellent Semantic Match"
        elif score >= 75:
            return "Strong Semantic Match"
        elif score >= 60:
            return "Good Semantic Match"
        elif score >= 40:
            return "Fair Semantic Match"
        elif score >= 20:
            return "Weak Semantic Match"
        else:
            return "Poor Semantic Match"
