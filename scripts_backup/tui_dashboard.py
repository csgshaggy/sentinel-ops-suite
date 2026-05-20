from __future__ import annotations

import curses
import json
import time
from typing import Any, Dict, List

from tools.anomaly_detector import detect_anomalies
from tools.makefile.autorepair import autorepair
from tools.makefile.drift_detector import detect_drift
from tools.makefile.health import compute_health
from tools.makefile.linter import lint_makefile
from tools.makefile.version_check import check_version
from tools.plugin_registry_viewer import list_plugins
from tools.security.file_integrity_monitor import (
    build_baseline as fim_build_baseline,
)
from tools.security.file_integrity_monitor import (
    load_baseline as fim_load_baseline,
)
from tools.security.file_integrity_monitor import (
    scan as fim_scan,
)
from tools.super_doctor import run_super_doctor

EVENT_LOG_PATH = "logs/events.log"
FIM_MONITORED_PATHS = [".", "tools/", "scripts/", "/etc", "/usr/local/bin"]


# ------------------------------------------------------------
# Utility Rendering Helpers
# ------------------------------------------------------------


def _draw(
    stdscr: curses.window, y: int, x: int, text: str, color: int | None = None
) -> None:
    try:
        if color is not None:
            stdscr.attron(curses.color_pair(color))
        stdscr.addstr(y, x, text)
        if color is not None:
            stdscr.attroff(curses.color_pair(color))
    except Exception:
        pass


def _health_color(score: int) -> int:
    if score >= 90:
        return 1
    if score >= 70:
        return 2
    return 3


# ------------------------------------------------------------
# System-Wide Health Score (Weighted Model)
# ------------------------------------------------------------


def compute_fim_health(fim_result: Dict[str, Any] | None) -> int:
    if not fim_result:
        return 100
    anomalies = fim_result.get("anomalies", [])
    if not anomalies:
        return 100
    penalty = min(80, len(anomalies) * 5)
    return max(20, 100 - penalty)


def compute_system_health(
    doctor_health: int,
    makefile_health: int,
    plugin_integrity: int,
    fim_health: int,
) -> int:
    score = (
        0.40 * doctor_health
        + 0.25 * makefile_health
        + 0.20 * plugin_integrity
        + 0.15 * fim_health
    )
    return int(score)


def compute_plugin_integrity(plugins: List[Dict[str, Any]]) -> int:
    if plugins is None:
        return 0
    if len(plugins) == 0:
        return 50

    missing_meta = any(not p.get("name") or not p.get("category") for p in plugins)
    if missing_meta:
        return 80

    return 100


# ------------------------------------------------------------
# Main Doctor Dashboard (Scrollable)
# ------------------------------------------------------------


def _render_dashboard(stdscr: curses.window, data: Dict[str, Any], offset: int) -> None:
    stdscr.clear()
    stdscr.border()

    height, width = stdscr.getmaxyx()
    center = width // 2

    summary = data.get("summary", {})
    checks: List[Dict[str, Any]] = data.get("checks", [])

    doctor_health = summary.get("health_score", 0)
    plugin_list = list_plugins({})
    plugin_integrity = compute_plugin_integrity(plugin_list)
    makefile_health = compute_health().get("health_score", 0)

    fim_result = None
    try:
        fim_result = fim_scan(FIM_MONITORED_PATHS)
    except Exception:
        fim_result = None
    fim_health = compute_fim_health(fim_result)

    system_health = compute_system_health(
        doctor_health,
        makefile_health,
        plugin_integrity,
        fim_health,
    )

    title = "SSRF COMMAND CONSOLE — TUI DASHBOARD"
    _draw(stdscr, 1, center - len(title) // 2, title, color=4)

    _draw(stdscr, 3, 2, f"Timestamp:         {time.strftime('%Y-%m-%d %H:%M:%S')}")
    _draw(stdscr, 4, 2, f"Doctor Status:     {summary.get('overall_status')}")
    _draw(
        stdscr,
        5,
        2,
        f"Doctor Health:     {doctor_health}",
        color=_health_color(doctor_health),
    )
    _draw(
        stdscr,
        6,
        2,
        f"Makefile Health:   {makefile_health}",
        color=_health_color(makefile_health),
    )
    _draw(
        stdscr,
        7,
        2,
        f"FIM Health:        {fim_health}",
        color=_health_color(fim_health),
    )
    _draw(
        stdscr,
        8,
        2,
        f"System Health:     {system_health}",
        color=_health_color(system_health),
    )

    _draw(stdscr, 10, 2, "Plugins:", color=4)
    _draw(stdscr, 11, 2, "NAME                CATEGORY    STATUS    DURATION(s)")

    max_rows = height - 15
    for i in range(max_rows):
        idx = offset + i
        if idx >= len(checks):
            break

        check = checks[idx]
        name = check["plugin"][:18]
        category = check["category"][:10]
        status = check["status"]
        duration = f"{check['duration_seconds']:.4f}"

        line = f"{name:<18}  {category:<10}  {status:<8}  {duration:>10}"
        color = 1 if status == "ok" else 3
        _draw(stdscr, 12 + i, 2, line, color=color)

    _draw(
        stdscr,
        height - 2,
        2,
        "q: quit | g: governance hub | j/k: scroll plugins",
        color=5,
    )

    stdscr.refresh()


# ------------------------------------------------------------
# Makefile Governance Panel
# ------------------------------------------------------------


def _makefile_panel(stdscr: curses.window) -> None:
    drift = detect_drift()
    health = compute_health()
    lint = lint_makefile()
    version = check_version()

    diff_lines = drift["diff"]
    offset = 0
    search_term: str | None = None
    matches: List[int] = []
    match_index = 0

    def recompute_matches() -> None:
        nonlocal matches, match_index
        matches = []
        match_index = 0
        if not search_term:
            return
        lower = search_term.lower()
        for i, line in enumerate(diff_lines):
            if lower in line.lower():
                matches.append(i)

    while True:
        stdscr.clear()
        stdscr.border()
        height, width = stdscr.getmaxyx()

        _draw(stdscr, 1, 2, "MAKEFILE GOVERNANCE PANEL", color=4)
        _draw(
            stdscr,
            3,
            2,
            f"Drift Detected:     {drift['drift']}",
            color=3 if drift["drift"] else 1,
        )
        _draw(
            stdscr,
            4,
            2,
            f"Health Score:       {health['health_score']}",
            color=_health_color(health["health_score"]),
        )
        _draw(
            stdscr,
            5,
            2,
            f"Linter OK:          {lint['ok']}",
            color=1 if lint["ok"] else 3,
        )
        _draw(
            stdscr,
            6,
            2,
            f"Version Stamp:      {version.get('version') or 'MISSING'}",
            color=1 if version.get("found") else 3,
        )
        _draw(stdscr, 7, 2, f"Search: {search_term or ''}")

        _draw(
            stdscr,
            9,
            2,
            "Diff (j/k scroll, / search, n next, r repair, b back):",
            color=5,
        )

        max_lines = height - 14
        for i in range(max_lines):
            idx = offset + i
            if idx >= len(diff_lines):
                break
            is_current_match = matches and idx == matches[match_index]
            prefix = "> " if is_current_match else "  "
            color = 2 if is_current_match else None
            _draw(
                stdscr, 10 + i, 2, (prefix + diff_lines[idx])[: width - 4], color=color
            )

        _draw(
            stdscr,
            height - 2,
            2,
            "b: back | j/k: scroll | /: search | n: next match | r: auto-repair",
            color=5,
        )

        stdscr.refresh()
        key = stdscr.getch()

        if key in (ord("b"), ord("B")):
            break
        if key in (ord("j"), curses.KEY_DOWN):
            if offset + 1 < len(diff_lines):
                offset += 1
        if key in (ord("k"), curses.KEY_UP):
            if offset > 0:
                offset -= 1
        if key in (ord("r"), ord("R")):
            autorepair()
            drift = detect_drift()
            health = compute_health()
            lint = lint_makefile()
            version = check_version()
            diff_lines = drift["diff"]
            offset = 0
            recompute_matches()
        if key == ord("/"):
            curses.echo()
            _draw(stdscr, 7, 2, "Search: ")
            stdscr.clrtoeol()
            search_bytes = stdscr.getstr(7, 10, 40)
            curses.noecho()
            try:
                search_term = search_bytes.decode("utf-8")
            except Exception:
                search_term = ""
            offset = 0
            recompute_matches()
            if matches:
                offset = max(matches[0] - 2, 0)
        if key == ord("n"):
            if matches:
                match_index = (match_index + 1) % len(matches)
                offset = max(matches[match_index] - 2, 0)


# ------------------------------------------------------------
# Plugin Governance Panel
# ------------------------------------------------------------


def _plugin_panel(stdscr: curses.window) -> None:
    plugins = list_plugins({})
    offset = 0

    while True:
        stdscr.clear()
        stdscr.border()
        height, width = stdscr.getmaxyx()

        _draw(stdscr, 1, 2, "PLUGIN GOVERNANCE PANEL", color=4)
        _draw(stdscr, 3, 2, f"Total plugins: {len(plugins)}")
        _draw(stdscr, 5, 2, "NAME                CATEGORY    ENTRYPOINT")

        max_rows = height - 10
        for i in range(max_rows):
            idx = offset + i
            if idx >= len(plugins):
                break

            p = plugins[idx]
            name = p["name"][:18]
            category = p["category"][:10]
            entry = (p.get("entrypoint") or "")[:20]

            line = f"{name:<18}  {category:<10}  {entry:<20}"
            _draw(stdscr, 6 + i, 2, line)

        _draw(stdscr, height - 2, 2, "b: back | j/k: scroll", color=5)

        stdscr.refresh()
        key = stdscr.getch()

        if key in (ord("b"), ord("B")):
            break
        if key in (ord("j"), curses.KEY_DOWN):
            if offset + 1 < len(plugins):
                offset += 1
        if key in (ord("k"), curses.KEY_UP):
            if offset > 0:
                offset -= 1


# ------------------------------------------------------------
# Plugin Dependency Graph Panel (ASCII)
# ------------------------------------------------------------


def _plugin_graph_panel(stdscr: curses.window) -> None:
    plugins = list_plugins({})
    deps_map: Dict[str, List[str]] = {}
    for p in plugins:
        name = p["name"]
        deps = p.get("depends_on") or []
        deps_map[name] = deps

    stdscr.clear()
    stdscr.border()
    height, width = stdscr.getmaxyx()

    _draw(stdscr, 1, 2, "PLUGIN DEPENDENCY GRAPH (ASCII)", color=4)
    row = 3

    for name, deps in deps_map.items():
        if row >= height - 2:
            break
        _draw(stdscr, row, 2, name, color=1)
        row += 1
        if not deps:
            _draw(stdscr, row, 4, "└── (no deps)")
            row += 1
            continue
        for i, dep in enumerate(deps):
            if row >= height - 2:
                break
            connector = "└──" if i == len(deps) - 1 else "├──"
            _draw(stdscr, row, 4, f"{connector} {dep}")
            row += 1

    _draw(stdscr, height - 2, 2, "Press 'b' to go back", color=5)
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key in (ord("b"), ord("B")):
            break


# ------------------------------------------------------------
# Real-Time Event Log Panel (Non-blocking)
# ------------------------------------------------------------


def _read_event_log(max_lines: int) -> List[str]:
    try:
        with open(EVENT_LOG_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return ["<no event log found>"]
    return lines[-max_lines:]


def _event_log_panel(stdscr: curses.window) -> None:
    offset = 0
    stdscr.nodelay(True)
    try:
        while True:
            stdscr.clear()
            stdscr.border()
            height, width = stdscr.getmaxyx()

            lines = _read_event_log(1000)
            _draw(stdscr, 1, 2, "REAL-TIME EVENT LOG", color=4)
            _draw(
                stdscr,
                3,
                2,
                "j/k: scroll | b: back (non-blocking, auto-refresh)",
                color=5,
            )

            max_rows = height - 7
            for i in range(max_rows):
                idx = offset + i
                if idx >= len(lines):
                    break
                _draw(stdscr, 4 + i, 2, lines[idx].rstrip("\n")[: width - 4])

            stdscr.refresh()
            time.sleep(0.3)

            key = stdscr.getch()
            if key == -1:
                continue

            if key in (ord("b"), ord("B")):
                break
            if key in (ord("j"), curses.KEY_DOWN):
                if offset + 1 < len(lines):
                    offset += 1
            if key in (ord("k"), curses.KEY_UP):
                if offset > 0:
                    offset -= 1
    finally:
        stdscr.nodelay(False)


# ------------------------------------------------------------
# System-Wide Anomaly Detector Panel + Heatmap
# ------------------------------------------------------------


def _anomaly_panel(stdscr: curses.window) -> None:
    result = detect_anomalies()
    anomalies = result["anomalies"]

    stdscr.clear()
    stdscr.border()
    height, width = stdscr.getmaxyx()

    _draw(stdscr, 1, 2, "SYSTEM-WIDE ANOMALY DETECTOR", color=4)
    _draw(stdscr, 3, 2, f"OK: {result['ok']}", color=1 if result["ok"] else 3)

    row = 5
    if not anomalies:
        _draw(stdscr, row, 2, "No anomalies detected.")
    else:
        for a in anomalies:
            if row >= height - 4:
                break
            _draw(stdscr, row, 2, f"- {a}"[: width - 4], color=3)
            row += 1

    count = len(anomalies)
    max_bar_width = width - 4
    bar_width = min(max_bar_width, max(1, count * 4))
    color = 1 if count == 0 else 2 if count <= 3 else 3
    _draw(stdscr, height - 4, 2, "Anomaly Heatmap:", color=5)
    _draw(stdscr, height - 3, 2, "█" * bar_width, color=color)

    _draw(stdscr, height - 2, 2, "Press 'b' to go back", color=5)
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key in (ord("b"), ord("B")):
            break


# ------------------------------------------------------------
# Plugin Execution Timeline Panel (with FIM events)
# ------------------------------------------------------------


def _plugin_timeline_panel(stdscr: curses.window) -> None:
    result = run_super_doctor({})
    checks: List[Dict[str, Any]] = result.get("checks", [])

    fim_events: List[Dict[str, Any]] = []
    try:
        with open(EVENT_LOG_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    evt = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if evt.get("event") in (
                    "file_added",
                    "file_deleted",
                    "file_modified",
                    "permission_changed",
                    "readability_changed",
                ):
                    fim_events.append(evt)
    except FileNotFoundError:
        pass

    stdscr.clear()
    stdscr.border()
    height, width = stdscr.getmaxyx()

    _draw(stdscr, 1, 2, "PLUGIN EXECUTION TIMELINE + FIM EVENTS", color=4)

    if not checks and not fim_events:
        _draw(stdscr, 3, 2, "No plugin execution data or FIM events available.")
        _draw(stdscr, height - 2, 2, "Press 'b' to go back", color=5)
        stdscr.refresh()
        while True:
            key = stdscr.getch()
            if key in (ord("b"), ord("B")):
                return

    max_duration = (
        max((c.get("duration_seconds", 0.0) for c in checks), default=0.0) or 1.0
    )
    max_bar_width = width - 30

    row = 3
    for check in checks:
        if row >= height - 4:
            break
        name = check["plugin"][:18]
        dur = check.get("duration_seconds", 0.0)
        bar_len = int((dur / max_duration) * max_bar_width)
        bar = "█" * max(bar_len, 1)
        line = f"{name:<18} {dur:>7.4f}s {bar}"
        _draw(stdscr, row, 2, line)
        row += 1

    if fim_events and row < height - 3:
        _draw(stdscr, row, 2, "--- FIM EVENTS ---", color=5)
        row += 1
        for evt in fim_events[-(height - row - 2) :]:
            if row >= height - 2:
                break
            label = f"{evt.get('event')} {evt.get('path', '')}"
            _draw(stdscr, row, 2, label[: width - 4], color=2)
            row += 1

    _draw(stdscr, height - 2, 2, "Press 'b' to go back", color=5)
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key in (ord("b"), ord("B")):
            break


# ------------------------------------------------------------
# File Integrity Monitoring (FIM) Panel — Regenerated & Hardened
# ------------------------------------------------------------


def _fim_panel(stdscr: curses.window) -> None:
    baseline = fim_load_baseline()
    has_baseline = bool(baseline)
    result: Dict[str, Any] | None = None

    if has_baseline:
        result = fim_scan(FIM_MONITORED_PATHS)

    anomalies = result["anomalies"] if result else []
    show_mode = "anomalies"  # "anomalies", "all", "unreadable"
    offset = 0

    def _paths_for_display() -> List[str]:
        if show_mode == "all":
            return sorted(baseline.keys())
        if show_mode == "unreadable":
            return sorted([p for p, meta in baseline.items() if meta.get("unreadable")])
        return sorted({a["path"] for a in anomalies})

    def _anomaly_for_path(path: str) -> Dict[str, Any] | None:
        for a in anomalies:
            if a["path"] == path:
                return a
        return None

    while True:
        stdscr.clear()
        stdscr.border()
        height, width = stdscr.getmaxyx()

        _draw(stdscr, 1, 2, "FILE INTEGRITY MONITOR (FIM)", color=4)
        _draw(stdscr, 3, 2, f"Monitored paths: {', '.join(FIM_MONITORED_PATHS)}")

        if not has_baseline:
            _draw(stdscr, 5, 2, "No baseline found.", color=3)
            _draw(stdscr, 6, 2, "Press 'r' to build baseline, 'b' to go back.", color=5)
            stdscr.refresh()

            key = stdscr.getch()
            if key in (ord("b"), ord("B")):
                break
            if key in (ord("r"), ord("R")):
                baseline = fim_build_baseline(FIM_MONITORED_PATHS)
                has_baseline = True
                result = fim_scan(FIM_MONITORED_PATHS)
                anomalies = result["anomalies"]
            continue

        if show_mode == "anomalies":
            mode_label = "ANOMALIES ONLY"
        elif show_mode == "all":
            mode_label = "ALL FILES"
        else:
            mode_label = "UNREADABLE ONLY"

        _draw(stdscr, 5, 2, f"Mode: {mode_label}", color=5)

        if result:
            _draw(stdscr, 6, 2, f"Baseline files: {result['baseline_count']}")
            _draw(stdscr, 7, 2, f"Current files:  {result['current_count']}")
            _draw(
                stdscr,
                8,
                2,
                f"Anomalies:      {len(anomalies)}",
                color=3 if anomalies else 1,
            )

        _draw(
            stdscr,
            10,
            2,
            "PATH (j/k scroll, a cycle mode, s scan, r rebuild, b back):",
            color=5,
        )

        paths = _paths_for_display()
        max_rows = height - 15

        for i in range(max_rows):
            idx = offset + i
            if idx >= len(paths):
                break

            path = paths[idx]
            meta = baseline.get(path, {})
            anomaly = _anomaly_for_path(path)

            if meta.get("unreadable"):
                color = 6
                label = f"[unreadable] {path}"
            elif anomaly:
                t = anomaly["type"]
                if t in ("modified", "deleted", "added"):
                    color = 3
                elif t in ("perm_changed", "readability_changed"):
                    color = 2
                else:
                    color = 2
                label = f"[{t}] {path}"
            else:
                color = 1
                label = f"[ok]        {path}"

            _draw(stdscr, 11 + i, 2, label[: width - 4], color=color)

        _draw(
            stdscr,
            height - 2,
            2,
            "b: back | j/k: scroll | a: cycle anomalies/all/unreadable | s: scan | r: rebuild baseline",
            color=5,
        )

        stdscr.refresh()
        key = stdscr.getch()

        if key in (ord("b"), ord("B")):
            break
        if key in (ord("j"), curses.KEY_DOWN):
            if offset + 1 < len(paths):
                offset += 1
        if key in (ord("k"), curses.KEY_UP):
            if offset > 0:
                offset -= 1
        if key in (ord("a"), ord("A")):
            if show_mode == "anomalies":
                show_mode = "all"
            elif show_mode == "all":
                show_mode = "unreadable"
            else:
                show_mode = "anomalies"
            offset = 0
        if key in (ord("s"), ord("S")):
            result = fim_scan(FIM_MONITORED_PATHS)
            anomalies = result["anomalies"]
            offset = 0
        if key in (ord("r"), ord("R")):
            baseline = fim_build_baseline(FIM_MONITORED_PATHS)
            has_baseline = True
            result = fim_scan(FIM_MONITORED_PATHS)
            anomalies = result["anomalies"]
            offset = 0


# ------------------------------------------------------------
# Governance Hub
# ------------------------------------------------------------


def _governance_hub(stdscr: curses.window) -> None:
    doctor_health = run_super_doctor({}).get("summary", {}).get("health_score", 0)
    makefile_health = compute_health().get("health_score", 0)
    plugin_integrity = compute_plugin_integrity(list_plugins({}))

    fim_result = None
    try:
        fim_result = fim_scan(FIM_MONITORED_PATHS)
    except Exception:
        fim_result = None
    fim_health = compute_fim_health(fim_result)

    system_health = compute_system_health(
        doctor_health,
        makefile_health,
        plugin_integrity,
        fim_health,
    )

    while True:
        stdscr.clear()
        stdscr.border()

        _draw(stdscr, 1, 2, "SYSTEM-WIDE GOVERNANCE HUB", color=4)
        _draw(
            stdscr,
            3,
            2,
            f"System Health Score: {system_health}",
            color=_health_color(system_health),
        )
        _draw(stdscr, 5, 2, "m: Makefile governance")
        _draw(stdscr, 6, 2, "p: Plugin governance")
        _draw(stdscr, 7, 2, "d: Plugin dependency graph")
        _draw(stdscr, 8, 2, "e: Event log panel")
        _draw(stdscr, 9, 2, "a: Anomaly detector + heatmap")
        _draw(stdscr, 10, 2, "t: Plugin execution timeline")
        _draw(stdscr, 11, 2, "f: File Integrity Monitor (FIM)")
        _draw(stdscr, 13, 2, "b: back to main dashboard", color=5)

        stdscr.refresh()
        key = stdscr.getch()

        if key in (ord("b"), ord("B")):
            break
        if key in (ord("m"), ord("M")):
            _makefile_panel(stdscr)
        if key in (ord("p"), ord("P")):
            _plugin_panel(stdscr)
        if key in (ord("d"), ord("D")):
            _plugin_graph_panel(stdscr)
        if key in (ord("e"), ord("E")):
            _event_log_panel(stdscr)
        if key in (ord("a"), ord("A")):
            _anomaly_panel(stdscr)
        if key in (ord("t"), ord("T")):
            _plugin_timeline_panel(stdscr)
        if key in (ord("f"), ord("F")):
            _fim_panel(stdscr)


# ------------------------------------------------------------
# Data Provider
# ------------------------------------------------------------


def _generate_dashboard_data() -> Dict[str, Any]:
    result = run_super_doctor({})
    return {
        "summary": result.get("summary", {}),
        "checks": result.get("checks", []),
    }


# ------------------------------------------------------------
# Main TUI Loop
# ------------------------------------------------------------


def run_tui_dashboard() -> None:
    def _main(stdscr: curses.window) -> None:
        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)
        curses.init_pair(2, curses.COLOR_YELLOW, -1)
        curses.init_pair(3, curses.COLOR_RED, -1)
        curses.init_pair(4, curses.COLOR_CYAN, -1)
        curses.init_pair(5, curses.COLOR_MAGENTA, -1)
        curses.init_pair(6, curses.COLOR_BLUE, -1)

        offset = 0

        while True:
            data = _generate_dashboard_data()
            _render_dashboard(stdscr, data, offset)

            key = stdscr.getch()

            if key in (ord("q"), ord("Q")):
                break

            if key in (ord("g"), ord("G")):
                _governance_hub(stdscr)

            if key in (ord("j"), curses.KEY_DOWN):
                offset += 1
            if key in (ord("k"), curses.KEY_UP):
                if offset > 0:
                    offset -= 1

            time.sleep(0.1)

    curses.wrapper(_main)


if __name__ == "__main__":
    run_tui_dashboard()
