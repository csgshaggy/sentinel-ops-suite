from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path
import json
import markdown

router = APIRouter(prefix="/admin/docs", tags=["Documentation"])

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DOCS_DIR = PROJECT_ROOT / "docs"
MAP_FILE = DOCS_DIR / "category_map.json"
SEARCH_INDEX = PROJECT_ROOT / "docs_search_index.json"
SITE_DIR = PROJECT_ROOT / "docs_site"


# ---------------------------------------------------------
# Dashboard
# ---------------------------------------------------------
@router.get("/dashboard")
def docs_dashboard():
    from scripts.docs_dashboard import main as dashboard_main
    import io, sys

    buf = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = buf

    dashboard_main()

    sys.stdout = sys_stdout
    return HTMLResponse(f"<pre>{buf.getvalue()}</pre>")


# ---------------------------------------------------------
# Search
# ---------------------------------------------------------
@router.get("/search")
def docs_search(q: str):
    if not SEARCH_INDEX.exists():
        raise HTTPException(500, "Search index missing. Run make docs.search")

    index = json.loads(SEARCH_INDEX.read_text())
    q_lower = q.lower()

    results = []
    for entry in index:
        if q_lower in entry["content"].lower() or q_lower in entry["title"].lower():
            results.append({
                "file": entry["file"],
                "title": entry["title"],
                "snippet": entry["content"][:200] + "..."
            })

    return JSONResponse(results)


# ---------------------------------------------------------
# View Markdown as HTML
# ---------------------------------------------------------
@router.get("/view/{category}/{file}", response_class=HTMLResponse)
def view_doc(category: str, file: str):
    md_path = DOCS_DIR / category / file
    if not md_path.exists():
        raise HTTPException(404, "Document not found")

    md_text = md_path.read_text()
    html = markdown.markdown(md_text)

    return f"<h1>{file}</h1>{html}"


# ---------------------------------------------------------
# Health Score
# ---------------------------------------------------------
@router.get("/health")
def docs_health():
    from scripts.docs_health import main as health_main
    import io, sys

    buf = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = buf

    try:
        health_main()
    except SystemExit:
        pass

    sys.stdout = sys_stdout
    return HTMLResponse(f"<pre>{buf.getvalue()}</pre>")


# ---------------------------------------------------------
# Drift Diff
# ---------------------------------------------------------
@router.get("/diff")
def docs_diff():
    from scripts.docs_diff import main as diff_main
    import io, sys

    buf = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = buf

    diff_main()

    sys.stdout = sys_stdout
    return HTMLResponse(f"<pre>{buf.getvalue()}</pre>")


# ---------------------------------------------------------
# Serve static HTML site
# ---------------------------------------------------------
@router.get("/site/{path:path}", response_class=HTMLResponse)
def serve_site(path: str):
    file_path = SITE_DIR / path
    if not file_path.exists():
        raise HTTPException(404, "Page not found")

    return file_path.read_text()
