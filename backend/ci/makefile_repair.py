import sys
from backend.ci.makefile_tools import auto_repair

def main():
    result = auto_repair()
    print(f"[makefile-repair] Repaired Makefile at {result['path']}")
    sys.exit(0)

if __name__ == "__main__":
    main()
