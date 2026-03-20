.PHONY: tui backend all clean sync doctor clean-root

# -------------------------------------------------------------------
# Application Targets
# -------------------------------------------------------------------

tui:
	python3 main.py

backend:
	python3 run_uvicorn.py

all:
	@echo "Starting backend..."
	@gnome-terminal -- bash -c "./run_backend.sh; exec bash"
	@echo "Starting TUI..."
	@./run_tui.sh

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +

# -------------------------------------------------------------------
# Maintenance Targets
# -------------------------------------------------------------------

doctor:
	@echo ">>> Running project doctor..."
	python3 doctor.py

clean-root:
	@echo ">>> Running hardened root cleanup..."
	python3 cleanup_root.py

sync:
	@echo ">>> Running project doctor..."
	python3 doctor.py
	@echo ">>> Running hardened root cleanup..."
	python3 cleanup_root.py
	@echo ">>> Staging changes..."
	git add .
	@echo ">>> Committing..."
	git commit -m "Sync: $$(date '+%Y-%m-%d %H:%M:%S')" || echo "No changes to commit."
	@echo ">>> Pushing to GitHub..."
	git push -u origin main
	@echo ">>> Sync complete."
