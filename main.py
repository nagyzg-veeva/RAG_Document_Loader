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
            
            if result.file_paths:

                file_names = result.display_names
                file_paths = result.file_paths
                last_updates = result.metadata.get('last_updates', [])

                if isinstance(file_names, str):
                    file_names = [file_names]
                if isinstance(file_paths, str):
                    file_paths = [file_paths]

                corpus_results = upload_file(file_names, file_paths)
                logger.info(f'The files {file_names} have been uploaded to the corpus. ids: {corpus_results}')

                for i, file_name in enumerate(file_names):
                    if i < len(last_updates):
                        file_version_tracker.set_last_version(file_name, last_updates[i])
                    
                    # deleting the temp file
                    if i < len(file_paths):
                        path = Path(file_paths[i])
                        path.unlink(missing_ok=True)


        except Exception as e:
            print(f"Error: {e}")

    
if __name__ == "__main__":
    
    main()