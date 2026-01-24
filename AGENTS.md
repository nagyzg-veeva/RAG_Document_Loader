# AGENTS.md - RAG Document Loader

This document provides guidelines for agentic coding assistants working in this repository.

## Project Overview

RAG Document Loader is a Python application for loading documents into Google Cloud Vertex AI RAG corpora. It features a plugin architecture for document processing and version tracking.

## Build & Development Commands

### Environment Setup
```bash
# Create virtual environment (if not exists)
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies using uv (preferred) or pip
uv sync  # Uses uv.lock
# OR
pip install -e .
```

### Running the Application
```bash
# Run main application
python main.py

# Run specific test
python test_corpus_manager.py
python test.py

# Run all tests with unittest
python -m unittest discover -v
```

### Testing Commands
```bash
# Run single test file
python test_corpus_manager.py

# Run specific test class
python -m unittest test_corpus_manager.TestCorpusManager

# Run specific test method
python -m unittest test_corpus_manager.TestCorpusManager.test_upload_file_existing

# Run all tests
python -m unittest discover
```

### Linting & Formatting
```bash
# Check code with ruff
ruff check .

# Format code with ruff
ruff format .

# Check types (if mypy is configured)
mypy .
```

## Code Style Guidelines

### Imports
- Use absolute imports within the project
- Group imports: standard library, third-party, local modules
- Import order: `import` statements first, then `from ... import`
- Use explicit imports for clarity

```python
# Standard library
import logging
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass

# Third-party
import gspread
import pandas as pd
from vertexai import rag

# Local modules
from config.config import PROJECT_ID, CORPUS_NAME
from plugins.document_loader_plugin import DocumentLoaderPlugin
```

### Naming Conventions
- **Classes**: `PascalCase` (e.g., `PluginLoader`, `DocumentLoaderPlugin`)
- **Functions/Methods**: `snake_case` (e.g., `upload_file`, `load_plugins`)
- **Variables**: `snake_case` (e.g., `file_version_tracker`, `plugin_config`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `PROJECT_ID`, `DB_TABLE_NAME`)
- **Private methods**: `_snake_case` with leading underscore (e.g., `_load_plugin`)

### Type Annotations
- Use type hints for all function parameters and return values
- Import typing modules as needed (`Dict`, `List`, `Optional`, `Any`, etc.)
- Use `dataclass` for data containers

```python
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class PluginResult:
    success: bool
    display_name: str
    content: Optional[str] = None
    file_path: Optional[Path] = None
    metadata: Optional[dict] = None

def upload_file(file_name: str, local_path: str) -> None:
    """Uploads a file to the Google Cloud Vertex AI RAG Corpus."""
```

### Error Handling
- Use try/except blocks for operations that can fail
- Log errors with appropriate levels (`logger.error`, `logger.warning`)
- Re-raise exceptions after logging when appropriate
- Use specific exception types when possible

```python
try:
    # Operation that might fail
    result = plugin_instance.run()
except FileNotFoundError as e:
    logger.error(f"Configuration file not found: {e}")
    raise
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise
```

### Logging
- Configure logging at module level: `logging.basicConfig(level=logging.INFO)`
- Get logger instance: `logger = logging.getLogger(__name__)`
- Use appropriate log levels:
  - `logger.debug`: Detailed debugging information
  - `logger.info`: General information about program execution
  - `logger.warning`: Warning messages
  - `logger.error`: Error messages for recoverable errors
  - `logger.critical`: Critical errors that may cause program termination

### File Paths
- Use `pathlib.Path` for file operations (OS-agnostic)
- Resolve paths relative to project root or module location
- Use `Path(__file__).parent` to get module directory

```python
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Plugin configuration file path
PLUGIN_CONFIG_PATH = (PROJECT_ROOT / "config" / "plugin_config.yml").resolve()
```

### Plugin Architecture
- All plugins must inherit from `DocumentLoaderPlugin`
- Plugins must implement `run()` method returning `PluginResult`
- Use `PluginResult` dataclass for standardized return values
- Plugins should use `create_result()` factory method

```python
class MyPlugin(DocumentLoaderPlugin):
    def run(self) -> PluginResult:
        try:
            # Plugin logic
            return self.create_result(
                success=True,
                display_name="My Document",
                file_path=temp_file_path
            )
        except Exception as e:
            return self.create_result(
                success=False,
                display_name="My Document",
                error_message=str(e)
            )
```

### Configuration Management
- Store configuration in `config/config.py`
- Use environment variables via `dotenv` for secrets
- Keep sensitive data out of version control (use `.env` file)
- Plugin configurations in YAML files (`config/plugin_config.yml`)

### Testing Guidelines
- Use `unittest` framework for tests
- Mock external dependencies (Google Cloud, databases, etc.)
- Test both success and failure cases
- Follow naming convention: `test_<method_name>_<scenario>`

```python
import unittest
from unittest.mock import MagicMock, patch

class TestCorpusManager(unittest.TestCase):
    @patch('corpus_manager.vertexai')
    @patch('corpus_manager.rag')
    def test_upload_file_existing(self, mock_rag, mock_vertexai):
        # Setup mocks
        # Execute function
        # Verify behavior
```

## Project Structure
```
RAG_Document_Loader/
├── config/
│   ├── config.py          # Main configuration
│   └── plugin_config.yml  # Plugin configurations
├── plugins/
│   ├── document_loader_plugin.py  # Base plugin class
│   └── migration_tracker/         # Example plugin
├── utils/
│   └── csv_transformer.py
├── main.py                # Entry point
├── corpus_manager.py      # RAG corpus operations
├── plugin_loader.py       # Plugin loading system
├── file_version_tracker.py # Version tracking
├── test_corpus_manager.py # Tests
└── pyproject.toml         # Dependencies
```

## Git Guidelines
- Commit messages should be descriptive and concise
- Use `.gitignore` to exclude virtual environments, IDE files, and secrets
- Never commit `.env` files or credentials
- Keep `uv.lock` file in sync with dependencies

## Security Notes
- Never hardcode credentials in source code
- Use environment variables for sensitive data
- Google Cloud credentials should be stored outside the repository
- Database credentials should be loaded from environment variables

## Common Patterns

### Temporary File Management
```python
import tempfile
from pathlib import Path

# Create temporary file
with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as tmp:
    tmp.write(content)
    tmp_path = tmp.name

# Clean up temporary file
path = Path(tmp_path)
path.unlink(missing_ok=True)
```

### Plugin Loading Pattern
```python
# Dynamic import
module = importlib.import_module(config.path)
plugin_cls = getattr(module, config.classname)
instance = plugin_cls()
```

### Version Tracking
```python
# Check if new version available
if self.should_process(filename, current_version):
    # Process file
    self.update_version_tracker(filename, current_version)
```

## Troubleshooting
- Ensure `.env` file exists with required environment variables
- Verify Google Cloud credentials are properly configured
- Check database connection settings in config
- Activate virtual environment before running commands