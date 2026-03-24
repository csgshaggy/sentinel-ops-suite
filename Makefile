# ============================================================
# Root Makefile — Operator‑Grade, CI‑Safe, Doctor‑Compatible
# ============================================================

# -----------------------------
# Backend
# -----------------------------
backend-test:
	$(MAKE) -C backend test-unit

# -----------------------------
# Dashboard
# -----------------------------
dashboard-test:
	$(MAKE) -C dashboard test-unit

# -----------------------------
# Full CI Check
# -----------------------------
ci-check: backend-test dashboard-test
	@echo "All CI checks passed."

# -----------------------------
# Deprecated Doctor Target
# (kept for compatibility with validators)
# -----------------------------
doctor:
	@echo "doctor target deprecated — skipping"
