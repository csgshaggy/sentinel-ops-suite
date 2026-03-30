import json
import subprocess
from datetime import datetime
from pathlib import Path

HEALTH_FILE = Path("health.json")
HISTORY_FILE = Path("health_history.jsonl")

def run(cmd):
    try:
        subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False

def compute_health_score():
    score = 100
    checks = {}

    # Drift check
    drift_ok = run("make drift")
    checks["drift"] = drift_ok
    if not drift_ok:
        score -= 25

    # Lint check
    lint_ok = run("make lint")
    checks["lint"] = lint_ok
    if not lint_ok:
        score -= 15

    # Format check
    format_ok = run("make format")
    checks["format"] = format_ok
    if not format_ok:
        score -= 10

    # CI-fast
    ci_ok = run("make ci-fast")
    checks["ci_fast"] = ci_ok
    if not ci_ok:
        score -= 25

    # Permissions check
    perm_ok = run("./auto_repair_permissions.sh")
    checks["permissions"] = perm_ok
    if not perm_ok:
        score -= 10

    # Final score floor
    score = max(score, 0)

    result = {
        "timestamp": datetime.utcnow().isoformat(),
        "score": score,
        "checks": checks,
    }

    # Write current health
    HEALTH_FILE.write_text(json.dumps(result, indent=2))

    # Append to history
    with HISTORY_FILE.open("a") as f:
        f.write(json.dumps(result) + "\n")

    return result
