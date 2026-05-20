# ============================================================
# Banners (Reusable Echo Blocks)
# Canonical Operator‑Grade Banner Library
# ============================================================

# Generic banner
define banner
	@echo -e "$(BLUE)== $(1) ==$(RESET)"
endef

# Success banner
define banner-success
	@echo -e "$(GREEN)== $(1) ==$(RESET)"
endef

# Warning banner
define banner-warn
	@echo -e "$(YELLOW)== $(1) ==$(RESET)"
endef

# Error banner
define banner-error
	@echo -e "$(RED)== $(1) ==$(RESET)"
endef

# Section header (bold + blue)
define banner-section
	@echo -e "$(BOLD)$(BLUE)=== $(1) ===$(RESET)"
endef

# Subsection header
define banner-sub
	@echo -e "$(CYAN)-- $(1) --$(RESET)"
endef
