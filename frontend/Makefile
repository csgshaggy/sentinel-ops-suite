# ============================================
# DASHBOARD MAKEFILE — HARDENED EDITION
# ============================================

.PHONY: install
install:
	@npm install

.PHONY: dev
dev:
	@npm run dev

.PHONY: build
build:
	@npm run build

.PHONY: test
test:
	@npm test

# --------------------------------------------
# SAFE CLEAN (delegates to root)
# --------------------------------------------
.PHONY: safe-clean
safe-clean:
	@echo "Delegating safe-clean to root Makefile..."
	@make -C .. safe-clean

# --------------------------------------------
# VALIDATE
# --------------------------------------------
.PHONY: validate
validate:
	@echo "Validating dashboard structure..."
	@python3 ../scripts/structure_validator.py
