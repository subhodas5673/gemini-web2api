# Security Analysis

This document outlines the security posture of `gemini-web2api`.

## 1. Authentication & Authorization

### Client to Proxy
- **Mechanism**: The proxy uses a simple bearer token implementation matching the OpenAI spec (`Authorization: Bearer <key>` or `x-api-key`).
- **Configuration**: Managed via the `api_keys` array in `config.json`.
- **Observed Risk**: If `api_keys` is left empty (`[]`), the proxy allows completely unauthenticated access. This is dangerous if the proxy is exposed to the public internet, as it allows anyone to consume the proxy's bandwidth and Google API limits.
- **Recommendation**: Always set strong API keys if deploying to a public-facing IP or Cloudflare Workers.

### Proxy to Google (Upstream)
- **Mechanism**: The proxy relies on extracting and transmitting Google session cookies (`__Secure-1PSID`, `SAPISID`, etc.) extracted from a real browser.
- **SAPISIDHASH**: The proxy accurately recreates the Google authentication header by hashing the `SAPISID` cookie with the current timestamp.
- **Observed Risk**: Cookie files (`cookie.txt`) grant full access to the associated Google account's Gemini history. If this file is leaked, attackers can view/delete Gemini conversations.

## 2. Secrets Management
- Secrets (`api_keys`, `cookie_file`) are loaded from disk or environment variables.
- **Potential Risk**: Docker deployments might accidentally bake `cookie.txt` into the image layer if `.dockerignore` is not configured correctly or the `COPY` commands overlap the cookie file location. 

## 3. Injection Risks
- **Prompt Injection**: The proxy passes user prompts directly to Google Gemini. Gemini's native safety filters handle prompt injection and jailbreaks. The proxy itself does not execute or evaluate prompt contents.
- **Payload Integrity**: The OpenAI messages are JSON-serialized into Google's payload format. 

## 4. Input Validation
- The server performs basic JSON validation (`json.loads(body)`). If invalid, returns HTTP 400.
- **Potential Risk**: Very large JSON payloads could cause Memory/CPU spikes (Denial of Service). There is no explicit maximum request body size limit enforced by the `BaseHTTPRequestHandler` implementation before reading.

## 5. Security Boundaries
The application is designed as a direct passthrough. It does not store chat history locally or in a database, avoiding PII storage concerns. However, data transmitted to Google is governed by Google's Privacy Policy. 

> **Important**: If `temporary_chats` is false (the default), prompts and responses sent through this proxy **are stored in the Google account's Gemini history**. Do not send sensitive personal data unless you intend for it to be stored by Google.
