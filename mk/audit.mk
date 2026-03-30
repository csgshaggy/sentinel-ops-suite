# ================================
# mk/audit.mk — Makefile Self-Audit
# ================================

self.audit:
	@echo "[self.audit] Running Makefile self-audit..."

	@echo "[self.audit] Checking for unexpected mk/*.mk files..."
	@allowed="core.mk docs.mk validate.mk util.mk audit.mk release.mk env.mk"; \
	for f in mk/*.mk; do \
		base=$$(basename $$f); \
		echo "$$allowed" | grep -qw "$$base" || { \
			echo "[self.audit] Unexpected mk file: $$base"; \
			exit 1; \
		}; \
	done

	@echo "[self.audit] Checking for duplicate targets..."
	@dups=$$(grep -R "^[a-zA-Z0-9_.-]\+:" -n Makefile mk/ \
		| awk -F: '{print $$3}' \
		| sed 's/ .*//' \
		| sort \
		| uniq -d); \
	if [ -n "$$dups" ]; then \
		echo "[self.audit] Duplicate targets detected:"; \
		echo "$$dups"; \
		exit 1; \
	fi

	@echo "[self.audit] Self-audit passed."
