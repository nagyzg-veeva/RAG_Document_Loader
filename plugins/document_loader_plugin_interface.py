import logging
import psycopg2
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any
from pathlib import Path

from file_version_tracker import FileVersionTracker

# Import the global config to access PLUGIN_CONFIG_PATH


class DocumentLoaderPluginInterface(ABC):

    def __init__(self, plugin_config:Dict[str, Any], file_version_tracker:FileVersionTracker, log_level:str=logging.ERROR):
        self.config = plugin_config or {}
        self.file_version_tracker = file_version_tracker

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

        

    @abstractmethod
    def download_document(self) -> str:
        pass


    @abstractmethod
    def transform_document(self) -> str:
        pass


    def load_document(self) -> str:
        pass




    

    