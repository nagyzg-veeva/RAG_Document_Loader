import logging
import datetime
from typing import Dict, Any
from plugins.document_loader_plugin_interface import DocumentLoaderPluginInterface

class TestPluginOne(DocumentLoaderPluginInterface):

    def __init__(self, plugin_config:Dict[str, Any], file_version_tracker:Any):
        super().__init__(plugin_config, file_version_tracker)

    def load_document(self):
        print("TestPluginOne.load_document() called")
    
        now = datetime.datetime.now(datetime.timezone.utc)

        new_version_vavailable = self.file_version_tracker.is_new_version_available("VCRM Migration - Tracker", now)
        if new_version_vavailable:
            print("NEW VERSION AVAILABLE")

    
    def transform_document(self):
        print("TestPluginOne.transform_document() called")
        return super().transform_document()
    
    def download_document(self):
        print("TestPluginOne.download_document() called")
        return super().download_document()