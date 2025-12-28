import importlib
import yaml
import pprint


def load_config() -> dict:
    with open('plugin_config.yml', 'r') as plugin_config:
        config = yaml.safe_load(plugin_config)
        pprint.pp(config)




def main():

    config = load_config()

    for plugin_config in config['plugins']:

        path = plugin_config['path']
        classname = plugin_config['name']

        




if __name__ == "__main__":
    main()
