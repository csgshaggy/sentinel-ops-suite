from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from app.ui.sidebar import sidebar
import functools
import inspect
import psutil
import html
import socket

router = APIRouter(prefix="/admin/cache", tags=["Cache"])


def find_lru_caches():
    """Find all functions in loaded modules that use functools.lru_cache."""
    caches = []
    for module in list(sys.modules.values()):
        if not module:
            continue
        for name, obj in inspect.getmembers(module):
            if hasattr(obj, "cache_info") and hasattr(obj, "cache_clear"):
                try:
                    info = obj.cache_info()
                    caches.append((f"{module.__name__}.{name}", obj, info))
                except Exception:
                    pass
    return caches


def get_dns_cache():
    """Try to read DNS resolver cache (platform dependent)."""
    try:
        # Python's socket resolver has no public cache, but we can show host lookups
        return "Python does not expose DNS cache directly"
    except Exception as e:
        return f"Error: {html.escape(str(e))}"


@router.get("/", response_class=HTMLResponse)
def cache_panel():
    lru_caches = find_lru_caches()
    dns_cache = get_dns_cache()

    # psutil caches
    psutil_cache = """
psutil caches are internal and refreshed automatically.
"""

    # Build table rows
    rows = ""
    for name, func, info in lru_caches:
        rows += f"""
        <tr>
            <td>{html.escape(name)}</td>
            <td>{info.hits}</td>
            <td>{info.misses}</td>
            <td>{info.currsize}</td>
            <td>{info.maxsize}</td>
            <td><a href="/admin/cache/clear?target={html.escape(name)}">Clear</a></td>
        </tr>
        """

    html_page = f"""
    <html>
    <head>
        <title>Cache Inspector</title>
        <meta http-equiv="refresh" content="15">
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
                vertical-align: top;
            }}
            tr:hover {{
                background: #f1f1f1;
            }}
            .metric {{
                background: white;
                padding: 20px;
                margin: 10px 0;
                border-radius: 8px;
            }}
        </style>
    </head>
    <body>
        {sidebar()}
        <div style="margin-left: 260px; padding: 20px;">
            <h1>🧠 Cache Inspector</h1>
            <p>Auto-refreshing every 15 seconds</p>

            <div class="metric">
                <h2>LRU Caches</h2>
                <table>
                    <tr>
                        <th>Function</th>
                        <th>Hits</th>
                        <th>Misses</th>
                        <th>Current Size</th>
                        <th>Max Size</th>
                        <th>Action</th>
                    </tr>
                    {rows}
                </table>
            </div>

            <div class="metric">
                <h2>psutil Cache</h2>
                <pre>{psutil_cache}</pre>
            </div>

            <div class="metric">
                <h2>DNS Resolver Cache</h2>
                <pre>{dns_cache}</pre>
            </div>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(html_page)


@router.get("/clear")
def clear_cache(target: str):
    """Clear a specific LRU cache."""
    for module in list(sys.modules.values()):
        if not module:
            continue
        for name, obj in inspect.getmembers(module):
            full = f"{module.__name__}.{name}"
            if full == target and hasattr(obj, "cache_clear"):
                obj.cache_clear()
                break

    return RedirectResponse("/admin/cache", status_code=302)
