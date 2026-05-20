import importlib
import pkgutil

from .plugins.base import SSRFPlugin


def load_plugins():
    """
    Dynamically discover and load all SSRF plugins.
    Returns a dict: {plugin_name: plugin_instance}
    """
    plugins = {}
    package = "sentinel_ops_suite.plugins"

    for _, module_name, _ in pkgutil.iter_modules([__import__(package).__path__[0]]):
        module = importlib.import_module(f"{package}.{module_name}")

        for attr in dir(module):
            obj = getattr(module, attr)
            if (
                isinstance(obj, type)
                and issubclass(obj, SSRFPlugin)
                and obj is not SSRFPlugin
            ):
                instance = obj()
                plugins[instance.name] = instance

    return plugins
