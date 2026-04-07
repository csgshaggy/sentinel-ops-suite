"""
IDRIM CLI
---------
Command‑line interface for running IDRIM analyses.

This wrapper is intentionally:
- Minimal
- Deterministic
- Operator‑grade
- Free of business logic (delegates to IDRIMService)
"""

from __future__ import annotations

import argparse
import json
import logging
import sys

from .idrim_service import IDRIMService
from .idrim_models import IDRIMRequest
from .idrim_exceptions import IDRIMError

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="idrim",
        description="IDRIM command‑line analysis tool",
    )

    parser.add_argument(
        "target",
        help="File or directory to analyze",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output result as JSON",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    service = IDRIMService()

    request = IDRIMRequest(target_path=args.target)

    try:
        result = service.run(request)
    except IDRIMError as exc:
        logger.error("IDRIM error: %s", exc)
        return 1
    except Exception as exc:
        logger.exception("Unexpected failure")
        return 1

    if args.json:
        print(json.dumps(result.__dict__, indent=2))
    else:
        print(f"Target:      {result.target}")
        print(f"Files:       {result.file_count}")
        print(f"Directories: {result.dir_count}")
        print(f"Score:       {result.score}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
