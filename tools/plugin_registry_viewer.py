from __future__ import annotations

import json
from typing import Any, Dict, List

from tools import super_doctor as sd  # reuse discovery logic


def list_plugins(config: Dict[str, Any] | None = None) -> List[Dict[str, Any]]:
    """
    Return discovered plugin metadata without executing them.
    """
    config = config or {}
    # Reach into super_doctor's discovery functions
    plugins_meta = sd._discover_plugins(config)  # type: ignore[attr-defined]
    return [
        {
            "name": meta.get("name", meta["module"]),
            "module": meta["module"],
            "category": meta.get("category", "general"),
            "entrypoint": meta.get("entrypoint"),
        }
        for meta in plugins_meta
    ]


def main() -> None:
    plugins = list_plugins({})
    print(json.dumps({"plugins": plugins}, indent=2))


if __name__ == "__main__":
    main()
