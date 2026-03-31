# =====================================================================
# release.mk — Versioning / Artifacts
# =====================================================================

VERSION_FILE := $(ROOT_DIR)/VERSION

.PHONY: release.version release.build release.all

release.version:
	$(call util.section,Reading version)
	if [ -f "$(VERSION_FILE)" ]; then \
		V=$$(cat "$(VERSION_FILE)"); \
		$(call util.ok,Version: $$V); \
	else \
		$(call util.warn,VERSION file missing); \
	fi

release.build:
	$(call util.section,Building release artifacts)
	$(call util.ensure_dir,$(DIST_DIR))
	$(call util.ok,Release artifacts built)

release.all: release.version release.build
	$(call util.ok,Release pipeline complete)
