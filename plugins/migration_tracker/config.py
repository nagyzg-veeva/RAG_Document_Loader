from pathlib import Path

SHEET_URL="https://docs.google.com/spreadsheets/d/1NJLdhSol4tqnIdeMg9uGSjC98h3V_sFGcAkAbJUBpp4/edit?usp=sharing"
TRACKED_FILENAME = 'VCRM Migration - Tracker'
OUTPUT_FILEPATH = 'VCRM Migration - Tracker.md'


PLUGIN_PATH = Path(__file__).parent
CREDNTIALS = (PLUGIN_PATH / "oca-agentic-rag-mig-helper-21954a69ee21.json").resolve()
