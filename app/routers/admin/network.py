from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.ui.sidebar import sidebar
import psutil
import socket

router = APIRouter(prefix="/admin/network", tags=["Network"])


def get_ip_address(iface):
    """Return the IPv4 address for an interface if available."""
    addrs = psutil.net_if_addrs().get(iface, [])
    for addr in addrs:
        if addr.family == socket.AF_INET:
            return addr.address
    return "N/A"


def get_mac_address(iface):
    """Return the MAC address for an interface if available."""
    addrs = psutil.net_if_addrs().get(iface, [])
    for addr in addrs:
        if addr.family == psutil.AF_LINK:
            return addr.address
    return "N/A"


@router.get("/", response_class=HTMLResponse)
def network_panel():
    interfaces = psutil.net_if_stats()
    io_counters = psutil.net_io_counters(pernic=True)

    rows = ""

    for iface, stats in interfaces.items():
        ip = get_ip_address(iface)
        mac = get_mac_address(iface)
        io = io_counters.get(iface)

        rows += f"""
        <tr>
            <td>{iface}</td>
            <td>{'Up' if stats.isup else 'Down'}</td>
            <td>{ip}</td>
            <td>{mac}</td>
            <td>{io.bytes_sent / (1024 * 1024):.2f} MB</td>
            <td>{io.bytes_recv / (1024 * 1024):.2f} MB</td>
            <td>{io.packets_sent}</td>
            <td>{io.packets_recv}</td>
        </tr>
        """

    html_page = f"""
    <html>
    <head>
        <title>Network Panel</title>
        <meta http-equiv="refresh" content="5"> <!-- auto-refresh -->
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
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            th, td {{
                padding: 10px;
                border-bottom: 1px solid #ddd;
                text-align: left;
            }}
            th {{
                background: #333;
                color: white;
            }}
            tr:hover {{
                background: #f1f1f1;
            }}
            h1 {{
                color: #333;
            }}
        </style>
    </head>
    <body>
        {sidebar()}

        <div style="margin-left: 260px; padding: 20px;">
            <h1>🌐 Network Interface Panel</h1>
            <p>Auto-refreshing every 5 seconds</p>

            <table>
                <tr>
                    <th>Interface</th>
                    <th>Status</th>
                    <th>IPv4</th>
                    <th>MAC</th>
                    <th>Bytes Sent</th>
                    <th>Bytes Received</th>
                    <th>Packets Sent</th>
                    <th>Packets Received</th>
                </tr>
                {rows}
            </table>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(html_page)
