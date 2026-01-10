from plugin_loader import PluginLoader
from plugins.document_loader_plugin import DocumentLoaderPlugin
from file_version_tracker import FileVersionTracker
import config.config as config

def main():
    file_version_tracker = FileVersionTracker(config=config)
    plugin_loader = PluginLoader(plugin_config=config.PLUGIN_CONFIG_PATH, file_version_tracker=file_version_tracker)
    plugins = plugin_loader.load_plugins()

    for plugin_name in plugins:
        try:
            plugin_context = plugins[plugin_name]
            plugin_instance:DocumentLoaderPlugin = plugin_context['plugin_instance']
            plugin_config = plugin_context['config']
            
            result = plugin_instance.run()

        except Exception as e:
            print(f"Error: {e}")

    
if __name__ == "__main__":
    
    main()