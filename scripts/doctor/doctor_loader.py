#!/usr/bin/env python3
import importlib
import os
import json
from pathlib import Path

VALIDATOR_DIR = "validators"

def load_validators():
    validators = []
    for file in os.listdir(VALIDATOR_DIR):
        if file.endswith(".py") and not file.startswith("__"):
            module_name = file[:-3]
            module_path = f"{VALIDATOR_DIR}.{module_name}"
            module = importlib.import_module(module_path)

            if hasattr(module, "run"):
                validators.append(module)
    return validators

def main():
    print("\n=== DOCTOR SUITE (Plugin Mode) ===\n")

    validators = load_validators()
    results = []

    for v in validators:
        try:
            result = v.run()
            results.append(result)

            status = result.get("status", "unknown")
            name = result.get("name", v.__name__)

            if status == "ok":
                print(f"🟩 {name}: OK")
            else:
                print(f"🟥 {name}: FAIL")

        except Exception as e:
            print(f"🟥 {v.__name__}: ERROR — {e}")
            results.append({
                "name": v.__name__,
                "status": "error",
                "details": [str(e)]
            })

    # Save machine-readable output
    os.makedirs("runtime", exist_ok=True)
    with open("runtime/doctor_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n[+] Doctor suite complete.\n")

if __name__ == "__main__":
    main()
