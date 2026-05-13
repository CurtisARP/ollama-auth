from flask import abort, request
from typing import Tuple


def _extract_api_key() -> Tuple[str, str]:
    auth_header = request.headers.get("Authorization", "")
    if auth_header.lower().startswith("bearer "):
        return "Authorization", auth_header[7:].strip()

    api_key = request.headers.get("X-API-Key")
    if api_key:
        return "X-API-Key", api_key.strip()

    return "", ""


def require_api_key(valid_keys):
    def decorator():
        header_name, api_key = _extract_api_key()
        if not api_key or api_key not in valid_keys:
            abort(401, description="Unauthorized: invalid or missing API key")

    return decorator
