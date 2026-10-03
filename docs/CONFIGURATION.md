# Configuration Reference

The application can be configured via a JSON file (default `config.json` or `~/.config/gemini-web2api/config.json`), via environment variables (in some contexts like Cloudflare/Docker), or via command-line arguments.

## Configuration Variables

| Name | JSON Key | Purpose | Default Value | Required |
|------|----------|---------|---------------|----------|
| **Port** | `port` | The port the HTTP server listens on. | `8081` | No |
| **Host** | `host` | The interface to bind the HTTP server to. | `"0.0.0.0"` | No |
| **Retry Attempts** | `retry_attempts` | Number of times to retry a failed upstream Gemini request. | `3` | No |
| **Retry Delay** | `retry_delay_sec` | Base delay between retries. | `2` | No |
| **Timeout** | `request_timeout_sec` | Upstream request timeout in seconds. | `180` | No |
| **Gemini Build Label** | `gemini_bl` | The exact frontend version identifier of Gemini Web. Must match Google's current expected version or requests will 405. | `"boq_assistant-bard-web-server_20260716.08_p0"` | **Yes** (defaults provided) |
| **Auth User** | `auth_user` | Multi-account index (e.g., `1` for `/u/1/app`). Used when authenticated with multiple Google accounts. | `null` | No |
| **XSRF Token** | `xsrf_token` | The page XSRF token (found in source as `SNlM0e`). Sometimes required for authenticated requests. | `null` | No |
| **Default Model** | `default_model` | Model to use if the client request omits one. | `"gemini-3.6-flash"` | No |
| **API Keys** | `api_keys` | Array of strings representing valid API keys for the client. If empty, authentication is disabled. | `[]` | No |
| **Cookie File** | `cookie_file` | Absolute or relative path to a file containing Google session cookies. Needed for `gemini-3.1-pro` routing and multimodal uploads. | `null` | No |
| **Proxy** | `proxy` | HTTP proxy for upstream requests (e.g. `http://127.0.0.1:7890`). | `null` | No |
| **Log Requests** | `log_requests` | Whether to print requests to stdout/stderr. | `true` | No |
| **Temporary Chats** | `temporary_chats` | If true, chats are not saved to the user's Google account history. | `false` | No |

## Environment Variables (Cloudflare specific)
The Cloudflare deployment (`worker.js`) relies entirely on Environment Variables injected by the platform. It supports identical configuration concepts, typically formatted as `UPPER_SNAKE_CASE` strings. 

- `COOKIE_STRING`: Can contain multiple cookies separated by `|` for rotation.
- `SAPISID`: Can contain multiple SAPISID hashes separated by `|`.
- `API_KEYS`: JSON array string (e.g. `["key1", "key2"]`).
- `RATE_LIMIT_MAX`: Max requests per window.
- `RATE_LIMIT_WINDOW`: Time window in seconds.
- `FINGERPRINT_JITTER_MS`: Delay jitter to prevent bot detection.

## Secret Management

> **SECRET — DO NOT COMMIT**

The following files and configuration values contain sensitive information and must never be committed to source control:
- `cookie.txt` (or any file designated by `cookie_file`)
- The `api_keys` array (if configured with real keys)
- The `xsrf_token`

## Configuration Inconsistencies
- **CLI vs JSON**: The Python single-file script and package both parse CLI arguments (`--port`, `--config`, `--cookie-file`, `--proxy`), which override `config.json` values.
- **Docker**: Docker users must mount their own `config.json` or `cookie.txt` into the container, as defaults are baked in.
- **Auto-Updating**: The `gemini_bl` configuration variable is automatically updated at runtime by the script if a 405 error occurs (it scrapes the live page for the newest token).
