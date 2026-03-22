from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.ui.sidebar import sidebar
import importlib
import inspect
import html

router = APIRouter(prefix="/admin/inspect", tags=["Inspect"])


def safe_import(path: str):
    """Import an object from a dotted path like 'os.path.join'."""
    try:
        parts = path.split(".")
        module_path = ".".join(parts[:-1])
        attr = parts[-1]

        module = importlib.import_module(module_path)
        obj = getattr(module, attr)
        return obj, None
    except Exception as e:
        return None, str(e)


def inspect_object(obj):
    """Return a dict of inspection details for an object."""
    info = {}

    try:
        info["type"] = html.escape(str(type(obj)))
    except:
        info["type"] = "Unavailable"

    try:
        info["module"] = html.escape(str(obj.__module__))
    except:
        info["module"] = "Unavailable"

    try:
        info["doc"] = html.escape(inspect.getdoc(obj) or "No docstring")
    except:
        info["doc"] = "Unavailable"

    try:
        if inspect.isfunction(obj) or inspect.ismethod(obj) or inspect.isclass(obj):
            info["signature"] = html.escape(str(inspect.signature(obj)))
        else:
            info["signature"] = "Not callable"
    except:
        info["signature"] = "Unavailable"

    try:
        source = inspect.getsource(obj)
        info["source"] = html.escape(source)
    except:
        info["source"] = "Source unavailable"

    try:
        attrs = dir(obj)
        info["attributes"] = "<br>".join(html.escape(a) for a in attrs)
    except:
        info["attributes"] = "Unavailable"

    return info


@router.get("/", response_class=HTMLResponse)
def inspect_panel(obj: str = None):
    if obj:
        inspected_obj, error = safe_import(obj)
        if inspected_obj:
            info = inspect_object(inspected_obj)
        else:
            info = {"error": html.escape(error)}
    else:
        info = None

    html_page = f"""
    <html>
    <head>
        <title>Object Inspector</title>
        <meta http-equiv="refresh" content="20">
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f4f4f4;
                margin: 0;
            }}
            pre {{
                background: #000;
                color: #0f0;
                padding: 20px;
                border-radius: 8px;
                overflow-x: auto;
                white-space: pre-wrap;
                font-size: 14px;
                max-height: 40vh;
            }}
            .metric {{
                background: white;
                padding: 20px;
                margin: 10px 0;
                border-radius: 8px;
            }}
            input {{
                width: 400px;
                padding: 10px;
                font-size: 16px;
            }}
            button {{
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
            }}
        </style>
    </head>
    <body>
        {sidebar()}
        <div style="margin-left: 260px; padding: 20px;">
            <h1>🔍 Python Object Inspector</h1>
            <p>Auto-refreshing every 20 seconds</p>

            <form method="get">
                <input type="text" name="obj" placeholder="e.g. os.path.join" value="{obj or ''}">
                <button type="submit">Inspect</button>
            </form>

            {"<h2>Inspection Results</h2>" if info else ""}

            {"<div class='metric'><h3>Error</h3><pre>" + info.get("error", "") + "</pre></div>" if info and "error" in info else ""}

            {"<div class='metric'><h3>Type</h3><pre>" + info.get("type", "") + "</pre></div>" if info else ""}
            {"<div class='metric'><h3>Module</h3><pre>" + info.get("module", "") + "</pre></div>" if info else ""}
            {"<div class='metric'><h3>Signature</h3><pre>" + info.get("signature", "") + "</pre></div>" if info else ""}
            {"<div class='metric'><h3>Docstring</h3><pre>" + info.get("doc", "") + "</pre></div>" if info else ""}
            {"<div class='metric'><h3>Attributes</h3><pre>" + info.get("attributes", "") + "</pre></div>" if info else ""}
            {"<div class='metric'><h3>Source Code</h3><pre>" + info.get("source", "") + "</pre></div>" if info else ""}
        </div>
    </body>
    </html>
    """

    return HTMLResponse(html_page)
