# backend/app/tui/main.py

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from backend.app.tui.panels.anomaly_panel import render_anomaly_panel


def main() -> None:
    console = Console()

    while True:
        console.print(
            Panel(
                "[bold cyan]SSRF Command Console — TUI[/bold cyan]\n"
                "\n"
                "[1] View Anomaly History\n"
                "[2] Exit\n",
                title="Main Menu",
            )
        )

        choice = Prompt.ask("Select an option", choices=["1", "2"], default="2")

        if choice == "1":
            render_anomaly_panel()
            console.print("\nPress Enter to return to menu.")
            input()
        elif choice == "2":
            console.print("[bold green]Goodbye![/bold green]")
            break


if __name__ == "__main__":
    main()
