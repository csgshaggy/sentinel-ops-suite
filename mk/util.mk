# ================================
# mk/util.mk — Utility Helpers
# ================================

COLOR_GREEN=\033[0;32m
COLOR_RED=\033[0;31m
COLOR_YELLOW=\033[1;33m
COLOR_RESET=\033[0m

print.green:
	@echo -e "$(COLOR_GREEN)$$MSG$(COLOR_RESET)"

print.red:
	@echo -e "$(COLOR_RED)$$MSG$(COLOR_RESET)"

print.yellow:
	@echo -e "$(COLOR_YELLOW)$$MSG$(COLOR_RESET)"
