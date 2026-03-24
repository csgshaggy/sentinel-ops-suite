import os
import importlib

PLUGIN_DIR = os.path.dirname(__file__)


def load_plugins():
    plugins = {}
    for file in os.listdir(PLUGIN_DIR):
        if file.endswith(".py") and file not in ("__init__.py"):
            name = file[:-3]
            module = importlib.import_module(f"plugins.{name}")
            plugins[name] = module
    return plugins
