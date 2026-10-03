# Contributing Guidelines

While this repository does not define a strict contribution policy, the following patterns are inferred from the codebase and should be followed by contributors.

## Code Style
- **Python**: The project uses standard Python conventions (PEP 8). It does not use type hints exhaustively but applies them to function signatures. 
- **Dependencies**: Keep the core dependency footprint as small as possible. The primary Python codebase relies only on the standard library, with `httpx` being the sole optional exception. Do not introduce new heavy dependencies (e.g., `requests`, `fastapi`, `flask`) unless absolutely necessary.
- **Single File Compatibility**: Changes to the core logic in `gemini_web2api/` should ideally be synchronized with the monolithic `gemini_web2api.py` script. The project promises a "single file" deployment option.

## Testing
- Tests are located in the `tests/` directory (e.g., `test_modular_sync.py`).
- Use the standard `unittest` framework.
- **Execution**: Run tests using `python -m unittest tests/test_modular_sync.py`.
- **Warning**: These are integration tests that make live network calls to Google Gemini. They require network access and may require valid configuration variables to pass.

## Pull Requests
- Ensure modifications don't break the exact OpenAI JSON response schemas.
- Ensure streaming functionality (SSE) is tested manually using an OpenAI-compatible client.
- When fixing Google protocol issues (e.g., changes to the `StreamGenerate` array structure), clearly document the evidence from the Gemini Web UI network logs in your PR description.
