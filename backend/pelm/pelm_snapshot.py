import json
from backend.pelm import pelm_plugin
from backend.pelm.pelm_tools import snapshot_pelm_output, validate_pelm_contract


def main():
    output = pelm_plugin.run_pelm()

    contract = validate_pelm_contract(output)
    if not contract["valid"]:
        print("[pelm-snapshot] INVALID CONTRACT:", json.dumps(contract, indent=2))
        return

    result = snapshot_pelm_output(output)
    print("[pelm-snapshot] Snapshot written:", result["snapshot"])


if __name__ == "__main__":
    main()
