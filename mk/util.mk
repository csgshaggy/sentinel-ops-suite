# =====================================================================
# util.mk — Shared Helpers, Colors, Paths
# =====================================================================

COLOR_RESET := \033[0m
COLOR_OK := \033[32m
COLOR_WARN := \033[33m
COLOR_ERR := \033[31m
COLOR_SECTION := \033[36m

ROOT_DIR := $(shell pwd)
MK_DIR := $(ROOT_DIR)/mk
BUILD_DIR := $(ROOT_DIR)/build
DIST_DIR := $(ROOT_DIR)/dist
DOCS_DIR := $(ROOT_DIR)/docs

define util.ensure_dir
	mkdir -p $(1)
endef

define util.section
	printf "$(COLOR_SECTION)==> %s$(COLOR_RESET)\n" "$(1)"
endef

define util.ok
	printf "$(COLOR_OK)[OK]$(COLOR_RESET) %s\n" "$(1)"
endef

define util.warn
	printf "$(COLOR_WARN)[WARN]$(COLOR_RESET) %s\n" "$(1)"
endef

define util.err
	printf "$(COLOR_ERR)[ERROR]$(COLOR_RESET) %s\n" "$(1)"
endef
