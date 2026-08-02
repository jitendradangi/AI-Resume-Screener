from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from app.ai.resume_analyzer import AIAnalysisError, AIServiceError
from app.services.resume_analysis import ResumeAnalysisService


AI_RESULT = {
    "summary": "Backend developer.",
    "strengths": ["FastAPI"],
    "weaknesses": ["No metrics"],
    "missing_skills": ["Docker"],
    "recommendations": ["Quantify impact"],
}


@pytest.fixture
def resume():
    return SimpleNamespace(id=1, user_id=7, filepath="uploads/resume.pdf")


@pytest.fixture
def repositories(monkeypatch, resume):
    resume_repo = MagicMock()
    resume_repo.get_by_public_id.return_value = resume

    analysis_repo = MagicMock()
    analysis_repo.get_by_resume.return_value = None
    analysis_repo.create.side_effect = lambda db, **kwargs: SimpleNamespace(**kwargs)
    analysis_repo.update.side_effect = lambda db, obj, **kwargs: SimpleNamespace(
        **kwargs
    )

    monkeypatch.setattr(
        "app.services.resume_analysis.resume_repository",
        resume_repo,
    )
    monkeypatch.setattr(
        "app.services.resume_analysis.resume_analysis_repository",
        analysis_repo,
    )

    return resume_repo, analysis_repo


@pytest.fixture
def analyzer():
    analyzer = MagicMock()
    analyzer.analyze_resume.return_value = dict(AI_RESULT)
    return analyzer


def test_creates_analysis_from_parsed_resume(
    monkeypatch, repositories, analyzer
):
    _, analysis_repo = repositories

    monkeypatch.setattr(
        "app.services.resume_analysis.TextExtractor.extract",
        staticmethod(lambda path: "Jane Doe\nPython"),
    )
    monkeypatch.setattr(
        "app.services.resume_analysis.ResumeParser.parse",
        staticmethod(lambda text: {"name": "Jane Doe", "skills": ["Python"]}),
    )

    service = ResumeAnalysisService(MagicMock())
    analysis = service.run_ai_analysis("resume-uuid", 7, analyzer)

    assert analysis.summary == AI_RESULT["summary"]
    assert analysis.strengths == AI_RESULT["strengths"]
    assert analysis.weaknesses == AI_RESULT["weaknesses"]
    assert analysis.missing_skills == AI_RESULT["missing_skills"]
    assert analysis.recommendations == AI_RESULT["recommendations"]
    assert analysis_repo.create.called
    assert not analysis_repo.update.called


def test_existing_analysis_is_updated_not_duplicated(
    monkeypatch, repositories, analyzer
):
    _, analysis_repo = repositories
    analysis_repo.get_by_resume.return_value = SimpleNamespace(
        raw_text="Jane Doe\nPython",
        parsed_data={"skills": ["Python"]},
    )

    extract = MagicMock()
    monkeypatch.setattr(
        "app.services.resume_analysis.TextExtractor.extract",
        extract,
    )

    service = ResumeAnalysisService(MagicMock())
    service.run_ai_analysis("resume-uuid", 7, analyzer)

    # Stored resume text is reused instead of parsing the file again.
    assert not extract.called
    assert analysis_repo.update.called
    assert not analysis_repo.create.called

    analyzer.analyze_resume.assert_called_once_with(
        "Jane Doe\nPython",
        {"skills": ["Python"]},
    )


def test_unknown_resume_raises_value_error(repositories, analyzer):
    resume_repo, _ = repositories
    resume_repo.get_by_public_id.return_value = None

    service = ResumeAnalysisService(MagicMock())

    with pytest.raises(ValueError):
        service.run_ai_analysis("missing", 7, analyzer)


def test_other_users_resume_raises_permission_error(repositories, analyzer):
    service = ResumeAnalysisService(MagicMock())

    with pytest.raises(PermissionError):
        service.run_ai_analysis("resume-uuid", 99, analyzer)


def test_unreadable_file_raises_analysis_error(
    monkeypatch, repositories, analyzer
):
    monkeypatch.setattr(
        "app.services.resume_analysis.TextExtractor.extract",
        MagicMock(side_effect=ValueError("Unsupported file format")),
    )

    service = ResumeAnalysisService(MagicMock())

    with pytest.raises(AIAnalysisError):
        service.run_ai_analysis("resume-uuid", 7, analyzer)


def test_ai_failure_is_propagated_and_nothing_is_saved(
    monkeypatch, repositories, analyzer
):
    _, analysis_repo = repositories
    analysis_repo.get_by_resume.return_value = SimpleNamespace(
        raw_text="Jane Doe",
        parsed_data={},
    )
    analyzer.analyze_resume.side_effect = AIServiceError("Gemini unavailable")

    service = ResumeAnalysisService(MagicMock())

    with pytest.raises(AIServiceError):
        service.run_ai_analysis("resume-uuid", 7, analyzer)

    assert not analysis_repo.create.called
    assert not analysis_repo.update.called
