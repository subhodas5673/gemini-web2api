# Development Workflow

## Installation

The project is written in pure Python with minimal dependencies.

```bash
# Clone the repository
git clone https://github.com/user/gemini-web2api.git
cd gemini-web2api

# (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies (only httpx is required for streaming)
pip install -r requirements.txt
```

## Running the Server

You can run the server in two ways:

1. **Using the package module:**
   ```bash
   python -m gemini_web2api --config config.example.json
   ```
2. **Using the standalone script:**
   ```bash
   python gemini_web2api.py --config config.example.json
   ```

## Getting Cookies
For full functionality (like `gemini-3.1-pro` routing), you must supply a cookie from a Gemini Advanced account.
1. Install the provided Chrome extension in `gemini-cookie-sync-extension/` (Load unpacked).
2. Or manually extract `SAPISID` and other cookies from DevTools and create a `cookie.txt` file.

## Testing
The repository contains a `tests/` directory.

```bash
# Run tests
python -m unittest tests/test_modular_sync.py
```
> **Note**: These tests hit the live Gemini endpoints and require a valid configuration.

## Formatting & Linting
No explicit formatting (e.g. Black) or linting (e.g. Flake8) configuration is provided in the repository. Adhere to the existing code style (PEP 8 generally).

## Debugging
Enable verbose logging in `config.json`:
```json
{
  "log_requests": true
}
```
Watch the stdout/stderr for `[INFO]` and `[ERROR]` messages. The `gemini.py` module logs upstream errors and `BardErrorInfo` rejection codes.
