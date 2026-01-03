import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Project root directory (where config.py resides)
PROJECT_ROOT = Path(__file__).parent.parent

# Plugin configuration file path (OS-agnostic)
PLUGIN_CONFIG_PATH = (PROJECT_ROOT / "config" / "plugin_config.yml").resolve()

# Document version tracking
DB_HOST = os.getenv("DB_HOST", "")
DB_USER = os.getenv("DB_USER", "")
DB_PASS = os.getenv("DB_PASS", "")
DB_NAME = os.getenv("DB_NAME", "")
DB_TABLE_NAME = "file_tracker"