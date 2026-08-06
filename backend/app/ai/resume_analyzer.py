"""
ResumeAnalyzer – Step 4 & 5
============================
Step 4: Build a detailed prompt that sends the resume text + pre-extracted data
        to Gemini and asks for a structured JSON evaluation.
Step 5: Parse Gemini's JSON response safely, stripping any markdown fences.
"""

import json
import re
import warnings

# Suppress the FutureWarning emitted by google-generativeai 0.8.x
with warnings.catch_warnings():
    warnings.simplefilter("ignore", FutureWarning)
    try:
        import google.generativeai as genai
        from app.core.config import settings
        genai.configure(api_key=settings.GEMINI_API_KEY)
        _GEMINI_AVAILABLE = True
    except ImportError:
        _GEMINI_AVAILABLE = False

_MODEL = "gemini-2.5-flash"


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
    """Calls Gemini to generate a structured AI analysis of a resume."""

    # ------------------------------------------------------------------
    # Step 4 – build and send the prompt
    # ------------------------------------------------------------------
    @staticmethod
    def analyze_resume(resume_text: str, extracted_data: dict) -> dict:
        """
        Send the resume to Gemini and return a parsed dict with the AI analysis.

        Args:
            resume_text:    Raw text extracted from the resume file.
            extracted_data: Structured dict produced by InformationExtractor.

        Returns:
            dict following the ANALYSIS_PROMPT_TEMPLATE schema.

        Raises:
            ValueError: If Gemini returns an invalid / unparseable response.
            RuntimeError: If the Gemini API call itself fails.
        """
        if not _GEMINI_AVAILABLE:
            raise RuntimeError("Gemini API is not available. Please install google-generativeai package.")

        prompt = ANALYSIS_PROMPT_TEMPLATE.format(
            resume_text=resume_text,
            extracted_data=json.dumps(extracted_data, indent=2, ensure_ascii=False),
        )

        try:
            model = genai.GenerativeModel(_MODEL)
            response = model.generate_content(prompt)
        except Exception as exc:
            raise RuntimeError(f"Gemini API call failed: {exc}") from exc

        # ------------------------------------------------------------------
        # Step 5 – parse the JSON response
        # ------------------------------------------------------------------
        return ResumeAnalyzer.parse_response(response.text)

    # ------------------------------------------------------------------
    # Step 5 – parse / sanitise Gemini's JSON response
    # ------------------------------------------------------------------
    @staticmethod
    def parse_response(response_text: str) -> dict:
        """
        Strip any markdown code fences from the Gemini response and parse it
        as a Python dict.  Validates that required top-level keys are present.

        Args:
            response_text: Raw text returned by Gemini.

        Returns:
            Parsed dict matching the analysis schema.

        Raises:
            ValueError: If JSON is invalid or required keys are missing.
        """
        # Remove ```json … ``` or ``` … ``` wrappers Gemini sometimes adds
        cleaned = re.sub(r"```(?:json)?", "", response_text).strip()

        # Remove any trailing ``` that may remain
        cleaned = cleaned.rstrip("`").strip()

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Gemini returned an invalid JSON response: {exc}\n"
                f"Raw response (first 500 chars): {response_text[:500]}"
            ) from exc

        # Light structural validation – ensure the key fields exist
        required_keys = {"overall_score", "strengths", "weaknesses", "recommendations"}
        missing = required_keys - data.keys()
        if missing:
            raise ValueError(
                f"Gemini response is missing required keys: {missing}\n"
                f"Got keys: {list(data.keys())}"
            )

        return data