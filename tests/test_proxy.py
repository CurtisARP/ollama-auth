import pytest
from unittest.mock import patch
from ollama_auth.config import Settings
from ollama_auth.app import create_app


def test_proxy_passes_request(monkeypatch):
    monkeypatch.setenv("OLLAMA_API_KEY", "valid-key")
    monkeypatch.setenv("OLLAMA_UPSTREAM_URL", "http://localhost:11434")
    settings = Settings()
    app = create_app(settings)
    client = app.test_client()

    with patch("ollama_auth.proxy.requests.request") as mock_request:
        mock_request.return_value.status_code = 200
        mock_request.return_value.headers = {"Content-Type": "application/json"}
        mock_request.return_value.iter_content.return_value = [b"{}"]

        response = client.get("/v1/models", headers={"Authorization": "Bearer valid-key"})

        assert response.status_code == 200
        mock_request.assert_called_once()
