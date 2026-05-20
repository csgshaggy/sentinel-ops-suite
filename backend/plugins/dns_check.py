from __future__ import annotations

import socket
import time

NAME = "DNS Check"
CATEGORY = "network"
AVG_DURATION = 20
LAST_RUN = None

TARGET_HOST = "example.com"


async def run():
    """
    Resolve a hostname and measure resolution time.
    """
    global LAST_RUN

    start = time.time()
    ip = socket.gethostbyname(TARGET_HOST)
    duration = int((time.time() - start) * 1000)

    LAST_RUN = time.strftime("%Y-%m-%dT%H:%M:%S")

    return {
        "host": TARGET_HOST,
        "ip": ip,
        "duration_ms": duration,
    }
