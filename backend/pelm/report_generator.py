from datetime import datetime
from pathlib import Path
import json

HTML_TEMPLATE_PATH = Path("backend/pelm/report_templates/html_template.html")
MD_TEMPLATE_PATH = Path("backend/pelm/report_templates/markdown_template.md")


def generate_html_report(output, drift, regression, snapshots, contract):
    template = HTML_TEMPLATE_PATH.read_text()

    return template.format(
        title="Sentinel Compliance Report — PELM Operator Report",
        timestamp=datetime.utcnow().isoformat(),
        risk=output.get("risk"),
        status=output.get("status"),
        signals=json.dumps(output.get("signals", {}), indent=2),
        metadata=json.dumps(output.get("metadata", {}), indent=2),
        drift=json.dumps(drift, indent=2),
        regression=json.dumps(regression, indent=2),
        contract=json.dumps(contract, indent=2),
        snapshots=json.dumps(snapshots, indent=2),
    )


def generate_markdown_report(output, drift, regression, snapshots, contract):
    template = MD_TEMPLATE_PATH.read_text()

    return template.format(
        timestamp=datetime.utcnow().isoformat(),
        risk=output.get("risk"),
        status=output.get("status"),
        signals=json.dumps(output.get("signals", {}), indent=2),
        metadata=json.dumps(output.get("metadata", {}), indent=2),
        drift=json.dumps(drift, indent=2),
        regression=json.dumps(regression, indent=2),
        contract=json.dumps(contract, indent=2),
        snapshots=json.dumps(snapshots, indent=2),
    )
