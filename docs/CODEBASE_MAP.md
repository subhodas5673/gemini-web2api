# Codebase Map

The repository is structured to support multiple execution environments: standard Python, Docker, and Cloudflare Workers.

```text
gemini-web2api/
├── gemini_web2api.py            → Standalone, single-file version of the proxy server.
├── gemini_web2api/              → Modular package version of the application.
│   ├── __main__.py              → CLI entry point for the modular package.
│   ├── server.py                → HTTP server handling OpenAI endpoints and SSE formatting.
│   ├── gemini.py                → Core client for the Google Gemini StreamGenerate protocol.
│   ├── tools.py                 → Parser for OpenAI tools and message histories.
│   ├── multimodal.py            → Logic for uploading images to Google's Scotty API.
│   ├── models.py                → Model dictionary and resolution logic.
│   └── config.py                → Configuration management and defaults.
├── cloudflare/                  
│   └── worker.js                → Independent JavaScript implementation for Cloudflare Workers.
├── gemini-cookie-sync-extension/→ Browser extension to export Gemini cookies.
├── Dockerfile                   → Defines the Docker container environment.
├── docker-compose.local.yml     → Local docker-compose configuration.
├── pyproject.toml               → Python packaging and dependency declarations.
└── config.example.json          → Template for local configuration.
```

## Important Files

### `gemini_web2api/server.py`
- **Purpose**: The HTTP interface of the proxy.
- **Main Responsibility**: Implements `GeminiHandler` (subclass of `BaseHTTPRequestHandler`). Routes requests to `/v1/chat/completions`, `/v1/responses`, and `/v1beta/models`.
- **Modification Sensitivity**: High. This file manages the exact JSON shapes and SSE formats required by OpenAI clients. Breaking the format here will break client integrations.

### `gemini_web2api/gemini.py`
- **Purpose**: Google Gemini upstream communication.
- **Main Responsibility**: Implements `generate` and `generate_stream`. Constructs the complex nested JSON array `[None, None, [prompt, ...]]` payload expected by the Gemini Web UI. Handles SAPISID authentication generation.
- **Dependencies**: Uses `httpx` if available, otherwise `urllib.request`.
- **Modification Sensitivity**: High. The payload structure is strictly validated by Google's backend. Any incorrect array index will result in an HTTP 400 or upstream rejection.

### `gemini_web2api/multimodal.py`
- **Purpose**: Image handling.
- **Main Responsibility**: Fetches page tokens (`push_id`, `pctx`) from the Gemini Web UI, and uses them to initiate a resumable upload to `content-push.googleapis.com/upload/`.
- **Callers**: Called by `server.py` before executing the main chat request if images are present in the user prompt.

### `gemini_web2api.py`
- **Purpose**: A monolithic script version.
- **Note**: It contains duplicated logic from the `gemini_web2api/` module, packaged into a single file. Modifications to the core logic must likely be synced between this file and the `gemini_web2api/` directory.

### `cloudflare/worker.js`
- **Purpose**: Serverless deployment.
- **Main Responsibility**: Complete JavaScript port of the application, heavily optimized for Cloudflare Workers. Contains complex logic for state isolation across isolates and browser fingerprint rotation.
- **Modification Sensitivity**: Very High. Careless modifications can cause global variable leakage (cross-request data contamination) in the V8 Isolate environment.
