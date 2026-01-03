from plugin_loader import PluginLoader
from plugins.document_loader_plugin_interface import DocumentLoaderPluginInterface
from file_version_tracker import FileVersionTracker
import config.config as config

def main():
    file_version_tracker = FileVersionTracker(config=config)
    plugin_loader = PluginLoader(plugin_config=config.PLUGIN_CONFIG_PATH, file_version_tracker=file_version_tracker)
    plugins = plugin_loader.load_plugins()

    for plugin_name in plugins:
        try:
            plugin_context = plugins[plugin_name]
            plugin_instance:DocumentLoaderPluginInterface = plugin_context['plugin_instance']
            plugin_config = plugin_context['config']

            download_document_result = plugin_instance.download_document()
            transform_document_result = plugin_instance.transform_document()
            load_document_result = plugin_instance.load_document()

        except Exception as e:
            print(f"Error: {e}")

    
if __name__ == "__main__":
    
    main()