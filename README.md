# ollama-auth

A lightweight Flask proxy that adds API key authentication in front of an Ollama API instance.

## Why this project

The current Ollama version don't implement auth, forcing anyone who need an API exposition to expose thier port and therefore allowing anyone to query thier models when self-hosted, it's a huge security issue that can easily be resolved with this wrapper that act as an authentication layer

## Features

- Enforces bearer token or `X-API-Key` authentication
- Forwards all Ollama-compatible OpenAPI requests to the configured upstream
- Includes health and status endpoints
- Supports local Python execution and Docker deployment

## Configuration

Set the following environment variables:

- `OLLAMA_UPSTREAM_URL`: URL of the Ollama API server (default: `http://localhost:11434`)
- `OLLAMA_API_KEY`: a single valid API key
- `OLLAMA_API_KEYS`: comma-separated list of valid API keys (backward-compatible)
- `HOST`: host address to bind (default: `0.0.0.0`)
- `PORT`: port to listen on (default: `5000`)
- `DEBUG`: enable Flask debug mode (`true`, `1`, `yes`)
- `REQUEST_TIMEOUT`: request timeout in seconds (default: `60`)

## Run locally

Install dependencies:

```bash
python -m pip install .
```

Run the proxy with `python`:

```bash
export OLLAMA_UPSTREAM_URL=http://localhost:11434
export OLLAMA_API_KEY=my-secret-key
python main.py
```

Run the proxy with `uv`:

```bash
export OLLAMA_UPSTREAM_URL=http://localhost:11434
export OLLAMA_API_KEY=my-secret-key
uv run main.py
```

If you want auto-reload during development:

```bash
uv run main.py --reload
```

Send requests through the proxy:

```bash
curl -H "Authorization: Bearer my-secret-key" http://localhost:5000/v1/models
```

## Docker

Build and run the image:

```bash
docker build -t ollama-auth .
docker run -p 5000:5000 \
  -e OLLAMA_UPSTREAM_URL=http://host.docker.internal:11434 \
  -e OLLAMA_API_KEY=my-secret-key \
  ollama-auth
```

Or use `docker-compose`:

```bash
docker compose up --build
```

## Health checks

- `GET /health`
- `GET /status`

## Notes

This proxy does not modify the Ollama API behavior; it only adds an authentication layer in front of an existing Ollama instance.