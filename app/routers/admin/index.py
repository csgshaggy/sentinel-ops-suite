from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.ui.sidebar import sidebar

router = APIRouter(prefix="/admin/index", tags=["Admin Index"])


SECTIONS = {
    "System Overview": [
        ("Home", "/admin/home"),
        ("System", "/admin/system"),
        ("Processes", "/admin/processes"),
        ("Network", "/admin/network"),
        ("Services", "/admin/services"),
        ("Firewall", "/admin/firewall"),
        ("Users", "/admin/users"),
        ("Storage", "/admin/storage"),
        ("Boot", "/admin/boot"),
        ("Hardware", "/admin/hardware"),
        ("Kernel", "/admin/kernel"),
        ("Packages", "/admin/packages"),
    ],

    "Runtime & Environment": [
        ("Runtime", "/admin/runtime"),
        ("Environment", "/admin/env"),
        ("Limits", "/admin/limits"),
        ("Paths", "/admin/paths"),
        ("Config", "/admin/config"),
        ("Performance", "/admin/performance"),
        ("Health", "/admin/health"),
    ],

    "Threads & Concurrency": [
        ("Threads", "/admin/threads"),
        ("Deadlock Inspector", "/admin/threads/deadlock"),
        ("Locks", "/admin/locks"),
        ("Timers", "/admin/timers"),
        ("AsyncIO", "/admin/async"),
    ],

    "Diagnostics & Forensics": [
        ("Logs", "/admin/logs"),
        ("Events", "/admin/events"),
        ("Audit", "/admin/audit"),
        ("Metrics", "/admin/metrics"),
        ("Tasks", "/admin/tasks"),
        ("Scheduler", "/admin/scheduler"),
        ("Inspect Object", "/admin/inspect"),
        ("Cache", "/admin/cache"),
        ("Sockets", "/admin/sockets"),
        ("Signals", "/admin/signals"),
    ],
}


@router.get("/", response_class=HTMLResponse)
def admin_index():
    # Build section HTML
    section_html = ""
    for section, items in SECTIONS.items():
        links = "".join(
            f'<li><a href="{url}" style="color:#4ea1ff;text-decoration:none;">{name}</a></li>'
            for name, url in items
        )

        section_html += f"""
        <div style="background:white;padding:20px;margin:20px 0;border-radius:8px;">
            <h2>{section}</h2>
            <ul style="line-height:1.8;font-size:16px;">
                {links}
            </ul>
        </div>
        """

    html_page = f"""
    <html>
    <head>
        <title>Admin Index</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f4f4f4;
                margin: 0;
            }}
            h1 {{
                margin-bottom: 10px;
            }}
            h2 {{
                margin-top: 0;
            }}
            ul {{
                list-style-type: none;
                padding-left: 0;
            }}
            li {{
                margin: 6px 0;
            }}
        </style>
    </head>
    <body>
        {sidebar()}
        <div style="margin-left:260px;padding:20px;">
            <h1>📊 Admin Control Center</h1>
            <p>Full operational overview of the system, runtime, diagnostics, and concurrency layers.</p>

            {section_html}
        </div>
    </body>
    </html>
    """

    return HTMLResponse(html_page)
