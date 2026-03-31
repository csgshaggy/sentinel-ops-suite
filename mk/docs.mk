# =====================================================================
# docs.mk — Documentation / Graph
# =====================================================================

DOCS_GRAPH := $(DOCS_DIR)/MAKEFILE_GRAPH.md

.PHONY: docs.build docs.graph docs.all

docs.build:
	$(call util.section,Building docs)
	$(call util.ensure_dir,$(DOCS_DIR))
	$(call util.ok,Docs build complete)

docs.graph:
	$(call util.section,Generating Makefile module dependency graph)
	$(call util.ensure_dir,$(DOCS_DIR))
	printf "# Makefile Module Dependency Graph\n\n" > "$(DOCS_GRAPH)"
	printf "- util.mk → all modules\n" >> "$(DOCS_GRAPH)"
	printf "- core.mk → init/clean\n" >> "$(DOCS_GRAPH)"
	printf "- env.mk → env.*\n" >> "$(DOCS_GRAPH)"
	printf "- validate.mk → validate.*\n" >> "$(DOCS_GRAPH)"
	printf "- audit.mk → audit.*\n" >> "$(DOCS_GRAPH)"
	printf "- docs.mk → docs.*\n" >> "$(DOCS_GRAPH)"
	printf "- release.mk → release.*\n" >> "$(DOCS_GRAPH)"
	printf "- test.mk → test.*\n" >> "$(DOCS_GRAPH)"
	$(call util.ok,Graph written)

docs.all: docs.build docs.graph
	$(call util.ok,Docs suite complete)
