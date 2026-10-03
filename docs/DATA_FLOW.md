# Data Flow

This document traces the path of a standard OpenAI-compatible Chat Completion request through the system.

## 1. Chat Completion Request (`/v1/chat/completions`)

```mermaid
flowchart TD
    Client[Client App] -->|POST JSON Request| Handler[GeminiHandler.do_POST]
    
    Handler --> AuthCheck{Check Auth}
    AuthCheck -->|Failed| 401[Return 401 Unauthorized]
    AuthCheck -->|Passed| ParseJSON[Parse Request Body]
    
    ParseJSON --> ResolveModel[models.py: resolve_model]
    ResolveModel --> Extract[tools.py: messages_to_prompt]
    
    Extract -->|Text & Image Data| ImagesCheck{Images Present?}
    
    ImagesCheck -->|Yes| Upload[multimodal.py: upload_images]
    Upload -->|Returns File Refs| GenRequest
    ImagesCheck -->|No| GenRequest[gemini.py: generate_stream]
    
    GenRequest --> Payload[Build nested JSON Array]
    Payload --> Auth[Generate SAPISIDHASH]
    Auth --> Stream[POST /StreamGenerate]
    
    Stream -->|Receive raw response| ParseStream[Parse chunked wrb.fr]
    ParseStream --> CleanText[Remove markdown execution artifacts]
    
    CleanText --> IsStreaming{Streaming Requested?}
    
    IsStreaming -->|Yes| SSE[Format as SSE chunks]
    SSE --> Client
    
    IsStreaming -->|No| WaitFull[Accumulate Full Text]
    WaitFull --> CheckTools{Tools Called?}
    CheckTools -->|Yes| ParseTools[tools.py: parse_tool_calls]
    ParseTools --> FormatJSON[Format OpenAI JSON]
    CheckTools -->|No| FormatJSON
    FormatJSON --> Client
```

### Data Transformations

1. **Input Format (OpenAI)**: 
   ```json
   {
     "model": "gemini-3.5-flash-thinking",
     "messages": [{"role": "user", "content": "Hello"}],
     "stream": true
   }
   ```
2. **Intermediate Format (`tools.py`)**: 
   The OpenAI messages array is flattened into a single prompt string, using text markers like `[System instruction]: ...` and `[Assistant]: ...` to simulate conversation history.
3. **Payload Format (`gemini.py`)**: 
   The prompt string is placed into a highly specific array index: `inner[0] = [prompt, 0, None, refs, None, None, 0]`.
4. **Google Stream Format**: 
   Google returns a format starting with `wrb.fr` containing heavily escaped JSON strings. The client parses this using regular expressions and JSON decoding to extract text deltas.
5. **Output Format (OpenAI SSE)**:
   ```text
   data: {"id": "chatcmpl-...", "object": "chat.completion.chunk", "choices": [{"delta": {"content": "Hello"}}]}
   ```

## 2. Image Processing Flow (`multimodal.py`)

When an image is provided in the OpenAI request (either via URL or base64):

1. **Extract**: The image is extracted and base64 is decoded to raw bytes. HTTP URLs are fetched locally by the server.
2. **Token Fetch**: The server makes a background GET request to `https://gemini.google.com/app` to retrieve temporary session tokens (`push_id`, `pctx`).
3. **Start Upload**: Sends a POST request to `https://content-push.googleapis.com/upload/` with the `X-Goog-Upload-Protocol: resumable` header.
4. **Execute Upload**: Receives an upload URL, then POSTs the raw image bytes to that URL.
5. **Reference**: Receives a file reference path from Google, which is then inserted into the `refs` array of the main Gemini request payload.
