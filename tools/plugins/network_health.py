"""
SuperDoctor Plugin: Network Health & Connectivity
Location: tools/plugins/network_health.py

Checks:
- DNS resolution (A/AAAA best-effort)
- Outbound connectivity to common endpoints
- Localhost binding test (TCP)
- Latency sampling (best-effort)
- Cross-platform safe (Windows + Linux)
"""

import socket
import time
from typing import List, Optional

from tools.super_doctor import CheckResult
from utils.modes import Mode

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------


def _dns_lookup(host: str) -> Optional[List[str]]:
    """
    Resolve DNS for a hostname.
    Returns list of IPs or None.
    """
    try:
        infos = socket.getaddrinfo(host, None)
        addrs = list({info[4][0] for info in infos})
        return addrs
    except Exception:
        return None


def _tcp_connect(host: str, port: int, timeout: float = 2.0) -> bool:
    """
    Attempt a TCP connection.
    """
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False


def _latency(host: str, port: int = 80, timeout: float = 2.0) -> Optional[float]:
    """
    Best-effort latency measurement using TCP connect timing.
    """
    start = time.time()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return (time.time() - start) * 1000.0
    except Exception:
        return None


def _localhost_bind_test() -> bool:
    """
    Ensure localhost can bind a TCP port.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("127.0.0.1", 0))  # OS assigns free port
        s.close()
        return True
    except Exception:
        return False


# ------------------------------------------------------------
# Main plugin
# ------------------------------------------------------------


def run_checks(mode: Mode, project_root=None) -> List[CheckResult]:
    results: List[CheckResult] = []

    # ------------------------------------------------------------
    # 1. DNS resolution
    # ------------------------------------------------------------
    test_hosts = ["example.com", "google.com", "cloudflare.com"]

    for host in test_hosts:
        addrs = _dns_lookup(host)
        if addrs is None:
            results.append(
                CheckResult(
                    id=f"dns.{host}.fail",
                    name=f"DNS resolution failed: {host}",
                    description=f"Could not resolve DNS for {host}.",
                    status="fail",
                    severity="high",
                    plugin="network_health",
                )
            )
        else:
            results.append(
                CheckResult(
                    id=f"dns.{host}.ok",
                    name=f"DNS resolution OK: {host}",
                    description=f"Resolved {host} successfully.",
                    status="ok",
                    severity="info",
                    details=", ".join(addrs),
                    plugin="network_health",
                )
            )

    # ------------------------------------------------------------
    # 2. Outbound connectivity tests
    # ------------------------------------------------------------
    endpoints = [
        ("example.com", 80),
        ("google.com", 80),
        ("cloudflare.com", 80),
    ]

    for host, port in endpoints:
        ok = _tcp_connect(host, port)
        if not ok:
            results.append(
                CheckResult(
                    id=f"net.{host}.fail",
                    name=f"Outbound connectivity failed: {host}:{port}",
                    description=f"Could not connect to {host}:{port}.",
                    status="fail",
                    severity="high",
                    plugin="network_health",
                )
            )
        else:
            results.append(
                CheckResult(
                    id=f"net.{host}.ok",
                    name=f"Outbound connectivity OK: {host}:{port}",
                    description=f"Successfully connected to {host}:{port}.",
                    status="ok",
                    severity="info",
                    plugin="network_health",
                )
            )

    # ------------------------------------------------------------
    # 3. Latency sampling
    # ------------------------------------------------------------
    latency = _latency("example.com", 80)

    if latency is None:
        results.append(
            CheckResult(
                id="latency.example.fail",
                name="Latency measurement failed",
                description="Could not measure latency to example.com.",
                status="warn",
                severity="medium",
                plugin="network_health",
            )
        )
    else:
        results.append(
            CheckResult(
                id="latency.example.ok",
                name="Latency OK",
                description="Measured latency to example.com.",
                status="ok",
                severity="info",
                details=f"{latency:.1f} ms",
                plugin="network_health",
            )
        )

        # High latency warnings
        if latency > 500:
            results.append(
                CheckResult(
                    id="latency.high",
                    name="High network latency",
                    description="Latency exceeds 500 ms.",
                    status="warn",
                    severity="high",
                    plugin="network_health",
                )
            )
        elif latency > 200:
            results.append(
                CheckResult(
                    id="latency.moderate",
                    name="Moderate network latency",
                    description="Latency exceeds 200 ms.",
                    status="warn",
                    severity="medium",
                    plugin="network_health",
                )
            )

    # ------------------------------------------------------------
    # 4. Localhost binding
    # ------------------------------------------------------------
    if _localhost_bind_test():
        results.append(
            CheckResult(
                id="localhost.bind.ok",
                name="Localhost binding OK",
                description="Successfully bound a TCP port on localhost.",
                status="ok",
                severity="info",
                plugin="network_health",
            )
        )
    else:
        results.append(
            CheckResult(
                id="localhost.bind.fail",
                name="Localhost binding failed",
                description="Could not bind a TCP port on localhost.",
                status="fail",
                severity="critical",
                plugin="network_health",
            )
        )

    return results
