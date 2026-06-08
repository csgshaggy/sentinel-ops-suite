#!/usr/bin/env python3
import os
import re
from pathlib import Path

ROOT = Path("src")

FILES = [
    "components/SessionManager.jsx",
    "hooks/useHeartbeat.js",
    "hooks/useSession.js",
    "api/apiClient.js",
    "features/auth/AuthContext.jsx",
    "pages/Dashboard.jsx",
    "pages/Preferences.jsx",
    "pages/Profile/components/tabs/AvatarTab.jsx",
    "pages/Profile/components/tabs/ApiKeysTab.jsx",
    "pages/Profile/components/tabs/LoginHistoryTab.jsx",
]

OPTIONAL_FILES = [
    "components/Sidebar.jsx",
    "components/TopBar.jsx",
    "App.jsx",
]

IMPORT_LINE = 'import { Telemetry } from "../telemetry/telemetry";\n'

TELEMETRY_CALLS = {
    "components/SessionManager.jsx":
        ('catch (err)', 'Telemetry.session("restore.failure", { error: err.message }, "SessionManager");'),
    "hooks/useHeartbeat.js":
        ('catch (err)', 'Telemetry.heartbeat("failure", { error: err.message }, "useHeartbeat");'),
    "hooks/useSession.js":
        ('catch (err)', 'Telemetry.session("restore.failure", { error: err.message }, "useSession");'),
    "api/apiClient.js":
        ('axios.interceptors.response.use', 'Telemetry.api("response.failure", { status: error?.response?.status }, "apiClient");'),
    "features/auth/AuthContext.jsx":
        ('catch (err)', 'Telemetry.sec("login.failure", { error: err.message }, "AuthContext");'),
    "pages/Dashboard.jsx":
        ('useEffect', 'Telemetry.perf("page_load", {}, "Dashboard");'),
    "pages/Preferences.jsx":
        ('handleSave', 'Telemetry.ui("submit", { form: "preferences" }, "Preferences");'),
    "pages/Profile/components/tabs/AvatarTab.jsx":
        ('catch (err)', 'Telemetry.ui("submit", { action: "avatar_upload" }, "AvatarTab");'),
    "pages/Profile/components/tabs/ApiKeysTab.jsx":
        ('catch (err)', 'Telemetry.ui("click", { action: "copy_api_key" }, "ApiKeysTab");'),
    "pages/Profile/components/tabs/LoginHistoryTab.jsx":
        ('catch (err)', 'Telemetry.ui("load", { action: "login_history" }, "LoginHistoryTab");'),
}


def inject_import(file_path: Path):
    """Insert telemetry import after first import statement."""
    content = file_path.read_text().splitlines(keepends=True)

    if any("Telemetry" in line for line in content):
        print(f"[SKIP] Import already present: {file_path}")
        return

    new_content = []
    inserted = False

    for line in content:
        new_content.append(line)
        if not inserted and line.strip().startswith("import"):
            new_content.append(IMPORT_LINE)
            inserted = True

    file_path.write_text("".join(new_content))
    print(f"[OK] Added telemetry import → {file_path}")


def inject_call(file_path: Path, anchor: str, call: str):
    """Insert telemetry call after anchor line."""
    content = file_path.read_text().splitlines(keepends=True)

    if any(call in line for line in content):
        print(f"[SKIP] Telemetry call already present: {file_path}")
        return

    new_content = []
    inserted = False

    for line in content:
        new_content.append(line)
        if not inserted and anchor in line:
            new_content.append(f"    {call}\n")
            inserted = True

    file_path.write_text("".join(new_content))
    print(f"[OK] Inserted telemetry call → {file_path}")


def main():
    print("=== Python Telemetry Injection Script ===\n")

    all_files = FILES + OPTIONAL_FILES

    for rel_path in all_files:
        file_path = ROOT / rel_path
        if not file_path.exists():
            print(f"[MISS] File not found: {file_path}")
            continue

        inject_import(file_path)

        if rel_path in TELEMETRY_CALLS:
            anchor, call = TELEMETRY_CALLS[rel_path]
            inject_call(file_path, anchor, call)

    print("\n=== Telemetry injection complete ===")


if __name__ == "__main__":
    main()
