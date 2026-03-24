import subprocess


def run():
    result = {
        "status": "ok",
        "makefile_present": False,
        "duplicates": False,
        "details": [],
    }

    # Check Makefile presence
    try:
        with open("Makefile", "r"):
            result["makefile_present"] = True
            result["details"].append("Makefile found in project root.")
    except FileNotFoundError:
        result["status"] = "error"
        result["details"].append("Makefile missing in project root.")
        return result

    # Run makefile_doctor
    proc = subprocess.run(
        ["python3", "scripts/makefile_doctor.py"],
        capture_output=True,
        text=True,
    )

    if proc.returncode != 0:
        result["status"] = "warning"
        result["duplicates"] = True
        result["details"].append("Duplicate targets detected in Makefile.")
        result["details"].append(proc.stdout.strip() or proc.stderr.strip())
    else:
        result["details"].append("No duplicate Makefile targets detected.")

    return result
