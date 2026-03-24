from __future__ import annotations

import time
import aiohttp

NAME = "SSRF Header Probe"
CATEGORY = "security"
AVG_DURATION = 90
LAST_RUN = None

TARGET_URL = "http://127.0.0.1:5001/system/health"

HEADERS = {
    "X-Forwarded-For": "127.0.0.1",
    "X-Original-URL": "http://169.254.169.254/latest/meta-data/",
}


async def run():
    """
    Perform an SSRF-style probe using crafted headers.
    """
    global LAST_RUN

    start = time.time()

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(TARGET_URL, headers=HEADERS, timeout=3) as resp:
                body = await resp.text()
                result = {
                    "target": TARGET_URL,
                    "status": resp.status,
                    "body_sample": body[:200],
                    "sent_headers": HEADERS,
                }
        except Exception as exc:
            result = {
                "target": TARGET_URL,
                "error": str(exc),
                "sent_headers": HEADERS,
            }

    duration = int((time.time() - start) * 1000)
    LAST_RUN = time.strftime("%Y-%m-%dT%H:%M:%S")

    return {
        "result": result,
        "duration_ms": duration,
    }
