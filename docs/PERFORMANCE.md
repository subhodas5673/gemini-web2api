# Performance & Resource Analysis

## 1. Network & Streaming
- **urllib vs httpx**: The proxy supports both standard `urllib` and `httpx`. `urllib` handles chunked transfer encoding poorly and can cause buffering. The proxy prioritizes `httpx` for streaming (`generate_stream`).
- **Streaming Efficiency**: When `httpx` is used, SSE chunks are pushed to the client immediately as they are parsed from Google's `wrb.fr` stream, providing a highly responsive type-writer effect.

## 2. Concurrency
- **Python**: Uses `socketserver.ThreadingMixIn`, meaning each incoming HTTP request spawns a new thread. 
- **Resource Constraints**: Python's Global Interpreter Lock (GIL) is not a significant bottleneck here because the workload is heavily I/O bound (waiting for Google's API to respond). However, a massive number of concurrent connections could exhaust available threads or memory.

## 3. Large File Processing
- **Base64 Images**: The proxy accepts base64-encoded images in the JSON payload.
- **Compression**: `tools.py` implements an optional compression step (`_compress_b64_if_needed`) using the `PIL` library. If an image exceeds `MAX_IMAGE_B64_SIZE` (~37KB), it resizes and recompresses it to JPEG before upload. This prevents massive payload overheads and speeds up upload times to Google's Scotty endpoint.

## 4. Cloudflare Workers Performance
- The `worker.js` implementation operates on the edge, providing extremely low-latency routing.
- **Rate Limiting**: Custom rate limiting is implemented to protect the worker and upstream endpoints.
- **Memory Management**: The worker uses a `Map` for rate limiting (`rateLimitStore`). Because Cloudflare isolates can be long-lived, the developer implemented a stochastic garbage collection mechanism (5% chance per request to clean stale entries) to prevent memory leaks over time.

## 5. Caching
- **Page Tokens**: In `multimodal.py`, the Google page tokens (`push_id`, `pctx`) required for image uploads are cached in memory for 10 minutes (`600` seconds) to avoid performing a full HTML fetch on every image upload.
- **Cookies**: `gemini.py` caches the cookie file contents and checks the file's `mtime` (modified time). It only re-reads the disk if the file has changed.
