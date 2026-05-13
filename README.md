# ollama-auth

A lightweight Flask proxy that adds API key authentication in front of an Ollama instance.

## Why

Ollama has no built-in authentication. Anyone who can reach your port can query your models and consume your compute. This proxy sits in front of Ollama and enforces API key validation on every request — without modifying Ollama's behavior or API surface.

## Features

- Bearer token and `X-API-Key` header authentication
- Full passthrough of all Ollama-compatible OpenAI API requests
- Multiple API keys support via comma-separated list
- Health and status endpoints
- Pre-built image on GHCR — no build step required
- Coolify-ready with automatic sslip.io domain and TLS

## Quick start

### Docker (standalone, Ollama already running)

```bash
docker run -p 5000:5000 \
  -e OLLAMA_UPSTREAM_URL=http://host.docker.internal:11434 \
  -e OLLAMA_API_KEY=my-secret-key \
  ghcr.io/curtisarp/ollama-auth:latest
```

### Docker Compose (local)

```bash
docker compose -f docker-compose.local.yml up -d
docker compose -f docker-compose.local.yml exec ollama ollama pull llama3
```

Send a request through the proxy:

```bash
curl -H "Authorization: Bearer my-secret-key" http://localhost:5000/v1/models
```

### Coolify

Use `docker-compose.coolify.yml` directly in Coolify as a Docker Compose service. It will:

- Build the proxy from this repo
- Start an Ollama instance on an isolated internal network
- Expose only the proxy via Traefik with automatic HTTPS and a generated sslip.io domain
- Keep Ollama unreachable from outside — all traffic must go through the authenticated proxy

After deployment, pull a model via the Coolify container console:

```bash
ollama pull llama3
```

## Configuration

| Variable | Default | Description |
|---|---|---|
| `OLLAMA_UPSTREAM_URL` | `http://localhost:11434` | URL of the Ollama instance |
| `OLLAMA_API_KEY` | — | Single valid API key |
| `OLLAMA_API_KEYS` | — | Comma-separated list of valid API keys |
| `HOST` | `0.0.0.0` | Bind address |
| `PORT` | `5000` | Port to listen on |
| `DEBUG` | `false` | Enable Flask debug mode (`true`, `1`, `yes`) |
| `REQUEST_TIMEOUT` | `60` | Upstream request timeout in seconds |

`OLLAMA_API_KEY` and `OLLAMA_API_KEYS` are both supported and merged — use either or both.

## Authentication

Every request must include one of:

```
Authorization: Bearer <key>
X-API-Key: <key>
```

Requests without a valid key receive a `401 Unauthorized` response.

## Endpoints

| Endpoint | Description |
|---|---|
| `GET /health` | Returns 200 if the proxy is running |
| `GET /status` | Returns proxy and upstream status |
| `/*` | Proxied to Ollama upstream |

## Run locally (Python)

```bash
# Install dependencies
python -m pip install .

# Run
export OLLAMA_UPSTREAM_URL=http://localhost:11434
export OLLAMA_API_KEY=my-secret-key
python main.py
```

With `uv` and auto-reload:

```bash
uv run main.py --reload
```

## Security model

In Docker Compose deployments, Ollama is intentionally **not** exposed to the host or public network. It only exists on an internal Docker bridge network shared with the proxy. The proxy is the sole entry point — no `ports:` mapping on Ollama means port 11434 is never reachable from outside the container network.

```
Internet → Traefik (HTTPS) → ollama-auth:5000 → ollama:11434 (internal only)
```

## Image

Pre-built and published to GHCR on every push to `master`:

```
ghcr.io/curtisarp/ollama-auth:latest
ghcr.io/curtisarp/ollama-auth:<git-sha>
```

---

## Contact

For questions, feedback, or contributions feel free to reach out.

| | |
|---|---|
| 𝕏 (Twitter) | [@curtis_sx](https://x.com/Curtis_SX) |
| Email | [curtis1337wastaken@protonmail.com](mailto:curtis1337wastaken@protonmail.com) |