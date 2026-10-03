# Deployment

`gemini-web2api` is designed to be deployed in several primary ways: via Docker/VPS, via Serverless Edge (Cloudflare Workers), or via PaaS providers like Northflank.

- [Northflank Deployment Guide](NORTHFLANK_DEPLOYMENT.md)

## 1. Docker Deployment (Local / VPS)

The repository provides a `Dockerfile` and `docker-compose.local.yml`.

### Architecture
```text
Source Code
 ↓
Docker Build (python:3.12-slim)
 ↓
Container (`python -m gemini_web2api`)
```

### Build & Run
```bash
cp config.example.json config.json
docker compose -f docker-compose.local.yml up -d
```

### Important Configuration
When running in Docker, you **must** mount your configuration and cookie files so they persist.
```yaml
volumes:
  - ./config.json:/app/config.json
  - ./cookie.txt:/app/cookie.txt
```
**Known Issue**: Docker NAT IP ranges are sometimes blocked or heavily throttled by Google. If you receive empty responses, use `network_mode: host` to bypass Docker NAT.

## 2. Cloudflare Workers Deployment

The repository contains a fully independent JavaScript implementation (`cloudflare/worker.js`) optimized for edge deployment.

### Deployment Steps
1. Log into Cloudflare Dashboard -> Workers & Pages.
2. Create a new Worker.
3. Paste the contents of `cloudflare/worker.js` into the editor.
4. Save and Deploy.

### Environment Variables
Configure the following in the Cloudflare Dashboard settings for the Worker:
- `COOKIE_STRING`: Full cookie string exported from browser. (Supports multiple separated by `|`).
- `SAPISID`: Associated SAPISID.
- `API_KEYS`: JSON array of acceptable client API keys (e.g., `["sk-123", "sk-456"]`).
- `DEFAULT_MODEL`: e.g. `gemini-3.6-flash`.

### Cloudflare Worker Features
The Worker implementation uses advanced techniques to avoid bot detection:
- **Fingerprint Rotation**: Rotates `User-Agent`, `Accept-Language`, and `Sec-Ch-Ua` arrays randomly.
- **Jitter**: Introduces random delay (`FINGERPRINT_JITTER_MS`) before requests.
- **Memory Safe Rate Limiting**: Uses a stochastic garbage collection mechanism on maps to prevent memory leaks in the V8 Isolate.
