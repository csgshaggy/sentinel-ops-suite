#!/usr/bin/env python3
import os
import sys

from scripts.drift_detector import compare, load_baseline, walk_tree

OUTPUT_MD = "runtime/drift_ci_comment.md"
os.makedirs("runtime", exist_ok=True)


def main():
    drift_fail = os.getenv("DRIFT_FAIL", "1") == "1"

    current = walk_tree()
    baseline = load_baseline()

    if baseline is None:
        with open(OUTPUT_MD, "w") as f:
            f.write(
                "### ⚠️ No baseline found\nA baseline must be generated before drift can be checked."
            )
        if drift_fail:
            sys.exit(1)
        return

    drift = compare(baseline, current)

    # Import markdown formatter
    from scripts.ci.drift_markdown import format_markdown

    md = format_markdown(drift)

    with open(OUTPUT_MD, "w") as f:
        f.write(md)

    # Fail CI only if toggle is enabled
    if drift_fail and any(drift.values()):
        sys.exit(1)


if __name__ == "__main__":
    main()
