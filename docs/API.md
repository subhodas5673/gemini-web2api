# API Reference

`gemini-web2api` exposes a local HTTP server that aims to be 100% compatible with the OpenAI API for chat completions. 

## Base URL
Default: `http://127.0.0.1:8081/v1`

## Authentication
If `api_keys` is configured, requests must include one of the following:
- Header: `Authorization: Bearer <key>`
- Header: `x-api-key: <key>`
- Header: `x-goog-api-key: <key>`
- Query Parameter: `?key=<key>`

If `api_keys` is empty `[]`, authentication is skipped.

## Endpoints

### 1. Create Chat Completion
`POST /v1/chat/completions`

**Request Body (JSON):**
Matches the standard OpenAI Chat Completion specification.
- `model` (string)
- `messages` (array of objects)
- `stream` (boolean)
- `tools` (array of objects)
- `tool_choice` (string or object)

**Response:**
Standard OpenAI Chat Completion format, or SSE stream if `stream: true`.

### 2. List Models (OpenAI Format)
`GET /v1/models`

**Response:**
Returns a list of supported Gemini models formatted as OpenAI model objects.

### 3. List Models (Gemini Native Format)
`GET /v1beta/models`

**Response:**
Returns a list of models formatted identically to the official Google Gemini API (used by the Gemini CLI).

### 4. Generate Content (Gemini Native Format)
`POST /v1beta/models/{model}:generateContent`
`POST /v1beta/models/{model}:streamGenerateContent`

**Request & Response:**
Matches the official Google Gemini API format (`contents`, `parts`, `candidates`). Allows native Gemini SDKs to route through this proxy.

### 5. Responses API (Codex CLI)
`POST /v1/responses`

An alternative endpoint supporting the OpenAI Codex CLI format.

## Error Behavior
- `401 Unauthorized`: Invalid or missing API key.
- `400 Bad Request`: Invalid JSON, unknown model, empty prompt.
- `404 Not Found`: Unknown endpoint.
- `502 Bad Gateway`: Upstream error from Google Gemini (e.g., cookie expired, rate limited, network error).
- `500 Internal Server Error`: Unhandled proxy exception.
