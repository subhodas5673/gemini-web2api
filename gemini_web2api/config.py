"""Configuration management."""
import json
import os

DEFAULT_CONFIG = {
    "port": 8081,
    "host": "0.0.0.0",
    "retry_attempts": 3,
    "retry_delay_sec": 2,
    "request_timeout_sec": 180,
    "gemini_bl": "boq_assistant-bard-web-server_20260716.08_p0",
    "auth_user": None,
    "xsrf_token": None,
    "default_model": "gemini-3.6-flash",
    "log_requests": True,
    "cookie_file": None,
    "proxy": None,
    "api_keys": [],
    "temporary_chats": False,
}

CONFIG = dict(DEFAULT_CONFIG)


def load_config(path: str = None):
    """Load config from JSON file."""
    if path and os.path.exists(path):
        with open(path) as f:
            CONFIG.update(json.load(f))
    return CONFIG


def load_env_config():
    """Load config from environment variables."""
    env_mapping = {
        "PORT": ("port", int),
        "HOST": ("host", str),
        "RETRY_ATTEMPTS": ("retry_attempts", int),
        "RETRY_DELAY_SEC": ("retry_delay_sec", int),
        "REQUEST_TIMEOUT_SEC": ("request_timeout_sec", int),
        "GEMINI_BL": ("gemini_bl", str),
        "AUTH_USER": ("auth_user", str),
        "XSRF_TOKEN": ("xsrf_token", str),
        "DEFAULT_MODEL": ("default_model", str),
        "LOG_REQUESTS": ("log_requests", lambda x: str(x).lower() in ("true", "1", "yes", "on")),
        "COOKIE_FILE": ("cookie_file", str),
        "PROXY": ("proxy", str),
        "API_KEYS": ("api_keys", lambda x: json.loads(x) if x.strip().startswith("[") else [k.strip() for k in x.split(",") if k.strip()]),
        "TEMPORARY_CHATS": ("temporary_chats", lambda x: str(x).lower() in ("true", "1", "yes", "on")),
    }
    
    for env_key, (config_key, type_func) in env_mapping.items():
        if env_key in os.environ:
            try:
                CONFIG[config_key] = type_func(os.environ[env_key])
            except Exception as e:
                import sys
                sys.stderr.write(f"Warning: Failed to parse env var {env_key}: {e}\n")
    return CONFIG


def find_config():
    """Search for config file in standard locations."""
    for p in ["./config.json", os.path.expanduser("~/.config/gemini-web2api/config.json")]:
        if os.path.exists(p):
            return p
    return None
