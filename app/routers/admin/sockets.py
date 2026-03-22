from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.ui.sidebar import sidebar
import psutil
import html

router = APIRouter(prefix="/admin/sockets", tags=["Sockets"])


def format_addr(addr):
    if not addr:
        return ""
    try:
        return f"{addr.ip}:{addr.port}"
    except:
        return str(addr)


@router.get("/", response_class=HTMLResponse)
def sockets_panel():
    conns = psutil.net_connections(kind="inet")
    unix_conns = psutil.net_connections(kind="unix")

    rows = ""
    for c in conns:
        laddr = format_addr(c.laddr)
        raddr = format_addr(c.raddr)
        pid = c.pid or ""
        proc_name = ""

        if pid:
            try:
                proc_name = psutil.Process(pid).name()
            except:
                proc_name = "unknown"

        rows += f"""
        <tr>
            <td>{html.escape(c.type.name)}</td>
            <td>{html.escape(c.status)}</td>
            <td>{html.escape(laddr)}</td>
            <td>{html.escape(raddr)}</td>
            <td>{pid}</td>
            <td>{html.escape(proc_name)}</td>
        </tr>
        """

    unix_rows = ""
    for c in unix_conns:
        pid = c.pid or ""
        proc_name = ""

        if pid:
            try:
                proc_name = psutil.Process(pid).name()
            except:
                proc_name = "unknown"

        unix_rows += f"""
        <tr>
            <td>{html.escape(c.laddr or '')}</td>
            <td>{pid}</td>
            <td>{html.escape(proc_name)}</td>
        </tr>
        """

    html_page = f"""
    <html>
    <head>
        <title>Socket Inspector</title>
        <meta http-equiv="refresh" content="10">
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
            h2 {{
                margin-top: 40px;
            }}
        </style>
    </head>
    <body>
        {sidebar()}
        <div style="margin-left: 260px; padding: 20px;">
            <h1>🔌 Socket Inspector</h1>
            <p>Auto-refreshing every 10 seconds</p>

            <h2>INET Sockets (TCP/UDP)</h2>
            <table>
                <tr>
                    <th>Type</th>
                    <th>Status</th>
                    <th>Local Address</th>
                    <th>Remote Address</th>
                    <th>PID</th>
                    <th>Process</th>
                </tr>
                {rows}
            </table>

            <h2>UNIX Domain Sockets</h2>
            <table>
                <tr>
                    <th>Path</th>
                    <th>PID</th>
                    <th>Process</th>
                </tr>
                {unix_rows}
            </table>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(html_page)
