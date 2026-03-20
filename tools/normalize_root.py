import os

PROJECT_ROOT = os.path.expanduser("~/ssrf-command-console")

EXPECTED = {
    "src": "source code",
    "scripts": "dashboard assets + utilities",
    "docs": "documentation",
    "tools": "operator scripts",
    "config": "configuration files",
    "data": "runtime or input data",
}

def main():
    print("\n=== Project Root Normalizer ===")
    print(f"Project root: {PROJECT_ROOT}\n")

    found = {
        d for d in os.listdir(PROJECT_ROOT)
        if os.path.isdir(os.path.join(PROJECT_ROOT, d))
    }

    print("Expected directories:")
    for d, desc in EXPECTED.items():
        print(f"  - {d}: {desc}")

    print("\nMissing:")
    for d in EXPECTED:
        if d not in found:
            print(f"  - {d}")

    print("\nUnexpected directories:")
    for d in found:
        if d not in EXPECTED:
            print(f"  - {d}")

    print("\nNormalization complete.")

if __name__ == "__main__":
    main()
