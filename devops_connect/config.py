"""
DevOps Connect — Configuration Loader
Handles multi-environment config with secret resolution.
"""
import os
import yaml
from pathlib import Path
from typing import Any

CONFIG_DIR = Path(__file__).parent.parent / "config"
ENV_FILE = Path(__file__).parent.parent / ".env.production"


def load_config(env: str = "staging") -> dict[str, Any]:
    """Load YAML config for the given environment."""
    config_path = CONFIG_DIR / f"{env}.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"Config not found: {config_path}")

    with open(config_path) as f:
        config = yaml.safe_load(f)

    config = _resolve_env_vars(config)

    if env == "production" and ENV_FILE.exists():
        config["secrets"] = _load_dotenv(ENV_FILE)

    return config


def _resolve_env_vars(config: dict) -> dict:
    """Replace ${VAR} placeholders with environment variables."""
    for key, value in config.items():
        if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
            var_name = value[2:-1]
            config[key] = os.environ.get(var_name, value)
        elif isinstance(value, dict):
            config[key] = _resolve_env_vars(value)
    return config


def _load_dotenv(path: Path) -> dict[str, str]:
    """Parse .env file into dict."""
    secrets = {}
    if path.exists():
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    secrets[key.strip()] = value.strip().strip('"').strip("'")
    return secrets
