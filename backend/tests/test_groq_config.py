import pytest
from unittest.mock import MagicMock, patch
from app.core.config import Settings
from app.ai.resume_analyzer import ResumeAnalyzer, get_groq_model, get_groq_client
from app.matching.semantic_matcher import SemanticMatcher


def test_settings_groq_model_default():
    """Test that Settings includes GROQ_MODEL with default value."""
    settings = Settings(DATABASE_URL="sqlite:///:memory:", SECRET_KEY="test-key")
    assert hasattr(settings, "GROQ_MODEL")
    assert settings.GROQ_MODEL == "llama-3.3-70b-versatile"


def test_settings_groq_model_custom(monkeypatch):
    """Test overriding GROQ_MODEL via environment variable."""
    monkeypatch.setenv("GROQ_MODEL", "llama-3.1-8b-instant")
    settings = Settings(DATABASE_URL="sqlite:///:memory:", SECRET_KEY="test-key")
    assert settings.GROQ_MODEL == "llama-3.1-8b-instant"


def test_get_groq_model(monkeypatch):
    """Test get_groq_model reads settings correctly."""
    from app.core import config
    monkeypatch.setattr(config.settings, "GROQ_MODEL", "custom-groq-model")
    assert get_groq_model() == "custom-groq-model"


@patch("app.ai.resume_analyzer.get_groq_client")
def test_analyze_resume_uses_configured_model(mock_get_client, monkeypatch):
    """Test that analyze_resume uses the model specified in settings."""
    from app.core import config
    monkeypatch.setattr(config.settings, "GROQ_MODEL", "llama-3.1-8b-instant")

    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = '{"overall_score": 85, "strengths": ["Python"], "weaknesses": ["Docker"], "recommendations": ["Learn Kubernetes"]}'
    mock_response.choices = [mock_choice]
    mock_client.chat.completions.create.return_value = mock_response
    mock_get_client.return_value = mock_client

    result = ResumeAnalyzer.analyze_resume("Resume content", {"skills": ["Python"]})

    # Verify model passed to chat.completions.create is llama-3.1-8b-instant
    mock_client.chat.completions.create.assert_called_once()
    call_kwargs = mock_client.chat.completions.create.call_args.kwargs
    assert call_kwargs["model"] == "llama-3.1-8b-instant"
    assert result["overall_score"] == 85


@patch("app.ai.resume_analyzer.get_groq_client")
def test_analyze_resume_handles_invalid_model_error(mock_get_client, monkeypatch):
    """Test clean error handling when model does not exist or access is denied."""
    from app.core import config
    monkeypatch.setattr(config.settings, "GROQ_MODEL", "invalid-model-name")

    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("The model `invalid-model-name` does not exist or you do not have access to it.")
    mock_get_client.return_value = mock_client

    with pytest.raises(RuntimeError) as exc_info:
        ResumeAnalyzer.analyze_resume("Resume content", {})

    assert "Model 'invalid-model-name' is invalid or inaccessible" in str(exc_info.value)
    assert "GROQ_MODEL" in str(exc_info.value)


@patch("app.matching.semantic_matcher.get_groq_client")
def test_semantic_matcher_uses_configured_model(mock_get_client, monkeypatch):
    """Test that SemanticMatcher uses the model specified in settings."""
    from app.core import config
    monkeypatch.setattr(config.settings, "GROQ_MODEL", "llama-3.1-8b-instant")

    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = '{"semantic_score": 90, "strengths": ["Python"], "weaknesses": [], "reason": "Strong alignment"}'
    mock_response.choices = [mock_choice]
    mock_client.chat.completions.create.return_value = mock_response
    mock_get_client.return_value = mock_client

    SemanticMatcher.clear_cache()
    result = SemanticMatcher.compare_semantic("Job desc", "Resume text", {}, use_cache=False)

    mock_client.chat.completions.create.assert_called_once()
    call_kwargs = mock_client.chat.completions.create.call_args.kwargs
    assert call_kwargs["model"] == "llama-3.1-8b-instant"
    assert result["semantic_score"] == 90
