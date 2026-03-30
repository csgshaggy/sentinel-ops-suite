# ============================================
# BACKEND MAKEFILE — HARDENED EDITION
# ============================================

.PHONY: run
run:
	@uvicorn backend.app.main:app --reload

.PHONY: test
test:
	@pytest -q

.PHONY: build
build:
	@echo "Building backend..."
	@python3 -m compileall backend/

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
	@echo "Validating backend structure..."
	@python3 ../scripts/structure_validator.py
