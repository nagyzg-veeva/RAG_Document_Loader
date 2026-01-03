from typing import Any, Dict

from plugins.document_loader_plugin_interface import DocumentLoaderPluginInterface

class TestPluginTwo(DocumentLoaderPluginInterface):
    def __init__(self, plugin_config:Dict[str, Any], file_version_tracker:Any):
        super().__init__(plugin_config, file_version_tracker)

    def load_document(self):
        print("TestPluginTwo.load_document() called")
        return super().load_document()
    
    def transform_document(self):
        print("TestPluginTwo.transform_document() called")
        return super().transform_document()
    
    def download_document(self):
        print("TestPluginTwo.download_document() called")
        return super().download_document()