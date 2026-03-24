from __future__ import annotations

import time
import aiohttp

NAME = "HTTP Probe"
CATEGORY = "network"
AVG_DURATION = 50
LAST_RUN = None

TARGET_URL = "http://127.0.0.1:5001/system/health"


async def run():
    """
    Perform an HTTP GET request and return timing + sample body.
    """
    global LAST_RUN

    start = time.time()

    async with aiohttp.ClientSession() as session:
        async with session.get(TARGET_URL, timeout=3) as resp:
            body = await resp.text()

    duration = int((time.time() - start) * 1000)
    LAST_RUN = time.strftime("%Y-%m-%dT%H:%M:%S")

    return {
        "target": TARGET_URL,
        "status": resp.status,
        "duration_ms": duration,
        "body_sample": body[:200],
    }
