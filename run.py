"""
SSRF Command Console — FastAPI Launcher
Programmatic Uvicorn entrypoint for IDEs, debuggers, and operator workflows.
"""

import uvicorn


def main():
    """
    Launch the FastAPI application using Uvicorn.
    This wrapper ensures consistent startup behavior across:
    - IDEs (VSCode, PyCharm)
    - CLI workflows
    - Makefile targets
    - run.sh shell launcher
    """
    uvicorn.run(
        "app.main:app",     # FastAPI application path
        host="127.0.0.1",   # Local development host
        port=8000,          # Default API port
        reload=True,        # Auto-reload on file changes
        workers=1           # Single worker for dev mode
    )


if __name__ == "__main__":
    main()
