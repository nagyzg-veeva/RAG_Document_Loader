import gspread
import google.auth
import pprint
import os
import pandas as pd
from pathlib import Path
from typing import Optional

from plugins.document_loader_plugin import DocumentLoaderPlugin
from file_version_tracker import FileVersionTracker

SHEET_ID = "1NJLdhSol4tqnIdeMg9uGSjC98h3V_sFGcAkAbJUBpp4"
WORKSHEET_ID = "1406128683"
TRACKED_FILENAME = "VCRM Migration - Tracker"
OUTPUT_FILEPATH = "VCRM Migration - Tracker.md"
PLUGIN_PATH = Path(__file__).parent
CREDNTIALS = str(
    (PLUGIN_PATH / "oca-agentic-rag-mig-helper-bd0382bcb4b0.json").resolve()
)

if Path(CREDNTIALS).exists():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDNTIALS

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
    12: "Customer/Org",  # This column varies (Orgs/Customers) but position is usually 12
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
    34: "Reference Link",
}

META_FIELDS = [5, 3, 6, 7, 8]


class MigrationTracker(DocumentLoaderPlugin):
    def __init__(self):
        super().__init__()
        self.client: Optional[gspread.Client] = None
        self.sheet = None
        self.data = None

    def get_gsheet_client(self) -> None:
        try:
            scopes = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive",
            ]

            credentials, project = google.auth.default(scopes=scopes)

            if not credentials:
                raise ValueError("No Google credentials found")

            self.logger.info(f"Using credentials for project: {project}")
            # Authorize with gspread
            self.client = gspread.authorize(credentials)  # type: ignore

        except Exception as e:
            self.logger.error(
                f"Failed to get Google credentials {type(e).__name__}: {e}"
            )
            raise

    def get_sheet(self) -> None:
        if not self.client:
            raise ValueError("Google Sheets client not initialized")

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
        if self.data is None:
            return ""

        formatted_docs = []

        # Iterate through the DataFrame
        for _, row in self.data.iterrows():
            # Clean the Item ID to ensure it's a valid row
            item_id_raw = row.iloc[0] if not pd.isna(row.iloc[0]) else ""
            item_id = str(item_id_raw).strip()

            # Skip rows that don't look like valid items (e.g., empty or repeat headers)
            if not item_id or not item_id.lower().startswith(
                ("item", "a-item", "legacy")
            ):
                continue

            doc_lines = []

            # --- A. Header Section ---
            doc_lines.append(f"## {item_id}")
            doc_lines.append("")

            # Get Description (Index 1)
            desc_raw = row.iloc[1] if not pd.isna(row.iloc[1]) else ""
            description = str(desc_raw).strip().replace("\n", " ")
            if description:
                doc_lines.append(f"**Issue Description:** {description}")
                doc_lines.append("")

            # --- B. Quick Status Section ---
            doc_lines.append("### Status")
            status_info = []
            for idx in META_FIELDS:
                if idx < len(row):
                    val = row.iloc[idx]
                    if not pd.isna(val) and str(val).strip():
                        label = HEADER_MAP.get(idx, "Meta")
                        clean_val = str(val).strip()
                        status_info.append(f"- **{label}:** {clean_val}")

            if status_info:
                doc_lines.extend(status_info)
            doc_lines.append("")

            # --- C. Detailed Information Section ---
            detailed_info = []
            for idx, label in HEADER_MAP.items():
                # Skip fields already handled in Header or Status sections
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

                    # Format URLs as clickable links
                    if (
                        "URL" in label
                        or "Link" in label
                        and clean_val.startswith(("http://", "https://"))
                    ):
                        detailed_info.append(
                            f"- **{label}:** [{clean_val}]({clean_val})"
                        )
                    else:
                        detailed_info.append(f"- **{label}:** {clean_val}")

            if detailed_info:
                doc_lines.append("### Details")
                doc_lines.extend(detailed_info)
                doc_lines.append("")

            # --- D. Context Section (for longer notes) ---
            notes_idx = 9  # Context/Notes column
            if notes_idx < len(row):
                notes_raw = row.iloc[notes_idx]
                if not pd.isna(notes_raw) and str(notes_raw).strip():
                    notes = str(notes_raw).strip()
                    if notes and notes.lower() != "nan":
                        doc_lines.append("### Context")
                        doc_lines.append("")
                        # Preserve line breaks in notes
                        notes_lines = notes.split("\n")
                        for note_line in notes_lines:
                            if note_line.strip():
                                doc_lines.append(f"> {note_line.strip()}")
                        doc_lines.append("")

            # Join the lines for this specific item
            formatted_docs.append("\n".join(doc_lines))

        # Join all items with a clear separator
        return "\n" + ("\n" + "---" + "\n").join(formatted_docs)

    def run(self) -> "PluginResult":
        from plugins.document_loader_plugin import (
            PluginResult,
        )  # Import here to avoid circular import

        self.logger.info(f"{__name__} plugin's run() method called")

        try:
            self.get_gsheet_client()
            self.get_sheet()

            if not self.sheet:
                return self.create_result(
                    success=False, error_message="Sheet not loaded"
                )

            sheet_last_update_time = self.sheet.get_lastUpdateTime()
            self.logger.info(f"sheet last update date: {sheet_last_update_time}")

            if self.should_process(TRACKED_FILENAME, sheet_last_update_time):
                self.logger.info("New version available, processing...")
                worksheet = self.sheet.get_worksheet_by_id(WORKSHEET_ID)
                worksheet_data = worksheet.get_all_values()
                self.data = pd.DataFrame(worksheet_data)
                content = self.convert_content()

                if content:
                    tmp_file_path = super().create_tmp_file_from_content(
                        content=content, extension=".md"
                    )
                    self.logger.info(f"Temp File Path: {tmp_file_path}")
                    # Update version tracker
                    # self.update_version_tracker(TRACKED_FILENAME, sheet_last_update_time)
                    return self.create_result(
                        success=True,
                        file_path=Path(tmp_file_path),
                        display_name=OUTPUT_FILEPATH,
                        metadata={
                            "source": "gsheet",
                            "last_update": sheet_last_update_time,
                        },
                    )
                else:
                    return self.create_result(
                        success=False, error_message="No content generated"
                    )
            else:
                self.logger.info("No new version, skipping")
                return self.create_result(
                    success=True,
                    display_name=OUTPUT_FILEPATH,
                    requires_version_update=False,
                    metadata={"skipped": True},
                )

        except Exception as e:
            self.logger.error(f"Error {type(e).__name__}: {e}")
            return self.create_result(
                success=False, display_name=OUTPUT_FILEPATH, error_message=str(e)
            )
