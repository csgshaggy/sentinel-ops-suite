#!/usr/bin/env python3
"""
Sentinel Ops Suite — Drift Detector
Plugin-driven baseline/snapshot/diff/check engine.
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Import plugin registry using RELATIVE imports
from .drift_modules import PLUGINS


# =====================================================================
# JSON UTILITIES
# =====================================================================

def write_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, sort_keys=True)


def load_json(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


# =====================================================================
# STATE COLLECTION (PLUGIN-DRIVEN)
# =====================================================================

def generate_state(root: Path) -> dict:
    """
    Runs all registered drift plugins in deterministic order.
    Each plugin returns a dict; results are merged under plugin.name.
    """
    state = {}
    for plugin in PLUGINS:
        try:
            state[plugin.name] = plugin.collect(root)
        except Exception as e:
            print(f"[drift] ERROR: Plugin '{plugin.name}' failed: {e}")
            sys.exit(1)
    return state


# =====================================================================
# DIFF ENGINE
# =====================================================================

def diff_states(baseline: dict, snapshot: dict) -> dict:
    """
    Computes a deterministic diff between plugin outputs.
    Each plugin's diff is plugin-specific.
    """
    diff = {}

    for plugin in PLUGINS:
        name = plugin.name
        base = baseline.get(name, {})
        snap = snapshot.get(name, {})

        # Filesystem plugin: detect added/removed/changed files
        if name == "filesystem_hash":
            base_keys = set(base.keys())
            snap_keys = set(snap.keys())

            added = sorted(snap_keys - base_keys)
            removed = sorted(base_keys - snap_keys)
            changed = sorted([k for k in base_keys & snap_keys if base[k] != snap[k]])

            diff[name] = {
                "added": added,
                "removed": removed,
                "changed": changed,
            }
            continue

        # Git metadata plugin: detect branch/commit/status changes
        if name == "git_metadata":
            diff[name] = {
                "branch_changed": base.get("branch") != snap.get("branch"),
                "commit_changed": base.get("commit") != snap.get("commit"),
                "working_tree_clean": snap.get("working_tree_clean", False),
                "changes": snap.get("changes", []),
            }
            continue

        # Default: simple structural diff
        diff[name] = {
            "baseline": base,
            "snapshot": snap,
            "changed": base != snap,
        }

    return diff


def has_drift(diff: dict) -> bool:
    """
    Determines whether any plugin reports drift.
    """
    for plugin in PLUGINS:
        name = plugin.name
        section = diff.get(name, {})

        # Filesystem plugin
        if name == "filesystem_hash":
            if section["added"] or section["removed"] or section["changed"]:
                return True

        # Git metadata plugin
        if name == "git_metadata":
            if (
                section["branch_changed"]
                or section["commit_changed"]
                or not section["working_tree_clean"]
            ):
                return True

        # Generic plugin
        if section.get("changed"):
            return True

    return False


# =====================================================================
# CLI
# =====================================================================

def main():
    parser = argparse.ArgumentParser(description="Sentinel Ops Suite Drift Detector")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # baseline
    p = sub.add_parser("baseline")
    p.add_argument("--output", required=True)

    # snapshot
    p = sub.add_parser("snapshot")
    p.add_argument("--output", required=True)

    # diff
    p = sub.add_parser("diff")
    p.add_argument("--baseline", required=True)
    p.add_argument("--snapshot", required=True)
    p.add_argument("--output", required=True)

    # check
    p = sub.add_parser("check")
    p.add_argument("--baseline", required=True)

    args = parser.parse_args()
    root = Path(os.getcwd())

    # ------------------------------------------------------------------
    # baseline
    # ------------------------------------------------------------------
    if args.cmd == "baseline":
        state = generate_state(root)
        write_json(Path(args.output), state)
        print(f"[drift] Baseline written to {args.output}")
        return

    # ------------------------------------------------------------------
    # snapshot
    # ------------------------------------------------------------------
    if args.cmd == "snapshot":
        state = generate_state(root)
        write_json(Path(args.output), state)
        print(f"[drift] Snapshot written to {args.output}")
        return

    # ------------------------------------------------------------------
    # diff
    # ------------------------------------------------------------------
    if args.cmd == "diff":
        baseline = load_json(Path(args.baseline))
        snapshot = load_json(Path(args.snapshot))
        d = diff_states(baseline, snapshot)
        write_json(Path(args.output), d)
        print(f"[drift] Diff written to {args.output}")
        return

    # ------------------------------------------------------------------
    # check
    # ------------------------------------------------------------------
    if args.cmd == "check":
        baseline = load_json(Path(args.baseline))
        snapshot = generate_state(root)
        d = diff_states(baseline, snapshot)

        if has_drift(d):
            print("[drift] DRIFT DETECTED — commit blocked.")
            print(json.dumps(d, indent=2))
            sys.exit(1)

        print("[drift] No drift detected.")
        return


if __name__ == "__main__":
    main()
