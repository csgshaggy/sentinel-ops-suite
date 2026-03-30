# ================================
# mk/env.mk — Environment Snapshot & Diff
# ================================

ENV_DIR := .envsnap
ENV_SNAPSHOT := $(ENV_DIR)/snapshot.txt
ENV_CURRENT := $(ENV_DIR)/current.txt

define WRITE_ENV
echo "DATE=$$(date)";
echo "UNAME=$$(uname -a)";
echo "PYTHON=$$(python3 --version 2>/dev/null || echo none)";
echo "NODE=$$(node --version 2>/dev/null || echo none)";
echo "NPM=$$(npm --version 2>/dev/null || echo none)";
echo "PIP_PKGS:";
pip freeze 2>/dev/null || echo none;
echo "";
echo "NPM_PKGS:";
npm list --prefix dashboard --depth=0 2>/dev/null || echo none;
endef

# --------------------------------
# env.snapshot — capture baseline
# --------------------------------
env.snapshot:
	@echo "[env.snapshot] Capturing environment snapshot..."
	@mkdir -p $(ENV_DIR)
	@$(WRITE_ENV) > $(ENV_SNAPSHOT)
	@echo "[env.snapshot] Snapshot written to $(ENV_SNAPSHOT)"

# --------------------------------
# env.diff — compare current vs snapshot
# --------------------------------
env.diff:
	@echo "[env.diff] Comparing environment to snapshot..."
	@if [ ! -f $(ENV_SNAPSHOT) ]; then \
		echo "[env.diff] No snapshot found. Run 'make env.snapshot' first."; \
		exit 1; \
	fi
	@mkdir -p $(ENV_DIR)
	@$(WRITE_ENV) > $(ENV_CURRENT)
	@diff -u $(ENV_SNAPSHOT) $(ENV_CURRENT) || true
	@echo "[env.diff] Done."

# --------------------------------
# env.validate — fail if drift exists
# --------------------------------
env.validate:
	@echo "[env.validate] Validating environment against snapshot..."
	@if [ ! -f $(ENV_SNAPSHOT) ]; then \
		echo "[env.validate] No snapshot found. Run 'make env.snapshot' first."; \
		exit 1; \
	fi
	@mkdir -p $(ENV_DIR)
	@$(WRITE_ENV) > $(ENV_CURRENT)
	@if ! diff -u $(ENV_SNAPSHOT) $(ENV_CURRENT) >/dev/null; then \
		echo "[env.validate] Environment drift detected."; \
		diff -u $(ENV_SNAPSHOT) $(ENV_CURRENT) || true; \
		exit 1; \
	fi
	@echo "[env.validate] Environment matches snapshot."
