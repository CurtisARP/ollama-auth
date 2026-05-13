import os
from typing import List, Optional


def _split_api_keys(raw: Optional[str]) -> List[str]:
    if not raw:
        return []
    return [key.strip() for key in raw.split(",") if key.strip()]


class Settings:
    def __init__(self):
        self.ollama_upstream_url = os.environ.get("OLLAMA_UPSTREAM_URL", "http://localhost:11434")
        api_key = os.environ.get("OLLAMA_API_KEY")
        api_keys = _split_api_keys(os.environ.get("OLLAMA_API_KEYS", ""))
        self.ollama_api_keys = ([api_key.strip()] if api_key else []) + api_keys
        self.host = os.environ.get("HOST", "0.0.0.0")
        self.port = int(os.environ.get("PORT", "5000"))
        self.debug = os.environ.get("DEBUG", "false").lower() in {"1", "true", "yes"}
        self.request_timeout = float(os.environ.get("REQUEST_TIMEOUT", "60"))

    @property
    def has_api_keys(self) -> bool:
        return bool(self.ollama_api_keys)
