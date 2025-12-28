from abc import ABC, abstractmethod

class DocumentLoaderPluginInterface(ABC):

    def __init__(self, document_config:dict):
        pass

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
    def download_document(self, document_config:dict) -> str:
        pass


    @abstractmethod
    def transform_document(self) -> str:
        pass


    def load_document(self) -> str:
        pass




    

    