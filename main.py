import logging
from pathlib import Path
from plugin_loader import PluginLoader
from plugins.document_loader_plugin import DocumentLoaderPlugin
from file_version_tracker import FileVersionTracker
import config.config as config
from corpus_manager import upload_file

def main():

    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    file_version_tracker = FileVersionTracker(config=config)
    plugin_loader = PluginLoader(plugin_config=config.PLUGIN_CONFIG_PATH, file_version_tracker=file_version_tracker)
    plugins = plugin_loader.load_plugins()

    for plugin_name in plugins:
        try:
            plugin_context = plugins[plugin_name]
            plugin_instance:DocumentLoaderPlugin = plugin_context['plugin_instance']
            plugin_config = plugin_context['config']
            
            result = plugin_instance.run()
            logger.info(f"Plugin Result: {result}")

            if result.success == False:
                continue
            
            if result.file_path:

                file_name = result.display_name
                file_path = result.file_path

                corpus_result = upload_file(file_name, file_path)
                logger.info(f'The file {file_name} has been uploaded to the corpus. id: {corpus_result}')
                
                # deleting the temp file
                path = Path(file_path)
                path.unlink(missing_ok=True)


        except Exception as e:
            print(f"Error: {e}")

    
if __name__ == "__main__":
    
    main()