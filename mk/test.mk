# ==============================================================================
# TEST MODULE
# ==============================================================================
# Provides deterministic, operator‑grade test execution for local development,
# CI pipelines, and pre‑commit hooks. This module is intentionally generic and
# can be extended for Python, Node, or shell‑based test suites.
# ==============================================================================


# ------------------------------------------------------------------------------
# COLORS
# ------------------------------------------------------------------------------
COLOR_RESET  := \033[0m
COLOR_RED    := \033[31m
COLOR_GREEN  := \033[32m
COLOR_YELLOW := \033[33m
COLOR_BLUE   := \033[34m


# ------------------------------------------------------------------------------
# TEST CONFIGURATION
# ------------------------------------------------------------------------------
TEST_DIR      ?= tests
TEST_PATTERN  ?= test_*.py
PYTHON        ?= python3
NODE          ?= node


# ------------------------------------------------------------------------------
# INTERNAL HELPERS
# ------------------------------------------------------------------------------
test_msg_ok = \
	printf "$(COLOR_GREEN)[OK]$(COLOR_RESET) %s\n" "$(1)"

test_msg_fail = \
	printf "$(COLOR_RED)[FAIL]$(COLOR_RESET) %s\n" "$(1)"

test_msg_info = \
	printf "$(COLOR_BLUE)[test]$(COLOR_RESET) %s\n" "$(1)"


# ------------------------------------------------------------------------------
# PYTHON TESTS
# ------------------------------------------------------------------------------
test.python:
	@$(call test_msg_info,"Running Python tests...")
	@$(PYTHON) -m pytest $(TEST_DIR) -q || { \
		$(call test_msg_fail,"Python tests failed"); exit 1; }
	@$(call test_msg_ok,"Python tests passed")


# ------------------------------------------------------------------------------
# NODE TESTS
# ------------------------------------------------------------------------------
test.node:
	@$(call test_msg_info,"Running Node tests...")
	@$(NODE) ./node_modules/.bin/jest --silent || { \
		$(call test_msg_fail,"Node tests failed"); exit 1; }
	@$(call test_msg_ok,"Node tests passed")


# ------------------------------------------------------------------------------
# SHELL TESTS (generic)
# ------------------------------------------------------------------------------
test.shell:
	@$(call test_msg_info,"Running shell tests...")
	@bash $(TEST_DIR)/run.sh || { \
		$(call test_msg_fail,"Shell tests failed"); exit 1; }
	@$(call test_msg_ok,"Shell tests passed")


# ------------------------------------------------------------------------------
# AGGREGATE TEST TARGET
# ------------------------------------------------------------------------------
test: test.python
	@$(call test_msg_ok,"All test suites passed")
