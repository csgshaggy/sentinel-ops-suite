#!/usr/bin/env python3
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
TARGET_DIR = PROJECT_ROOT / "src"

BINARY_THRESHOLD = 0.20  # If >20% bytes are non-text, treat as binary


def is_binary(path: Path) -> bool:
    """Heuristic: detect binary files by scanning for non-text bytes."""
    try:
        raw = path.read_bytes()
    except Exception:
        return True

    if not raw:
        return False

    # Count non-printable bytes
    nontext = sum(1 for b in raw if b < 9 or (13 < b < 32) or b > 126)
    ratio = nontext / len(raw)

    return ratio > BINARY_THRESHOLD


def safe_read(path: Path):
    """Read file with fallback encodings."""
    try:
        return path.read_text(encoding="utf-8"), "utf-8"
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="latin-1"), "latin-1"
        except Exception:
            return None, None


def clean_binary_junk(text: str) -> str:
    """Remove invalid characters that break Python parsing."""
    # Remove control characters except newline/tab
    cleaned = re.sub(r"[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]", "", text)
    return cleaned


def normalize_to_utf8(path: Path):
    """Normalize file encoding to UTF-8."""
    text, encoding = safe_read(path)

    if text is None:
        print(f"[SKIP] Could not read file: {path}")
        return

    cleaned = clean_binary_junk(text)

    if cleaned != text or encoding != "utf-8":
        print(f"[FIX] Normalizing to UTF-8: {path}")
        path.write_text(cleaned, encoding="utf-8")


def scan_and_repair():
    print("\n=== Encoding Repair & Binary Cleanup ===\n")

    py_files = list(TARGET_DIR.rglob("*.py"))

    corrupted = []
    binaries = []

    for py_file in py_files:
        if is_binary(py_file):
            binaries.append(py_file)
            continue

        text, encoding = safe_read(py_file)
        if text is None:
            corrupted.append(py_file)
            continue

        # Detect invalid characters
        if "\x00" in text or any(ord(c) < 9 for c in text):
            corrupted.append(py_file)

    # Step 1 — Report binary files
    print(f"[INFO] Scanned {len(py_files)} Python files.\n")

    if binaries:
        print(f"[!] {len(binaries)} binary-like Python files detected:\n")
        for f in binaries:
            print(f"  - {f}")
        print("\nThese will NOT be modified (manual inspection recommended).\n")
    else:
        print("[OK] No binary-like Python files detected.\n")

    # Step 2 — Normalize corrupted files
    if corrupted:
        print(f"[!] {len(corrupted)} corrupted Python files detected. Normalizing...\n")
        for f in corrupted:
            normalize_to_utf8(f)
    else:
        print("[OK] No corrupted Python files detected.\n")

    print("\n=== Repair Complete ===\n")


if __name__ == "__main__":
    scan_and_repair()
