from __future__ import annotations

import os
import re
from typing import Dict, List, Tuple

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
MAKEFILE_PATH = os.path.join(ROOT_DIR, "Makefile")
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
DOC_PATH = os.path.join(DOCS_DIR, "MAKEFILE.md")

RE_TARGET = re.compile(r"^([A-Za-z0-9_.-]+):")
RE_ECHO = re.compile(r'echo\s+"(.+)"')


def _read_makefile() -> List[str]:
    with open(MAKEFILE_PATH, "r", encoding="utf-8") as f:
        return f.readlines()


def _extract_targets_with_comments(lines: List[str]) -> List[Tuple[str, str]]:
    """
    Extract targets and a short description if present in the help section.
    We look for lines in the help target that echo descriptions.
    """
    targets: List[str] = []
    descriptions: Dict[str, str] = {}

    # First pass: collect all targets
    for line in lines:
        m = RE_TARGET.match(line.strip())
        if m:
            targets.append(m.group(1))

    # Second pass: parse help echo lines
    in_help = False
    for line in lines:
        stripped = line.rstrip("\n")
        if stripped.startswith("help:"):
            in_help = True
            continue
        if in_help and stripped.startswith(".PHONY"):
            break
        if in_help and "echo" in stripped:
            m = RE_ECHO.search(stripped)
            if not m:
                continue
            text = m.group(1)
            # Expect lines like: "  make backend-run        — Run FastAPI backend"
            if "make " in text:
                try:
                    part = text.split("make ", 1)[1]
                    target = part.split()[0]
                    desc = text.split("—", 1)[1].strip() if "—" in text else ""
                    descriptions[target] = desc
                except Exception:
                    continue

    result: List[Tuple[str, str]] = []
    for t in targets:
        result.append((t, descriptions.get(t, "")))
    return result


def _render_markdown(entries: List[Tuple[str, str]]) -> str:
    lines = [
        "# Makefile index",
        "",
        "Auto‑generated from `Makefile`. Do not edit by hand.",
        "",
        "| Target | Description |",
        "|--------|-------------|",
    ]
    for target, desc in entries:
        lines.append(f"| `{target}` | {desc} |")
    lines.append("")
    return "\n".join(lines)


def generate_index() -> str:
    lines = _read_makefile()
    entries = _extract_targets_with_comments(lines)
    return _render_markdown(entries)


def main() -> None:
    os.makedirs(DOCS_DIR, exist_ok=True)
    content = generate_index()
    with open(DOC_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Wrote Makefile index to {DOC_PATH}")


if __name__ == "__main__":
    main()
