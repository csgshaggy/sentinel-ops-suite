import importlib
import os
from typing import List, Optional

PLUGIN_DIR = "backend/plugins"


class Plugin:
    def __init__(self, id: str, module):
        self.id = id
        self.module = module

    def to_dict(self):
        return {
            "id": self.id,
            "name": getattr(self.module, "NAME", self.id),
            "category": getattr(self.module, "CATEGORY", "general"),
            "status": "ok",
            "avgDurationMs": getattr(self.module, "AVG_DURATION", 0),
            "lastRunAt": getattr(self.module, "LAST_RUN", None),
        }


def get_all_plugins() -> List[Plugin]:
    plugins = []
    for file in os.listdir(PLUGIN_DIR):
        if file.endswith(".py") and not file.startswith("_"):
            module_name = file[:-3]
            module = importlib.import_module(f"plugins.{module_name}")
            plugins.append(Plugin(module_name, module))
    return plugins


def get_plugin_by_id(plugin_id: str) -> Optional[Plugin]:
    for p in get_all_plugins():
        if p.id == plugin_id:
            return p
    return None


async def run_plugin(plugin: Plugin):
    if hasattr(plugin.module, "run"):
        return await plugin.module.run()
    return "Plugin has no run() function"
