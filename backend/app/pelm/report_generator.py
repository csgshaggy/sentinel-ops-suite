"""
PELM Report Generator
Produces HTML and Markdown reports for snapshots, drift, regression,
and canonical status.

This implementation:
- Never crashes the backend
- Uses simple templates stored in report_templates/
- Produces clean, readable output for dashboards or downloads
"""

import os
from typing import Dict, Any

from .pelm_tools import safe_json_dumps, utc_now


TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "report_templates")
HTML_TEMPLATE_PATH = os.path.join(TEMPLATE_DIR, "html_template.html")
MD_TEMPLATE_PATH = os.path.join(TEMPLATE_DIR, "markdown_template.md")


def _load_template(path: str) -> str:
    """Load a template file safely."""
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception:
        return "<html><body><pre>{{content}}</pre></body></html>"


def generate_html_report(data: Dict[str, Any]) -> str:
    """
    Generate an HTML report using the template.
    """
    template = _load_template(HTML_TEMPLATE_PATH)

    return template.replace("{{timestamp}}", utc_now()) \
                   .replace("{{content}}", safe_json_dumps(data))


def generate_markdown_report(data: Dict[str, Any]) -> str:
    """
    Generate a Markdown report using the template.
    """
    template = _load_template(MD_TEMPLATE_PATH)

    return template.replace("{{timestamp}}", utc_now()) \
                   .replace("{{content}}", safe_json_dumps(data))


def generate_pelm_report(
    snapshot: Dict[str, Any],
    regression: Dict[str, Any],
    drift: Dict[str, Any],
    canonical: Dict[str, Any]
) -> Dict[str, str]:
    """
    Generate both HTML and Markdown PELM reports.
    Returns a dict containing both formats.
    """

    combined = {
        "snapshot": snapshot,
        "regression": regression,
        "drift": drift,
        "canonical": canonical,
        "generated_at": utc_now(),
    }

    return {
        "html": generate_html_report(combined),
        "markdown": generate_markdown_report(combined),
    }
