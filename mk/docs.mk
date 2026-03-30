# ================================
# mk/docs.mk — Documentation & Structure
# ================================

self-check:
	@echo "[self-check] Running documentation structure checks..."
	@test -f README.md || (echo "Missing README.md" && exit 1)
	@test -d docs || echo "[self-check] docs/ directory not found (optional)"
	@echo "[self-check] Done."

plugins.load:
	@echo "[plugins] Loading plugin manifest..."
	@test -f plugins.json || echo "[plugins] No plugin manifest found."
