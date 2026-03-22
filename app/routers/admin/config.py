from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.ui.sidebar import sidebar
import importlib.metadata
import html

router = APIRouter(prefix="/admin/config", tags=["Config"])


def get_installed_packages():
    """Return a list of (name, version) tuples using importlib.metadata."""
    packages = []
    for dist in importlib.metadata.distributions():
        name = dist.metadata.get("Name", dist.metadata.get("Summary", "Unknown"))
        version = dist.version or "Unknown"
        packages.append((name, version))
    return sorted(packages, key=lambda x: x[0].lower())


@router.get("/", response_class=HTMLResponse)
def config_panel():
    packages = get_installed_packages()

    rows = ""
    for name, version in packages:
        rows += f"""
        <tr>
            <td>{html.escape(name)}</td>
            <td>{html.escape(version)}</td>
        </tr>
        """

    html_page = f"""
    <html>
    <head>
        <title>Installed Packages</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f4f4f4;
                margin: 0;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                background: white;
            }}
            th {{
                background: #333;
                color: white;
            }}
            th, td {{
                padding: 10px;
                border-bottom: 1px solid #ddd;
            }}
            tr:hover {{
                background: #f1f1f1;
            }}
        </style>
    </head>
    <body>
        {sidebar()}
        <div style="margin-left:260px;padding:20px;">
            <h1>📦 Installed Python Packages</h1>
            <p>Using importlib.metadata (Python 3.13 compatible)</p>

            <table>
                <tr>
                    <th>Package</th>
                    <th>Version</th>
                </tr>
                {rows}
            </table>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(html_page)
