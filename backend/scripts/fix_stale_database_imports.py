#!/usr/bin/env python3
import os

TARGET = "from app.database import get_db"
REPLACEMENT = "from app.db.session import get_db"

PATCHED = []

for root, dirs, files in os.walk("app"):
    for file in files:
        if not file.endswith(".py"):
            continue

        path = os.path.join(root, file)

        with open(path, "r") as f:
            content = f.read()

        if TARGET in content:
            new_content = content.replace(TARGET, REPLACEMENT)

            with open(path, "w") as f:
                f.write(new_content)

            PATCHED.append(path)

print("\n=== PATCH COMPLETE ===")
if PATCHED:
    print("Updated imports in:")
    for p in PATCHED:
        print("  -", p)
else:
    print("No stale imports found.")
