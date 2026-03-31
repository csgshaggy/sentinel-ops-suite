"""
Virtualization plugin (sync).

Detects whether the system is running inside:
- a virtual machine (KVM, VMware, Hyper‑V, VirtualBox, QEMU)
- a container (Docker, LXC, Podman)
- bare metal

Forms the foundation for:
- environment‑aware baselining
- container vs VM vs host policy enforcement
- CI drift detection across execution environments
"""

from __future__ import annotations

import os
import subprocess
import time
from typing import Any, Dict

from tools.super_doctor import CheckResult, Status
from utils.modes import Mode

PLUGIN_INFO: Dict[str, Any] = {
    "name": __name__.split(".")[-1],
    "description": "Detects virtualization/containerization environment.",
    "entrypoint": "run",
    "mode": "sync",
}


def _run_cmd(cmd: list[str]) -> str:
    """
    Safely run a command and return stdout as text.
    """
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
        return out.decode().strip()
    except Exception:
        return ""


def _detect_container() -> str | None:
    """
    Detect common container environments.
    """
    # Docker / containerd
    if os.path.exists("/.dockerenv"):
        return "docker"

    # Podman / LXC / generic container
    cgroup = ""
    try:
        with open("/proc/1/cgroup", "r") as f:
            cgroup = f.read()
    except Exception:
        pass

    if "docker" in cgroup:
        return "docker"
    if "kubepods" in cgroup:
        return "kubernetes"
    if "lxc" in cgroup:
        return "lxc"
    if "podman" in cgroup:
        return "podman"

    return None


def _detect_vm() -> str | None:
    """
    Detect virtualization using systemd-detect-virt or fallback heuristics.
    """
    out = _run_cmd(["systemd-detect-virt", "--vm"])
    if out and out != "none":
        return out.strip()

    # Fallback: check DMI data
    dmi = _run_cmd(["dmidecode", "-s", "system-product-name"])
    if dmi:
        lower = dmi.lower()
        if "kvm" in lower:
            return "kvm"
        if "virtualbox" in lower:
            return "virtualbox"
        if "vmware" in lower:
            return "vmware"
        if "hyper-v" in lower:
            return "hyper-v"
        if "qemu" in lower:
            return "qemu"

    return None


def run(mode: Mode = Mode.FAST) -> CheckResult:
    """
    Synchronous virtualization/containerization detection.
    """
    try:
        container = _detect_container()
        vm = _detect_vm()

        if container:
            env = "container"
            env_type = container
            status = Status.OK
            message = f"Container environment detected: {container}"
        elif vm:
            env = "virtual_machine"
            env_type = vm
            status = Status.OK
            message = f"Virtual machine detected: {vm}"
        else:
            env = "bare_metal"
            env_type = None
            status = Status.OK
            message = "Running on bare metal."

        data = {
            "environment": env,
            "type": env_type,
            "mode": mode.value,
            "timestamp": time.time(),
        }

        return CheckResult(
            name=PLUGIN_INFO["name"],
            status=status,
            message=message,
            data=data,
        )

    except Exception as exc:
        return CheckResult.fail(
            name=PLUGIN_INFO["name"],
            message=f"Virtualization plugin failed: {exc}",
        )
