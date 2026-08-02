import json
from types import SimpleNamespace
from unittest.mock import MagicMock

import httpx
import pytest
from google.genai import errors as genai_errors

from app.ai.resume_analyzer import (
    AIAnalysisError,
    AIConfigurationError,
    AIResponseError,
    AIServiceError,
    ResumeAnalyzer,
)


VALID_PAYLOAD = {
    "summary": "Backend developer with 2 years of Python experience.",
    "strengths": ["Strong FastAPI experience", "Clear project section"],
    "weaknesses": ["No measurable impact in bullets"],
    "missing_skills": ["Docker", "AWS"],
    "recommendations": ["Add metrics to experience bullets"],
}


@pytest.fixture
def analyzer(monkeypatch):
    monkeypatch.setattr(
        "app.ai.resume_analyzer.genai.Client",
        MagicMock(),
    )

    return ResumeAnalyzer(api_key="test-key", model="test-model")


def api_error(code: int, message: str) -> genai_errors.APIError:
    return genai_errors.APIError(
        code,
        {"error": {"code": code, "message": message}},
    )


def set_response(analyzer, text):
    analyzer.client.models.generate_content = MagicMock(
        return_value=SimpleNamespace(text=text)
    )


def set_failure(analyzer, exc):
    analyzer.client.models.generate_content = MagicMock(side_effect=exc)


def test_missing_api_key_raises_configuration_error(monkeypatch):
    monkeypatch.setattr("app.ai.resume_analyzer.GEMINI_API_KEY", None)

    with pytest.raises(AIConfigurationError):
        ResumeAnalyzer()


def test_analyze_resume_returns_all_fields(analyzer):
    set_response(analyzer, json.dumps(VALID_PAYLOAD))

    result = analyzer.analyze_resume("Jane Doe\nPython", {"skills": ["Python"]})

    assert result == VALID_PAYLOAD

    prompt = analyzer.client.models.generate_content.call_args.kwargs["contents"]
    assert "Jane Doe" in prompt
    assert "Python" in prompt


def test_analyze_resume_strips_markdown_fences(analyzer):
    set_response(
        analyzer,
        "```json\n" + json.dumps(VALID_PAYLOAD) + "\n```",
    )

    assert analyzer.analyze_resume("resume text")["missing_skills"] == [
        "Docker",
        "AWS",
    ]


def test_empty_resume_text_is_rejected(analyzer):
    with pytest.raises(AIAnalysisError):
        analyzer.analyze_resume("   ")


def test_empty_response_raises_response_error(analyzer):
    set_response(analyzer, "")

    with pytest.raises(AIResponseError):
        analyzer.analyze_resume("resume text")


def test_invalid_json_raises_response_error(analyzer):
    set_response(analyzer, "Sure! Here is the analysis: not json")

    with pytest.raises(AIResponseError):
        analyzer.analyze_resume("resume text")


def test_non_object_json_raises_response_error(analyzer):
    set_response(analyzer, json.dumps(["strength"]))

    with pytest.raises(AIResponseError):
        analyzer.analyze_resume("resume text")


def test_wrong_field_type_raises_response_error(analyzer):
    set_response(
        analyzer,
        json.dumps({**VALID_PAYLOAD, "strengths": "Strong FastAPI experience"}),
    )

    with pytest.raises(AIResponseError):
        analyzer.analyze_resume("resume text")


def test_payload_without_analysis_fields_raises_response_error(analyzer):
    set_response(analyzer, json.dumps({"irrelevant": "value"}))

    with pytest.raises(AIResponseError):
        analyzer.analyze_resume("resume text")


def test_partial_payload_is_normalized(analyzer):
    set_response(
        analyzer,
        json.dumps({"summary": "Solid junior backend profile."}),
    )

    result = analyzer.analyze_resume("resume text")

    assert result == {
        "summary": "Solid junior backend profile.",
        "strengths": [],
        "weaknesses": [],
        "missing_skills": [],
        "recommendations": [],
    }


@pytest.mark.parametrize(
    "exc",
    [
        api_error(401, "API key not valid"),
        api_error(429, "Quota exceeded"),
        api_error(500, "Internal error"),
        httpx.ConnectError("connection refused"),
        httpx.ReadTimeout("request timed out"),
    ],
)
def test_api_failures_raise_service_error(analyzer, exc):
    set_failure(analyzer, exc)

    with pytest.raises(AIServiceError):
        analyzer.analyze_resume("resume text")
