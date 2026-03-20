import ast
from pathlib import Path

PROJECT_ROOT = Path.home() / "ssrf-command-console"
SRC_ROOT = PROJECT_ROOT / "src"

def validate_python_files():
    print(f"[OK] Project root: {PROJECT_ROOT}")
    print(f"[OK] Scanning for Python syntax errors...\n")

    failed = []

    for py_file in SRC_ROOT.rglob("*.py"):
        rel = py_file.relative_to(PROJECT_ROOT)
        print(f"[TEST] Checking {rel} ... ", end="")
        try:
            ast.parse(py_file.read_text(), filename=str(py_file))
            print("OK")
        except SyntaxError as e:
            print("FAIL")
            failed.append((rel, str(e)))

    print("\n=== Syntax Validation Summary ===")
    print(f"[!] {len(failed)} file(s) failed:\n")

    for name, err in failed:
        print(f"--- {name} ---")
        print(err)

if __name__ == "__main__":
    validate_python_files()
