"""
ResumeAnalyzer – Step 4 & 5
============================
Step 4: Build a detailed prompt that sends the resume text + pre-extracted data
        to Groq AI and asks for a structured JSON evaluation.
Step 5: Parse Groq's JSON response safely, stripping any markdown fences.
"""

import json
import re
import warnings

try:
    from groq import Groq
    _GROQ_PKG_INSTALLED = True
except ImportError:
    _GROQ_PKG_INSTALLED = False

from app.core.config import settings


def get_groq_model() -> str:
    """Retrieve configured Groq AI model name from settings."""
    return getattr(settings, "GROQ_MODEL", None) or "llama-3.3-70b-versatile"


def get_groq_client():
    """Get initialized Groq client using settings.GROQ_API_KEY."""
    if not _GROQ_PKG_INSTALLED:
        raise RuntimeError("groq package is not installed. Please install it using `pip install groq`.")
    api_key = getattr(settings, "GROQ_API_KEY", "")
    if not api_key or api_key.startswith("CHANGE_ME"):
        raise RuntimeError("GROQ_API_KEY is not set or invalid. Please configure GROQ_API_KEY in your .env file.")
    return Groq(api_key=api_key)


# ---------------------------------------------------------------------------
# Step 4 – Analysis prompt
# ---------------------------------------------------------------------------

ANALYSIS_PROMPT_TEMPLATE = """
You are an expert ATS (Applicant Tracking System) resume analyst with 15+ years of
experience in technical recruitment across software engineering, data science, and
product management roles.

You will be given:
  1. The raw resume text extracted from the candidate's document.
  2. Pre-extracted structured data (skills, education, experience, projects, etc.)

Your job is to perform a deep, objective evaluation of the resume and return a
structured JSON object. Be specific, actionable, and honest.

---
## RAW RESUME TEXT
{resume_text}

---
## PRE-EXTRACTED STRUCTURED DATA
{extracted_data}

---
## OUTPUT FORMAT

Return ONLY a valid JSON object — no markdown, no extra text, no code fences.
The JSON must match this exact schema:

{{
  "overall_score": <integer 0-100>,
  "score_breakdown": {{
    "content_quality":    <integer 0-25>,
    "skills_relevance":   <integer 0-25>,
    "experience_depth":   <integer 0-25>,
    "formatting_clarity": <integer 0-25>
  }},
  "summary": "<2-3 sentence professional summary of the candidate>",
  "strengths": [
    "<specific strength 1>",
    "<specific strength 2>",
    "<specific strength 3>"
  ],
  "weaknesses": [
    "<specific weakness 1>",
    "<specific weakness 2>"
  ],
  "missing_skills": [
    "<skill that is commonly expected but absent>"
  ],
  "recommendations": [
    "<actionable improvement 1>",
    "<actionable improvement 2>",
    "<actionable improvement 3>"
  ],
  "keyword_suggestions": [
    "<ATS keyword that should be added>"
  ],
  "experience_level": "<one of: Fresher | Junior | Mid-level | Senior | Lead | Executive>",
  "top_skills": ["<skill1>", "<skill2>", "<skill3>", "<skill4>", "<skill5>"]
}}

Scoring guidelines:
- content_quality   (0-25): Clarity, grammar, bullet-point quality, quantified achievements
- skills_relevance  (0-25): Breadth and depth of technical/soft skills
- experience_depth  (0-25): Years, impact, progression, leadership
- formatting_clarity(0-25): ATS-friendliness, section organisation, readability
"""


class ResumeAnalyzer:
    """Calls Groq AI to generate a structured AI analysis of a resume."""

    # ------------------------------------------------------------------
    # Step 4 – build and send the prompt
    # ------------------------------------------------------------------
    @staticmethod
    def analyze_resume(resume_text: str, extracted_data: dict) -> dict:
        """
        Send the resume to Groq AI and return a parsed dict with the AI analysis.

        Args:
            resume_text:    Raw text extracted from the resume file.
            extracted_data: Structured dict produced by InformationExtractor.

        Returns:
            dict following the ANALYSIS_PROMPT_TEMPLATE schema.

        Raises:
            ValueError: If Groq AI returns an invalid / unparseable response.
            RuntimeError: If the Groq API call itself fails.
        """
        client = get_groq_client()
        model_name = get_groq_model()

        prompt = ANALYSIS_PROMPT_TEMPLATE.format(
            resume_text=resume_text,
            extracted_data=json.dumps(extracted_data, indent=2, ensure_ascii=False),
        )

        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert ATS resume analyst. Always respond with valid JSON only, no markdown or extra text."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=4096,
                response_format={"type": "json_object"}
            )
        except Exception as exc:
            err_str = str(exc)
            if "does not exist" in err_str or "access" in err_str or "model_not_found" in err_str:
                raise RuntimeError(
                    f"Groq API call failed: Model '{model_name}' is invalid or inaccessible. "
                    f"Please update GROQ_MODEL in your environment/.env file to a supported model (e.g. 'llama-3.3-70b-versatile' or 'llama-3.1-8b-instant'). "
                    f"Details: {err_str}"
                ) from exc
            raise RuntimeError(f"Groq API call failed: {exc}") from exc

        # ------------------------------------------------------------------
        # Step 5 – parse the JSON response
        # ------------------------------------------------------------------
        return ResumeAnalyzer.parse_response(response.choices[0].message.content)

    # ------------------------------------------------------------------
    # Step 5 – parse / sanitise Groq's JSON response
    # ------------------------------------------------------------------
    @staticmethod
    def parse_response(response_text: str) -> dict:
        """
        Strip any markdown code fences from the Groq response and parse it
        as a Python dict.  Validates that required top-level keys are present.

        Args:
            response_text: Raw text returned by Groq AI.

        Returns:
            Parsed dict matching the analysis schema.

        Raises:
            ValueError: If JSON is invalid or required keys are missing.
        """
        # Remove ```json … ``` or ``` … ``` wrappers Groq sometimes adds
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

        # Light structural validation – ensure the key fields exist
        required_keys = {"overall_score", "strengths", "weaknesses", "recommendations"}
        missing = required_keys - data.keys()
        if missing:
            raise ValueError(
                f"Groq AI response is missing required keys: {missing}\n"
                f"Got keys: {list(data.keys())}"
            )

        return data
