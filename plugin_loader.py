import importlib
import yaml
import pprint
import logging

from typing import Dict, Any, List
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PluginConfig:
    """ Data class for the pllugin configuration instances"""
    name: str
    path: str
    classname: str
    enabled: bool
    config: Dict[str, Any]


class PluginLoader:

    def __init__(self, plugin_config:str, file_version_tracker:Any):
        self.plugin_config_path = plugin_config
        self.file_version_tracker = file_version_tracker

        self.plugin_configs: List[PluginConfig] = []
        self.loaded_plugins: Dict[str, Any] = {}

        logger.info("Plugin Loader initialized")



    def load_config(self):

        try:
            with open(self.plugin_config_path, 'r') as config_file:
                config_data = yaml.safe_load(config_file)
                #logger.info(pprint.pp(config_data))

            self.plugin_configs = [
                PluginConfig(
                    name=plugin.get('name', ''),
                    path=plugin.get('path', ''),
                    classname=plugin.get('classname',''),
                    enabled=plugin.get('enabled', True),
                    config=plugin.get('config', {})    
                )
                for plugin in config_data.get('plugins', [])
            ]
            logger.info(f"Loaded configuration for {len(self.plugin_configs)} plugins")
            logger.info(self.plugin_configs)
        except FileNotFoundError:
            logger.error(f"Configuration file can not be fould: {self.config_path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"YAML parsing error: {e}")
            raise

    
    def _load_plugin(self, config:PluginConfig) -> Any:

        try:
            
            logger.info(f"Loading plugin module {config.name} ({config.classname})")

            module = importlib.import_module(config.path)
            if not hasattr(module, config.classname):
                raise AttributeError(f"Class {config.classname} not found in module {config.path}")

            plugin_cls = getattr(module, config.classname)
            instance = plugin_cls(config.config, self.file_version_tracker)

            return instance


        except Exception as e:
            logger.error(f"Failed to load module {config.name}: {e}")
            return None

    
    def load_plugins(self) -> Dict[str, Any]:

        self.load_config()

        for config in self.plugin_configs:
            if not config.enabled:
                logger.info(f"Skipping diabled plugin: {config.name}")
                continue

            plugin_instance = self._load_plugin(config)
            if plugin_instance is not None:
                self.loaded_plugins.update({
                    config.name : {
                        "plugin_instance":plugin_instance,
                        "config": config
                    }
                })
                logger.info(f"Succesfully loaded plugin module: {config.name}")
        
        return self.loaded_plugins
        
