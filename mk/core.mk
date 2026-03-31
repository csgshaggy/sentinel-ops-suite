# =====================================================================
# core.mk — Core Init / Clean
# =====================================================================

.PHONY: core.init core.clean

core.init:
	$(call util.section,Core init)
	$(call util.ensure_dir,$(BUILD_DIR))
	$(call util.ensure_dir,$(DIST_DIR))
	$(call util.ok,Core init complete)

core.clean:
	$(call util.section,Cleaning build + dist)
	rm -rf "$(BUILD_DIR)" "$(DIST_DIR)"
	$(call util.ok,Clean complete)
