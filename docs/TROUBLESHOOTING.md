# Troubleshooting

## Problem: Requests return HTTP 405 Method Not Allowed

### Symptoms
Client applications fail to connect, and the server logs show repeated HTTP 405 errors from upstream.

### Likely Cause
Google has updated the Gemini frontend, and the `gemini_bl` (Build Label) value in your configuration is stale.

### How to Diagnose
Check the logs. If you see `Retrying with updated BL...`, the proxy is attempting to auto-update. If it still fails, the fallback mechanism couldn't scrape the new label.

### Solution
Manually update `gemini_bl`:
1. Open `https://gemini.google.com/app` in a browser.
2. Open DevTools (F12) -> Network.
3. Search for requests containing `boq_assistant-bard-web-server`.
4. Copy the full identifier (e.g., `boq_assistant-bard-web-server_20261001.10_p0`).
5. Update `config.json`.

### Relevant Files
- `gemini_web2api/config.py`
- `gemini_web2api/gemini.py` (auto-update logic)

---

## Problem: Upstream rejected request: BardErrorInfo [X]

### Symptoms
The proxy returns a `502 Bad Gateway` containing `"upstream error: Gemini upstream rejected request: BardErrorInfo [X]"`.

### Likely Cause
This is a strict internal rejection from Google's backend. 
- **[Error 33]**: Typically means the account requires acceptance of Terms of Service, or the prompt violates safety policies.
- **Other codes**: Can mean the payload format was malformed (e.g. invalid `refs` index, missing multimodal fields).

### Solution
If you are using cookies, open the browser with that account and ensure you can use the Gemini web interface normally (dismiss any popups). If the error persists for all requests, the internal JSON payload structure in `gemini.py` may need updating to match a recent Google protocol change.

---

## Problem: Docker container returns empty responses (content: null)

### Symptoms
Running via `docker run` results in empty assistant responses or immediate stops, while running natively with Python works perfectly.

### Likely Cause
Google's WAF (Web Application Firewall) frequently blocks or rate-limits requests originating from default Docker NAT IP ranges (like `172.17.x.x`).

### Solution
Run the container using the host network mode to bypass Docker NAT:
`docker run --network host ...` or set `network_mode: host` in `docker-compose.local.yml`.

---

## Problem: Multimodal (image upload) fails with "No upload URL"

### Symptoms
Log shows `RuntimeError: No upload URL in response headers`.

### Likely Cause
The Scotty upload initialization endpoint (`content-push.googleapis.com`) rejected the request. Usually because the account requires authentication, or the `push_id` token is stale.

### Solution
Ensure `cookie_file` is properly configured. Anonymous users are sometimes restricted from uploading images.

### Relevant Files
- `gemini_web2api/multimodal.py`
