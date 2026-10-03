# Project Overview

## Purpose
`gemini-web2api` is a zero-cost, cross-platform proxy that converts Google Gemini's web interface into an OpenAI-compatible API server. 
It allows developers and applications (like Cherry Studio, ChatBox, or OpenAI's SDK) that expect the standard OpenAI API format (`/v1/chat/completions`) to interact seamlessly with Google's Gemini models using the native web endpoints.

## Problem It Solves
Accessing the Gemini API normally requires API keys, and advanced models may require paid tiers or quota limitations. `gemini-web2api` circumvents these requirements by reverse-engineering Google Gemini's web `StreamGenerate` protocol. It essentially masquerades as the Gemini Web client, removing the need for a developer API key, and providing free access to Gemini's capabilities for local clients.

## Main Functionality
- Acts as a local HTTP server that accepts OpenAI-formatted requests.
- Converts these requests into Google's internal protobuf-like payload format.
- Connects to `https://gemini.google.com/app` and `https://gemini.google.com/_/BardChatUi/data/...` endpoints.
- Processes the response (handling both streaming SSE and non-streaming) and formats it back into OpenAI JSON responses.
- Supports Image/Multimodal inputs (by uploading them to Google's Scotty resumable upload service).
- Supports Tool Calling (function calling) mapping OpenAI format to Gemini's native tool formats.
- Supports alternative deployment to Cloudflare Workers.

## Major Components
1. **HTTP Server (`server.py`)**: Accepts HTTP requests, parses `/v1/chat/completions`, handles authentication, and outputs Server-Sent Events (SSE) or JSON.
2. **Gemini Protocol Client (`gemini.py`)**: Implements the payload construction and network communication with Gemini's backend.
3. **Multimodal Uploader (`multimodal.py`)**: Uses Scotty resumable uploads to push images to Gemini's temporary storage, returning references used in the prompt.
4. **Tool/Message Parser (`tools.py`)**: Converts OpenAI message histories and tool call configurations into Gemini format, and parses Gemini's raw tool responses back to OpenAI format.
5. **Configuration (`config.py`)**: Manages environment variables, CLI args, and `config.json`.
6. **Cloudflare Worker (`cloudflare/worker.js`)**: An alternative, fully independent implementation of the proxy optimized for Edge deployment with advanced fingerprinting and rate-limiting.

## Technology Stack
- **Language**: Python 3.8+ (for local/Docker deployment), JavaScript (for Cloudflare Workers)
- **Dependencies**: 
  - Standard library (`http.server`, `urllib`, `json`, `ssl`, `re`)
  - `httpx` (Optional but recommended, for streaming support)
- **Deployment**: Docker, Docker Compose, Cloudflare Workers, Local execution.

## High-Level Execution Flow
1. **Startup**: User runs `python -m gemini_web2api` or `python gemini_web2api.py`. The HTTP server starts on port 8081.
2. **Request Reception**: Client sends a POST request to `/v1/chat/completions`.
3. **Parsing**: The `GeminiHandler` parses the OpenAI JSON payload, extracting the `messages`, `model`, `tools`, and `stream` flag.
4. **Model Resolution**: Maps the requested model (e.g., `gemini-3.5-flash-thinking`) to Gemini's internal IDs (e.g., mode: 2, think: 0).
5. **Payload Construction**: Translates messages and tools into the `StreamGenerate` nested array format. If there are images, `multimodal.py` uploads them first.
6. **Upstream Request**: Sends the request to `https://gemini.google.com/.../StreamGenerate` using `urllib` or `httpx` with the appropriate headers (including optional cookies).
7. **Response Streaming**: 
   - If streaming: Reads the response line by line, extracts incremental text deltas, and sends them to the client as SSE chunks.
   - If non-streaming: Accumulates the full response, parses it, and sends a single JSON response.
8. **Completion**: Closes the connection.

## Important External Dependencies
- **Google Gemini Web Endpoints**:
  - `https://gemini.google.com/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate` (Chat)
  - `https://content-push.googleapis.com/upload/` (Image Uploads)
- **HTTPX**: Used for reliable HTTP stream processing (urllib blocks on chunked streams).

## Important Terminology
- **StreamGenerate**: Google's internal endpoint for the Gemini web UI.
- **SAPISID**: A crucial cookie used by Google for authentication. It is hashed with the timestamp to generate the `Authorization` header.
- **BL (Build Label)**: An identifier (e.g., `boq_assistant-bard-web-server_2026...`) representing the current version of the Gemini frontend. If mismatched, requests return HTTP 405.
- **Think Mode**: Configures the depth of reasoning. Mapped via `@think=N` syntax.
- **Scotty**: Google's internal resumable upload infrastructure used for uploading images.
