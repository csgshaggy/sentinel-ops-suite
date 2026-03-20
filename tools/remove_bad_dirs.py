import os
import shutil

PROJECT_ROOT = os.path.expanduser("~/ssrf-command-console")

BAD_DIRS = [
    # Add incorrect directories here, e.g.:
    # "fastapi_wrong",
    # "old_dashboard",
]

def main():
    print("\n=== Directory Cleanup Tool ===")
    print(f"Project root: {PROJECT_ROOT}\n")

    if not BAD_DIRS:
        print("No directories marked for removal.")
        return

    for d in BAD_DIRS:
        path = os.path.join(PROJECT_ROOT, d)

        if os.path.isdir(path):
            print(f"[REMOVE] {path}")
            shutil.rmtree(path)
        else:
            print(f"[SKIP] {path} (not found)")

    print("\nCleanup complete.")

if __name__ == "__main__":
    main()
