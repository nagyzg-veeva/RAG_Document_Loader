from plugins.document_loader_plugin_interface import DocumentLoaderPluginInterface

class TestPluginTwo(DocumentLoaderPluginInterface):
    def __init__(self):
        print("TestPluginTwo initialized")

    def run(self) -> str:
        print("TestPluginTwo running")
        return "TestPluginTwo"  