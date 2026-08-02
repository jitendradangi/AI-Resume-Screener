import json
import re

from google import genai
from google.genai import errors as genai_errors
from google.genai import types

from app.core.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    GEMINI_TIMEOUT_MS,
)


class AIAnalysisError(Exception):
    """Base error raised by the AI layer."""


class AIConfigurationError(AIAnalysisError):
    """Raised when the Gemini client is not configured correctly."""


class AIServiceError(AIAnalysisError):
    """Raised when Gemini is unreachable or returns an API error."""


class AIResponseError(AIAnalysisError):
    """Raised when Gemini returns an empty or non-JSON response."""


LIST_FIELDS = (
    "strengths",
    "weaknesses",
    "missing_skills",
    "recommendations",
)

CODE_FENCE_PATTERN = re.compile(
    r"^\s*```(?:json)?\s*|\s*```\s*$",
    re.IGNORECASE,
)

PROMPT_TEMPLATE = """You are an experienced technical recruiter and ATS \
(Applicant Tracking System) analyst.

Analyse the candidate resume below and produce an ATS-style review.

Rules:
- Base every statement only on the resume content, never invent experience.
- "missing_skills" must list in-demand skills for the candidate's target \
role that the resume does not evidence.
- "recommendations" must be concrete, actionable resume edits.
- Each list must contain between 3 and 6 short items.
- Respond with a single JSON object and nothing else. No markdown, no \
code fences, no commentary.

Required JSON shape:
{{
  "summary": "string",
  "strengths": ["string"],
  "weaknesses": ["string"],
  "missing_skills": ["string"],
  "recommendations": ["string"]
}}

Structured data already extracted from the resume:
{extracted_data}

Resume text:
\"\"\"
{resume_text}
\"\"\"
"""

MAX_RESUME_CHARS = 20000


class ResumeAnalyzer:
    """Generates ATS feedback for a resume using Google Gemini."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        timeout_ms: int | None = None,
    ):
        key = api_key or GEMINI_API_KEY

        if not key:
            raise AIConfigurationError(
                "GEMINI_API_KEY is not configured."
            )

        self.model = model or GEMINI_MODEL

        self.client = genai.Client(
            api_key=key,
            http_options=types.HttpOptions(
                timeout=timeout_ms or GEMINI_TIMEOUT_MS,
            ),
        )

    def analyze_resume(
        self,
        resume_text: str,
        extracted_data: dict | None = None,
    ) -> dict:

        if not resume_text or not resume_text.strip():
            raise AIAnalysisError(
                "Resume text is empty, nothing to analyse."
            )

        prompt = self.build_prompt(
            resume_text,
            extracted_data or {},
        )

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.2,
                ),
            )
        except genai_errors.APIError as exc:
            raise AIServiceError(
                f"Gemini API request failed: {exc}"
            ) from exc
        except Exception as exc:
            raise AIServiceError(
                f"Could not reach Gemini: {exc}"
            ) from exc

        return self.parse_response(
            getattr(response, "text", None)
        )

    @staticmethod
    def build_prompt(
        resume_text: str,
        extracted_data: dict,
    ) -> str:
        return PROMPT_TEMPLATE.format(
            extracted_data=json.dumps(
                extracted_data,
                default=str,
            ),
            resume_text=resume_text[:MAX_RESUME_CHARS],
        )

    @classmethod
    def parse_response(cls, raw_text: str | None) -> dict:

        if not raw_text or not raw_text.strip():
            raise AIResponseError(
                "Gemini returned an empty response."
            )

        cleaned = CODE_FENCE_PATTERN.sub(
            "",
            raw_text.strip(),
        ).strip()

        try:
            payload = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise AIResponseError(
                f"Gemini returned invalid JSON: {exc}"
            ) from exc

        if not isinstance(payload, dict):
            raise AIResponseError(
                "Gemini response is not a JSON object."
            )

        return cls.normalize(payload)

    @staticmethod
    def normalize(payload: dict) -> dict:

        summary = payload.get("summary")

        if summary is not None and not isinstance(summary, str):
            raise AIResponseError(
                "Gemini response field 'summary' is not a string."
            )

        result = {"summary": summary}

        for field in LIST_FIELDS:
            value = payload.get(field, [])

            if value is None:
                value = []

            if not isinstance(value, list):
                raise AIResponseError(
                    f"Gemini response field '{field}' is not a list."
                )

            result[field] = [
                str(item).strip()
                for item in value
                if str(item).strip()
            ]

        if not summary and not any(
            result[field] for field in LIST_FIELDS
        ):
            raise AIResponseError(
                "Gemini response did not contain any analysis fields."
            )

        return result
