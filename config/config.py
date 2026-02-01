import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Project root directory (where config.py resides)
PROJECT_ROOT = Path(__file__).parent.parent

# Plugin configuration file path (OS-agnostic)
PLUGIN_CONFIG_PATH = (PROJECT_ROOT / "config" / "plugin_config.yml").resolve()


def get_required_env(key: str) -> str:
    """Get required environment variable or raise error"""
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Required environment variable {key} is not set")
    return value


def get_env_with_default(key: str, default: str) -> str:
    """Get env variable with default"""
    return os.getenv(key, default)


# Document version tracking
DB_HOST = get_required_env("DB_HOST")
DB_USER = get_required_env("DB_USER")
DB_PASS = get_required_env("DB_PASS")
DB_NAME = get_required_env("DB_NAME")
DB_TABLE_NAME = get_env_with_default("DB_TABLE_NAME", "file_tracker")


# Corpus settings
PROJECT_ID = get_required_env("GCP_PROJECT_ID")
LOCATION = get_required_env("GCP_LOCATION")
CORPUS_NAME = get_required_env("GCP_CORPUS_NAME")

# Validate corpus name format
if not CORPUS_NAME.startswith("projects/"):
    raise ValueError(f"Invalid CORPUS_NAME format: {CORPUS_NAME}")

print("✅ Configuration validated successfully")
