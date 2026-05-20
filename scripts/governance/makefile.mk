# scripts/governance/makefile.mk
# Makefile Governance Include
# Provides the governance-makefile target for strict Makefile validation.

governance-makefile:
	@echo "[governance] Running Makefile integrity checks..."
	@node scripts/governance/governance-makefile-check.cjs

.PHONY: governance-makefile
