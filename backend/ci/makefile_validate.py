import sys
from backend.ci.makefile_tools import validate_makefile

def main():
    result = validate_makefile()
    if result["match"]:
        print("[makefile-validate] OK: Makefile matches canonical structure.")
        sys.exit(0)
    else:
        print("[makefile-validate] FAIL: Makefile does not match canonical structure.")
        print(
            f"  current length={result['length_current']}, "
            f"canonical length={result['length_canonical']}"
        )
        sys.exit(1)

if __name__ == "__main__":
    main()
