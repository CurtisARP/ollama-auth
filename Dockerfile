FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
COPY README.md .
COPY ollama_auth ./ollama_auth
COPY main.py ./main.py

RUN python -m pip install --no-cache-dir .

EXPOSE 5000

ENV HOST=0.0.0.0
ENV PORT=5000

CMD ["python", "main.py"]
