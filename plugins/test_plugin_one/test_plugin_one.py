from plugins.document_loader_plugin_interface import DocumentLoaderPluginInterface

class TestPluginOne(DocumentLoaderPluginInterface):
    def __init__(self):
        print("TestPluginOne initialized")

    

    def load_document(self):
        return super().load_document()
    
    def transform_document(self):
        return super().transform_document()
    
    def download_document(self, document_config):
        return super().download_document(document_config)