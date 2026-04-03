from __future__ import annotations

import socket
from typing import Any, Dict, List

from fastapi import APIRouter

router = APIRouter(prefix="/admin/sockets", tags=["admin-sockets"])


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------


def _safe_socket_info(sock: socket.socket) -> Dict[str, Any]:
    """
    Safely extract socket information without risking exceptions.
    """
    info: Dict[str, Any] = {
        "family": str(sock.family),
        "type": str(sock.type),
        "proto": sock.proto,
    }

    try:
        info["local_address"] = sock.getsockname()
    except Exception:
        info["local_address"] = "<unavailable>"

    try:
        info["remote_address"] = sock.getpeername()
    except Exception:
        info["remote_address"] = "<unconnected>"

    return info


def _list_active_sockets() -> List[Dict[str, Any]]:
    """
    Enumerate active sockets for diagnostic purposes.
    This does NOT attempt to inspect OS-level sockets — only Python-level ones.
    """
    sockets: List[Dict[str, Any]] = []

    for obj in (
        socket._socketobject.__subclasses__()
        if hasattr(socket, "_socketobject")
        else []
    ):
        # Legacy fallback — modern Python doesn't expose this
        pass

    # Python does not expose a global registry of sockets.
    # Instead, we provide a safe, minimal diagnostic endpoint.
    return sockets


# ------------------------------------------------------------
# API Endpoints
# ------------------------------------------------------------


@router.get("/diagnostic", summary="Return basic socket subsystem diagnostics")
def socket_diagnostic() -> Dict[str, Any]:
    """
    Provide a high-level view of the Python socket subsystem.
    This does NOT enumerate OS-level sockets (requires elevated privileges).
    """
    return {
        "default_timeout": socket.getdefaulttimeout(),
        "hostname": socket.gethostname(),
        "family_constants": {
            "AF_INET": socket.AF_INET,
            "AF_INET6": socket.AF_INET6,
            "AF_UNIX": getattr(socket, "AF_UNIX", None),
        },
        "type_constants": {
            "SOCK_STREAM": socket.SOCK_STREAM,
            "SOCK_DGRAM": socket.SOCK_DGRAM,
        },
    }


@router.get("/resolve/{hostname}", summary="Resolve a hostname to IP addresses")
def resolve_hostname(hostname: str) -> Dict[str, Any]:
    """
    Resolve a hostname safely.
    """
    try:
        results = socket.getaddrinfo(hostname, None)
    except Exception as exc:
        return {
            "success": False,
            "hostname": hostname,
            "error": str(exc),
        }

    addresses = sorted({item[4][0] for item in results})

    return {
        "success": True,
        "hostname": hostname,
        "addresses": addresses,
    }


@router.get("/test/{host}/{port}", summary="Test TCP connectivity (non-blocking)")
def test_connectivity(host: str, port: int) -> Dict[str, Any]:
    """
    Perform a safe, non-blocking TCP connectivity test.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)

    try:
        result = sock.connect_ex((host, port))
    except Exception as exc:
        return {
            "success": False,
            "host": host,
            "port": port,
            "error": str(exc),
        }
    finally:
        sock.close()

    return {
        "success": result == 0,
        "host": host,
        "port": port,
        "result_code": result,
    }
