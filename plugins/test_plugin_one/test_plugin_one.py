from plugins.document_loader_plugin_interface import DocumentLoaderPluginInterface

class TestPluginOne(DocumentLoaderPluginInterface):
    def __init__(self):
        print("TestPluginOne initialized")

    def run(self):
        print("TestPluginOne running")