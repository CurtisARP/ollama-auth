from flask import Flask, jsonify, request
from .config import Settings
from .auth import require_api_key
from .proxy import proxy_request


def create_app(settings: Settings | None = None):
    settings = settings or Settings()
    app = Flask(__name__)

    @app.before_request
    def validate_api_key():
        if request.path in {"/health", "/", "/status"}:
            return None
        if not settings.has_api_keys:
            return (
                jsonify(
                    {
                        "error": "No API keys configured. Set OLLAMA_API_KEY or OLLAMA_API_KEYS."
                    }
                ),
                500,
            )
        require_api_key(settings.ollama_api_keys)()

    @app.route("/", methods=["GET"])
    def index():
        return jsonify(
            {
                "message": "Ollama Auth Proxy",
                "upstream": settings.ollama_upstream_url,
                "auth": "API key required",
            }
        )

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok"})

    @app.route("/status", methods=["GET"])
    def status():
        return jsonify(
            {
                "status": "ok",
                "upstream": settings.ollama_upstream_url,
                "api_keys_configured": settings.has_api_keys,
            }
        )

    @app.route("/<path:path>", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"])
    def proxy(path):
        return proxy_request(settings.ollama_upstream_url, settings.request_timeout)

    return app
