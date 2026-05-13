from ollama_auth import create_app
from ollama_auth.config import Settings

settings = Settings()
app = create_app(settings)


def main():
    app.run(host=settings.host, port=settings.port, debug=settings.debug)


if __name__ == "__main__":
    main()
