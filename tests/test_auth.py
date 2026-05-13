import pytest
from flask import Flask
from ollama_auth.config import Settings
from ollama_auth.app import create_app


def test_no_api_keys_configured(monkeypatch):
    monkeypatch.delenv("OLLAMA_API_KEY", raising=False)
    monkeypatch.setenv("OLLAMA_API_KEYS", "")
    app = create_app(Settings())
    client = app.test_client()

    response = client.get("/status")
    assert response.status_code == 200
    assert response.json["api_keys_configured"] is False


def test_invalid_api_key(monkeypatch):
    monkeypatch.setenv("OLLAMA_API_KEY", "valid-key")
    app = create_app(Settings())
    client = app.test_client()

    response = client.get("/v1/models")
    assert response.status_code == 401
