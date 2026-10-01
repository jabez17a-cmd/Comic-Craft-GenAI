from types import SimpleNamespace

import pytest
from google.genai.errors import APIError

from app.services.gemini import GeminiService


class FakeModels:
    def __init__(self, errors):
        self.errors = list(errors)
        self.calls = 0
        self.requested_models = []

    def generate_content(self, **kwargs):
        self.calls += 1
        self.requested_models.append(kwargs.get("model"))
        if self.errors:
            raise self.errors.pop(0)
        return "response"


def make_api_error(code):
    return APIError(
        code,
        {"error": {"code": code, "status": "ERROR"}},
    )


def test_generate_content_retries_temporary_errors(monkeypatch):
    models = FakeModels(
        [make_api_error(503), make_api_error(503)]
    )
    client = SimpleNamespace(models=models)
    service = GeminiService("", "", "", 1)
    delays = []
    monkeypatch.setattr(
        "app.services.gemini.time.sleep",
        delays.append,
    )

    result = service._generate_content(client, model="test")

    assert result == "response"
    assert models.calls == 3
    assert delays == [1, 2]


def test_generate_content_uses_fallback_after_primary_retries(monkeypatch):
    models = FakeModels(
        [make_api_error(503), make_api_error(503), make_api_error(503)]
    )
    client = SimpleNamespace(models=models)
    service = GeminiService("", "primary", "fallback", 1)
    delays = []
    monkeypatch.setattr(
        "app.services.gemini.time.sleep",
        delays.append,
    )

    result = service._generate_content(
        client,
        model="primary",
        fallback_model="fallback",
    )

    assert result == "response"
    assert models.requested_models == [
        "primary",
        "primary",
        "primary",
        "fallback",
    ]
    assert delays == [1, 2]


def test_generate_content_fails_over_immediately_on_quota_error():
    models = FakeModels([make_api_error(429)])
    client = SimpleNamespace(models=models)
    service = GeminiService("", "primary", "fallback", 1)

    result = service._generate_content(
        client,
        model="primary",
        fallback_model="fallback",
    )

    assert result == "response"
    assert models.requested_models == ["primary", "fallback"]


def test_generate_content_does_not_retry_invalid_key_errors():
    models = FakeModels([make_api_error(401)])
    client = SimpleNamespace(models=models)
    service = GeminiService("", "", "", 1)

    with pytest.raises(APIError):
        service._generate_content(client, model="test")

    assert models.calls == 1