# ================================
# mk/release.mk — Release Pipeline
# ================================

VERSION_FILE := VERSION
DATE := $(shell date +"%Y-%m-%d")
TIME := $(shell date +"%H:%M:%S")
GIT_SHA := $(shell git rev-parse --short HEAD 2>/dev/null || echo "no-git")

# --------------------------------
# release — full release pipeline
# --------------------------------
release: release.version release.tag
	@echo "[release] Release complete."

# --------------------------------
# release.version — write VERSION file
# --------------------------------
release.version:
	@echo "[release.version] Writing VERSION file..."
	@if [ ! -f $(VERSION_FILE) ]; then \
		echo "0.1.0" > $(VERSION_FILE); \
		echo "[release.version] Initialized VERSION to 0.1.0"; \
	else \
		echo "[release.version] VERSION file exists, leaving unchanged."; \
	fi
	@echo "[release.version] Done."

# --------------------------------
# release.tag — create git tag
# --------------------------------
release.tag:
	@echo "[release.tag] Creating git tag..."
	@if [ -f $(VERSION_FILE) ]; then \
		V=$$(cat $(VERSION_FILE)); \
		git tag -a "v$$V" -m "Release $$V ($(DATE) $(TIME), $(GIT_SHA))" || true; \
		echo "[release.tag] Tagged v$$V"; \
	else \
		echo "[release.tag] VERSION file missing, cannot tag."; \
		exit 1; \
	fi
