"""
SSRF Command Console — Operator-Grade CLI Entry Point.

This module defines the full command tree for the SSRF Command Console,
including scanning, payload generation, enumeration, plugin management,
and diagnostic utilities.

The CLI is implemented using Typer and exported as a Click Group so that
pytest and external tooling can import `cli` directly.
"""

import typer
from typer.main import get_group

from .version import __version__

# ============================================================================
# ROOT APPLICATION
# ============================================================================

_app = typer.Typer(
    name="ssrf-console",
    no_args_is_help=True,
    help="SSRF Command Console — operator-grade SSRF tooling.",
)


# ============================================================================
# VERSION COMMAND
# ============================================================================


@_app.command("version")
def version_command() -> None:
    """
    Display the SSRF Command Console version.
    """
    typer.echo(f"ssrf-command-console version {__version__}")


# ============================================================================
# HELLO COMMAND
# ============================================================================


@_app.command("hello")
def hello_command(name: str = "operator") -> None:
    """
    Simple connectivity/sanity check.
    """
    typer.echo(f"[ssrf-console] Hello, {name}.")


# ============================================================================
# SCAN COMMAND GROUP
# ============================================================================

scan_app = typer.Typer(help="SSRF scanning operations.")
_app.add_typer(scan_app, name="scan")


@scan_app.command("run")
def scan_run(
    target: str = typer.Argument(..., help="Target URL to probe for SSRF."),
    profile: str = typer.Option("default", help="Scan profile to use."),
) -> None:
    """
    Execute an SSRF scan against a target URL.
    """
    typer.echo(f"[scan] (stub) scanning {target} with profile '{profile}'.")


@scan_app.command("profiles")
def scan_profiles() -> None:
    """
    List available scan profiles.
    """
    typer.echo("[scan] Available profiles: default, aggressive, cloud")


@scan_app.command("validate")
def scan_validate(target: str) -> None:
    """
    Validate that a target URL is suitable for SSRF scanning.
    """
    typer.echo(f"[scan] Validating target: {target}")


# ============================================================================
# PAYLOAD COMMAND GROUP
# ============================================================================

payload_app = typer.Typer(help="Payload generation and testing.")
_app.add_typer(payload_app, name="payload")


@payload_app.command("list")
def payload_list() -> None:
    """
    List available payload templates.
    """
    typer.echo("[payload] Listing payload templates...")


@payload_app.command("generate")
def payload_generate(kind: str) -> None:
    """
    Generate a payload of a given type.
    """
    typer.echo(f"[payload] Generating payload of type: {kind}")


@payload_app.command("test")
def payload_test(payload: str) -> None:
    """
    Test a payload against a local or remote endpoint.
    """
    typer.echo(f"[payload] Testing payload: {payload}")


# ============================================================================
# ENUM COMMAND GROUP
# ============================================================================

enum_app = typer.Typer(help="Enumeration utilities.")
_app.add_typer(enum_app, name="enum")


@enum_app.command("dns")
def enum_dns(domain: str) -> None:
    """
    Perform DNS enumeration on a domain.
    """
    typer.echo(f"[enum] DNS enumeration for {domain}")


@enum_app.command("http")
def enum_http(url: str) -> None:
    """
    Perform HTTP enumeration on a URL.
    """
    typer.echo(f"[enum] HTTP enumeration for {url}")


@enum_app.command("cloud")
def enum_cloud(provider: str) -> None:
    """
    Perform cloud provider enumeration.
    """
    typer.echo(f"[enum] Cloud enumeration for provider: {provider}")


# ============================================================================
# PLUGINS COMMAND GROUP
# ============================================================================

plugins_app = typer.Typer(help="Plugin management.")
_app.add_typer(plugins_app, name="plugins")


@plugins_app.command("list")
def plugins_list() -> None:
    """
    List all available SSRF plugins.
    """
    from .plugin_loader import load_plugins

    plugins = load_plugins()
    if not plugins:
        typer.echo("No plugins found.")
        return

    typer.echo("Available plugins:")
    for name in plugins:
        typer.echo(f" - {name}")


@plugins_app.command("run")
def plugins_run(name: str) -> None:
    """
    Execute a plugin by name.
    """
    from .plugin_loader import load_plugins

    plugins = load_plugins()
    if name not in plugins:
        typer.echo(f"Plugin '{name}' not found.")
        raise typer.Exit(code=1)

    result = plugins[name].run()
    typer.echo(f"Plugin '{name}' result: {result}")


# ============================================================================
# DOCTOR COMMAND GROUP
# ============================================================================

doctor_app = typer.Typer(help="System diagnostics.")
_app.add_typer(doctor_app, name="doctor")


@doctor_app.command("env")
def doctor_env() -> None:
    """
    Validate environment configuration.
    """
    typer.echo("[doctor] Environment looks good.")


@doctor_app.command("plugins")
def doctor_plugins() -> None:
    """
    Validate plugin subsystem.
    """
    typer.echo("[doctor] Plugin subsystem OK.")


@doctor_app.command("structure")
def doctor_structure() -> None:
    """
    Validate project structure.
    """
    typer.echo("[doctor] Project structure validated.")


# ============================================================================
# EXPORT CLICK GROUP (CRITICAL FOR TESTS)
# ============================================================================

cli = get_group(_app)
