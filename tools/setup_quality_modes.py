#!/usr/bin/env python3
"""
Complete Quality Mode System Installer

Installs:
  • README section explaining strict vs balanced modes
  • Makefile targets to toggle modes
  • GitHub badge for active mode
  • Slack/Discord notification hook for strict failures
  • Dashboard indicator showing active mode

Idempotent. Safe to run multiple times.
"""

import re
from pathlib import Path

# Paths
PROJECT_ROOT = Path.home() / "ssrf-command-console"
README = PROJECT_ROOT / "README.md"
MAKEFILE = PROJECT_ROOT / "Makefile"
DASHBOARD = PROJECT_ROOT / "docs" / "dashboard.html"
CONFIG_DIR = PROJECT_ROOT / "config"
MODE_FILE = CONFIG_DIR / "quality_mode.txt"
WEBHOOK_FILE = CONFIG_DIR / "webhook_url.txt"

# Badges
STRICT_BADGE = "https://img.shields.io/badge/quality_mode-strict-d32f2f"
BALANCED_BADGE = "https://img.shields.io/badge/quality_mode-balanced-2ea44f"

# README block
README_BLOCK = f"""
## Quality Modes

Your project supports two CI enforcement modes:

### **Strict Mode**
- Blocks FAIL, WARN, dead files, unused functions, circular imports
- Blocks score < 80
- Blocks score drop > 5 points
- Blocks any regression
- Used for high‑assurance environments

Badge: ![Strict Mode]({STRICT_BADGE})

---

### **Balanced Mode**
- Blocks FAIL only
- Blocks score < 70
- Blocks score drop > 10 points
- Allows WARNs, dead files, unused functions
- Used for normal development

Badge: ![Balanced Mode]({BALANCED_BADGE})

---

### **Current Mode**
The active mode is stored in:

config/quality_mode.txt


This file is read by:
- GitHub Actions workflows
- Dashboard generator
- Makefile toggles
"""

# Makefile block
MAKEFILE_BLOCK = """
# -------------------------------
# Quality Mode Toggle Targets
# -------------------------------

MODE_FILE = config/quality_mode.txt

.PHONY: mode-strict
mode-strict:
\t@echo "strict" > $(MODE_FILE)
\t@echo "Switched to STRICT mode"

.PHONY: mode-balanced
mode-balanced:
\t@echo "balanced" > $(MODE_FILE)
\t@echo "Switched to BALANCED mode"

.PHONY: mode-show
mode-show:
\t@echo "Current mode: $$(cat $(MODE_FILE))"
"""

# Slack/Discord hook
SLACK_SNIPPET = """
# Slack/Discord notification (optional)
# Add your webhook URL to: config/webhook_url.txt

WEBHOOK_FILE = config/webhook_url.txt

.PHONY: notify-strict-failure
notify-strict-failure:
\t@if [ -f $(WEBHOOK_FILE) ]; then \\
\t  URL=$$(cat $(WEBHOOK_FILE)); \\
\t  curl -X POST -H 'Content-type: application/json' --data '{"text":"❌ STRICT MODE FAILURE detected in Super Doctor pipeline"}' $$URL; \\
\telse \\
\t  echo "No webhook configured"; \\
\tfi
"""

# Dashboard indicator
DASHBOARD_INDICATOR = """
<div id="quality-mode" style="margin-top:20px;padding:10px;border-radius:8px;background:#f6f8fa;border:1px solid #e1e4e8;">
  <h3>Quality Mode</h3>
  <p>This dashboard reflects the active CI enforcement mode stored in <code>config/quality_mode.txt</code>.</p>
  <p>The mode badge updates automatically based on this file.</p>
</div>
"""

# ---------------------------------------------------------
# Functions
# ---------------------------------------------------------

def ensure_mode_file():
    CONFIG_DIR.mkdir(exist_ok=True)
    if not MODE_FILE.exists():
        MODE_FILE.write_text("strict")
        print("[OK] Created config/quality_mode.txt (default: strict)")
    else:
        print("[OK] Mode file already exists")

def update_readme():
    text = README.read_text()
    if "## Quality Modes" not in text:
        README.write_text(text + "\n\n" + README_BLOCK)
        print("[OK] README updated with quality mode section")
    else:
        print("[OK] README already contains quality mode section")

def update_makefile():
    text = MAKEFILE.read_text()
    if "mode-strict" not in text:
        MAKEFILE.write_text(text + "\n\n" + MAKEFILE_BLOCK + "\n" + SLACK_SNIPPET)
        print("[OK] Makefile updated with mode toggles + Slack hook")
    else:
        print("[OK] Makefile already contains mode toggles")

def update_dashboard():
    if not DASHBOARD.exists():
        print("[WARN] dashboard.html not found — skipping dashboard update")
        return

    html = DASHBOARD.read_text()

    # Remove old indicator if present
    html = re.sub(r"<div id=\"quality-mode\".*?</div>", "", html, flags=re.DOTALL)

    # Insert before </body>
    html = html.replace("</body>", DASHBOARD_INDICATOR + "\n</body>")

    DASHBOARD.write_text(html)
    print("[OK] Dashboard updated with mode indicator")

# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():
    ensure_mode_file()
    update_readme()
    update_makefile()
    update_dashboard()
    print("\n🎉 Quality mode system fully installed.")

if __name__ == "__main__":
    main()
