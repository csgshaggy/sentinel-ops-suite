import importlib
import pkgutil
from pathlib import Path

PLUGIN_DIR = Path(__file__).parent
PLUGIN_NAMESPACE = __name__

def discover_plugins():
    plugins = {}

    for module_info in pkgutil.iter_modules([str(PLUGIN_DIR)]):
        name = module_info.name

        # Skip private or non-plugin modules
        if name.startswith("_"):
            continue

        module_path = f"{PLUGIN_NAMESPACE}.{name}"
        module = importlib.import_module(module_path)

        # Look for a Plugin class
        plugin_class = getattr(module, "Plugin", None)
        if plugin_class is None:
            continue

        try:
            instance = plugin_class()
            plugins[name] = instance
        except Exception as e:
            print(f"[plugin] Failed to load {name}: {e}")

    return plugins

# Auto-discover on import
PLUGINS = discover_plugins()
