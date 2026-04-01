# tools/security/idrim/outputs/idrim_reporter.py

import json
import sys


class IDRIMReporter:
    """
    Emits IDRIM drift events to various output channels.

    Responsibilities:
    - Emit events to console (dev mode)
    - Append events to audit log
    - Forward events to anomaly subsystem (future integration)
    - Provide a clean, deterministic output pipeline

    Event input MUST be a dictionary produced by DriftAnalyzer.
    """

    def __init__(self, audit_log_path="idrim_audit.log"):
        self.audit_log_path = audit_log_path

    def emit(self, event):
        """
        Main entrypoint for emitting a drift event.
        """
        self._emit_console(event)
        self._emit_audit_log(event)
        # Future integrations:
        # self._emit_anomaly_subsystem(event)
        # self._emit_sse(event)
        # self._emit_webhook(event)

    # -----------------------------
    # Output Channels
    # -----------------------------

    def _emit_console(self, event):
        """
        Developer-friendly console output.
        """
        try:
            sys.stdout.write(
                f"[IDRIM] {event.get('timestamp')} | {event.get('type')} | {event.get('user')}\n"
            )
            sys.stdout.flush()
        except Exception:
            pass  # Console output is non-critical

    def _emit_audit_log(self, event):
        """
        Append event to audit log as JSONL.
        """
        try:
            with open(self.audit_log_path, "a") as f:
                f.write(json.dumps(event) + "\n")
        except Exception:
            # Fail-safe: do not crash the engine if audit logging fails
            pass

    # -----------------------------
    # Future Integration Hooks
    # -----------------------------

    def _emit_anomaly_subsystem(self, event):
        """
        Placeholder for anomaly subsystem integration.
        """
        pass

    def _emit_sse(self, event):
        """
        Placeholder for SSE event streaming.
        """
        pass

    def _emit_webhook(self, event):
        """
        Placeholder for webhook integrations.
        """
        pass
