import gspread
import google.auth
import pprint
import os
import pandas as pd
from pathlib import Path

from plugins.document_loader_plugin import DocumentLoaderPlugin
from file_version_tracker import FileVersionTracker

SHEET_ID="1NJLdhSol4tqnIdeMg9uGSjC98h3V_sFGcAkAbJUBpp4"
WORKSHEET_ID="1406128683"
TRACKED_FILENAME = 'VCRM Migration - Tracker'
OUTPUT_FILEPATH = 'VCRM Migration - Tracker.md'
PLUGIN_PATH = Path(__file__).parent
CREDNTIALS = str((PLUGIN_PATH / "oca-agentic-rag-mig-helper-21954a69ee21.json").resolve())
if Path(CREDNTIALS).exists():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=CREDNTIALS

HEADER_MAP = header_map = {
        0: "Item ID",
        1: "Issue Description",
        2: "Raised By",
        3: "Status",
        4: "Parent Issue",
        5: "Priority",
        6: "Area",
        7: "Type",
        8: "Topic",
        9: "Context/Notes",
        10: "Log URL",
        11: "Impact/Workaround",
        12: "Customer/Org", # This column varies (Orgs/Customers) but position is usually 12
        13: "Response",
        14: "Jira ID",
        15: "Target Release",
        16: "Release Date",
        # Skipping indexes 17-29 (Stack flags) to reduce noise, unless critical
        17: "EA Critical Issue", 
        18: "G17 Critical Issue",
        30: "Critical Issue",
        31: "Date Created",
        32: "Date Closed",
        33: "Days Open",
        34: "Reference Link"
    }

META_FIELDS = [5, 3, 6, 7, 8] 


class MigrationTracker(DocumentLoaderPlugin):

    def __init__(self):
        self.client:gspread.Client = None
        self.sheet = None
        self.data = None
        super().__init__()


    def get_gsheet_client(self) -> None:

        try:
            credentials, project = google.auth.default(
                scopes=[
                    "https://www.googleapis.com/auth/spreadsheets",
                    "https://www.googleapis.com/auth/drive"
                ]
            )
        
            if not credentials:
                raise ValueError('No Google credentials found')

            self.logger.info(f"Using credentials for project: {project}")
            self.logger.info(f"Using credentials: {credentials}")
            client = gspread.authorize(credentials)
            self.client = client

        except Exception as e:
            self.logger.error(f"Failed to get Google credentials {type(e).__name__}: {e}")
            raise

    
    def get_sheet(self) -> None:

        try: 
            sheet = self.client.open_by_key(SHEET_ID)
            self.sheet = sheet
        except gspread.exceptions.SpreadsheetNotFound as e:
            self.logger.error(f"Spreadsheet can not be found or no permission: {e}")
            raise
        except gspread.exceptions.APIError as e:
            self.logger.error(f"Google Sheets API error: {e}")
            raise

    
    def convert_content(self) -> str:

        formatted_docs = []

        # Iterate through the DataFrame
        for _, row in self.data.iterrows():
            # Clean the Item ID to ensure it's a valid row
            item_id_raw = row.iloc[0] if not pd.isna(row.iloc[0]) else ""
            item_id = str(item_id_raw).strip()

            # Skip rows that don't look like valid items (e.g., empty or repeat headers)
            if not item_id or not item_id.lower().startswith(("item", "a-item", "legacy")):
                continue

            doc_lines = []

            # --- A. Title Block ---
            doc_lines.append(f"Item ID: {item_id}")

            # Get Description (Index 1)
            desc_raw = row.iloc[1] if not pd.isna(row.iloc[1]) else ""
            description = str(desc_raw).strip().replace("\n", " ")
            if description:
                doc_lines.append(f"Issue Description: {description}")

            # --- B. Metadata Line ---
            meta_parts = []
            for idx in META_FIELDS:
                if idx < len(row): # Safety check for bounds
                    val = row.iloc[idx]
                    if not pd.isna(val) and str(val).strip():
                        label = HEADER_MAP.get(idx, "Meta")
                        clean_val = str(val).strip()
                        meta_parts.append(f"{label}: {clean_val}")

            if meta_parts:
                doc_lines.append(" | ".join(meta_parts))

            # --- C. Body Content ---
            for idx, label in HEADER_MAP.items():
                # Skip fields already handled in Title or Metadata sections
                if idx in [0, 1] or idx in META_FIELDS:
                    continue
                
                if idx < len(row):
                    val = row.iloc[idx]

                    # Check for empty/NaN values
                    if pd.isna(val):
                        continue
                    
                    clean_val = str(val).strip()
                    if not clean_val or clean_val.lower() == "nan":
                        continue

                    doc_lines.append(f"{label}: {clean_val}")

            # Join the lines for this specific item
            formatted_docs.append("\n".join(doc_lines))

        # Join all items with a separator
        return "\n" + ("\n" + "-" * 40 + "\n").join(formatted_docs)

    


    def run(self) -> PluginResult:
        self.logger.info(f"{__name__} plugin's run() method called")

        try:
            self.get_gsheet_client()
            self.get_sheet()          

        except Exception as e:
            self.logger.error(f"Error {type(e).__name__}: {e} ")
            raise
        
        sheet_last_update_time = self.sheet.get_lastUpdateTime()
        self.logger.info(f"sheet last update date: {sheet_last_update_time}")
        
        new_version_available = self.file_version_tracker.is_new_version_available(TRACKED_FILENAME, sheet_last_update_time)
        self.logger.info(f"New version available: {new_version_available}")

        if new_version_available:
            worksheet = self.sheet.get_worksheet_by_id(WORKSHEET_ID)
            worksheet_data = worksheet.get_all_values()
            self.data = pd.DataFrame(worksheet_data)
            content = self.convert_content()

            if content:
                tmp_file_path = super().create_tmp_file_from_content(content=content, extension="txt")
                self.logger.info(f"Temp File Path: {tmp_file_path}")

            
