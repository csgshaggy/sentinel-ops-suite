import os

PROJECT_ROOT = os.path.expanduser("~/ssrf-command-console")

EXPECTED_DIRS = [
    "src",
    "scripts",
    "docs",
    "config",
    "data",
    "tools",
]

def main():
    print(f"\n=== Directory Tree Validator ===")
    print(f"Project root: {PROJECT_ROOT}\n")

    dirs = [
        d for d in os.listdir(PROJECT_ROOT)
        if os.path.isdir(os.path.join(PROJECT_ROOT, d))
    ]

    print("Found directories:")
    for d in dirs:
        print(f"  - {d}")

    print("\nMissing expected directories:")
    missing = [d for d in EXPECTED_DIRS if d not in dirs]
    if missing:
        for d in missing:
            print(f"  - {d}")
    else:
        print("  None")

    print("\nExtra directories (unexpected):")
    extras = [d for d in dirs if d not in EXPECTED_DIRS]
    if extras:
        for d in extras:
            print(f"  - {d}")
    else:
        print("  None")

if __name__ == "__main__":
    main()
