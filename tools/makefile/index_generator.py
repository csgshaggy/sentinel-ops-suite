from __future__ import annotations

from pathlib import Path

CANONICAL = Path(__file__).parent / "Makefile.canonical"
OUTPUT = Path(__file__).parents[2] / "docs" / "MAKEFILE.md"


def generate_index() -> None:
    OUTPUT.parent.mkdir(exist_ok=True)

    content = CANONICAL.read_text()

    OUTPUT.write_text(
        "# Canonical Makefile Index\n\n"
        "This file is auto-generated.\n\n"
        "```\n" + content + "\n```"
    )
