def format_markdown(drift):
    lines = []
    lines.append("## 🧭 Structure Drift Report")
    lines.append("")

    if drift["new_paths"]:
        lines.append("### 🟩 New Paths")
        for p in drift["new_paths"]:
            lines.append(f"- `+ {p}`")
        lines.append("")

    if drift["missing_paths"]:
        lines.append("### 🟥 Missing Paths")
        for p in drift["missing_paths"]:
            lines.append(f"- `- {p}`")
        lines.append("")

    if drift["modified_files"]:
        lines.append("### 🟨 Modified Files")
        for p in drift["modified_files"]:
            lines.append(f"- `* {p}`")
        lines.append("")

    if not any(drift.values()):
        lines.append("### ✔️ No drift detected")
        lines.append("Everything matches the baseline.")

    return "\n".join(lines)
