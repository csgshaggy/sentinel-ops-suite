from __future__ import annotations

import time
import aiohttp

NAME = "SSRF Basic Probe"
CATEGORY = "security"
AVG_DURATION = 80
LAST_RUN = None

TARGETS = [
    "http://127.0.0.1:80",
    "http://169.254.169.254/latest/meta-data/",
]


async def run():
    """
    Perform SSRF-style GET requests against a list of targets.
    """
    global LAST_RUN

    start = time.time()
    results = []

    async with aiohttp.ClientSession() as session:
        for url in TARGETS:
            try:
                async with session.get(url, timeout=2) as resp:
                    body = await resp.text()
                    results.append(
                        {
                            "url": url,
                            "status": resp.status,
                            "body_sample": body[:200],
                        }
                    )
            except Exception as exc:
                results.append({"url": url, "error": str(exc)})

    duration = int((time.time() - start) * 1000)
    LAST_RUN = time.strftime("%Y-%m-%dT%H:%M:%S")

    return {
        "targets": TARGETS,
        "results": results,
        "duration_ms": duration,
    }
