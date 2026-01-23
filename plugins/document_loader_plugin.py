import logging
import psycopg2
import tempfile
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional
from pathlib import Path
import tempfile
import os

from file_version_tracker import FileVersionTracker

# Import the global config to access PLUGIN_CONFIG_PATH


@dataclass
class PluginResult:
    """Standardized return type for document loader plugins"""
    success: bool
    display_name: str
    content: Optional[str] = None
    file_path: Optional[Path] = None
    metadata: Optional[dict] = None
    error_message: Optional[str] = None
    requires_version_update: bool = True


class DocumentLoaderPlugin(ABC):

    def __init__(self):
        self.plugin_dir = Path(__file__).resolve().parent

    def set_file_version_tracker(self, file_version_tracker:FileVersionTracker) -> 'DocumentLoaderPlugin':
        self.file_version_tracker = file_version_tracker
        return self

    def set_logger(self, logger:logging) -> 'DocumentLoaderPlugin':
        self.logger = logger
        return self

    def download_vault_file(self, vault_file_config:str) -> str:
        """
        Downloads Vault file from the given vault.
        
        :param self:
        :param vault_file_config: Vault credentials and fiel uri
        :type vault_file_config: str
        :return: temp file path for the downloaded document
        :rtype: str
        """
        pass

    def download_gdrive_file(self, gdrive_file_config:str) -> str:
        """
        Downloads a gdrive file
        
        :param self: self
        :param gdrive_file_config: GDrive credentials and file uri
        :type gdrive_file_config: str
        :return: temp file path for the downloaded content
        :rtype: str
        """
        pass


    def download_gsheet_file(self, gsheet_file_config:str) -> str:
        """
        Downloads a gsheet file
        
        :param self: Description
        :param gsheet_file_config: Description
        :type gsheet_file_config: str
        :return: Description
        :rtype: str
        """
        pass


    def docling_conversion(self, input_document_path:str) -> str:
        """
        Converts the document found on the given temp file path, using docling
        
        :param self: self
        :param input_document_path: temp file path of the document to convert
        :type input_document_path: str
        :return: Markdown representation of the file.
        :rtype: str
        """
        pass

    def create_tmp_file_from_content(self, content:str, extension:str) -> str:
        """
        Creates a temporary file with the given content and extension.
        
        :param content: The content to write to the file
        :type content: str
        :param extension: File extension (e.g., '.txt', '.pdf'). If not starting with dot, one will be added.
        :type extension: str
        :return: Path to the created temporary file
        :rtype: str
        """

        # Ensure extension starts with a dot
        if not extension.startswith('.'):
            extension = '.' + extension
        
        # Create a temporary file with the given extension
        with tempfile.NamedTemporaryFile(mode='w', suffix=extension, delete=False, encoding='utf-8') as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        
        return tmp_path

    def create_result(self, success: bool, **kwargs) -> PluginResult:
        """Factory method for creating PluginResult instances"""
        return PluginResult(success=success, **kwargs)

    def update_version_tracker(self, filename: str, version: str):
        """Wrapper to update file version tracker"""
        self.file_version_tracker.set_last_version(filename, version)

    def should_process(self, filename: str, current_version: str) -> bool:
        """Check if new version is available"""
        return self.file_version_tracker.is_new_version_available(filename, current_version)


    @abstractmethod
    def run(self) -> PluginResult:
        pass



    

    