#!/usr/bin/env bash
set -euo pipefail

echo ""
echo "=== SSRF Console Project Migration Script (Final Hardened Version) ==="
echo "This will reorganize your project into a clean operator-grade layout."
echo ""

ROOT="$(pwd)"

# --- Helper function ---
move_safe() {
    src="$1"
    dest="$2"

    if [ -e "$src" ]; then
        mkdir -p "$(dirname "$dest")"
        echo "[MOVE] $src → $dest"
        mv "$src" "$dest"
    fi
}

echo "[*] Creating new directory structure..."

mkdir -p src/ssrf_console
mkdir -p src/ssrf_console/{modes,plugins,static,ssrf_scanner,ssrf_manager,dashboard,templates}
mkdir -p scripts
mkdir -p runtime/{logs,crash_reports,results,out}
mkdir -p data/baseline
mkdir -p config/systemd
mkdir -p docs

echo ""
echo "[*] Moving Python source files into src/ssrf_console/..."

# Core Python modules
for f in analyzer.py dispatcher.py metadata_tools.py ops.py mode_template.py dashboard.py dashboard_web.py ws_dashboard_unused.py main.py; do
    move_safe "$f" "src/ssrf_console/$f"
done

# Python packages
for d in ssrf_scanner ssrf_manager dashboard static modes plugins console app; do
    if [ -d "$d" ]; then
        move_safe "$d" "src/ssrf_console/$d"
    fi
done

echo ""
echo "[*] Moving templates directory into Python package..."

if [ -d "templates" ]; then
    move_safe "templates" "src/ssrf_console/templates"
fi

echo ""
echo "[*] Moving scripts into scripts/..."

for f in cleanup_ssrf_console.sh kill_port.sh run_backend.sh run_backend.bat run_tui.sh run_tui.bat run_uvicorn.py validate_tree.py verify_structure.py preflight_scanner.py healthcheck.sh run_all.sh scanner_launcher.py; do
    move_safe "$f" "scripts/$f"
done

echo ""
echo "[*] Moving runtime artifacts..."

for f in nohup.out tui_error.log tu_error.log favorites.json; do
    move_safe "$f" "runtime/$f"
done

for d in logs crash_reports results out; do
    if [ -d "$d" ]; then
        move_safe "$d" "runtime/$d"
    fi
done

echo ""
echo "[*] Moving data files..."

for f in targets.txt targets_history.json usernames_raw.txt usernames_clean.txt usernames_final.txt users.txt kerberoastables.txt; do
    move_safe "$f" "data/$f"
done

if [ -d baseline ]; then
    move_safe "baseline" "data/baseline"
fi

echo ""
echo "[*] Moving configuration files..."

move_safe "config.yaml" "config/config.yaml"
move_safe "ssrf_config.json" "config/ssrf_config.json"
move_safe "gunicorn_conf.py" "config/gunicorn_conf.py"

if [ -d systemd ]; then
    move_safe "systemd" "config/systemd"
fi

echo ""
echo "[*] Moving documentation..."

move_safe "HELP.md" "docs/HELP.md"
move_safe "gitcleanup.txt" "docs/gitcleanup.txt"

if [ -d dev ]; then
    move_safe "dev" "docs/dev"
fi

echo ""
echo "[+] Migration complete!"
echo ""
echo "Final structure:"
echo "----------------------------------------"
tree -L 4 || echo 'Install tree with: sudo apt install tree'
echo "----------------------------------------"
echo ""
echo "Review the structure above. If everything looks correct, commit the changes."
