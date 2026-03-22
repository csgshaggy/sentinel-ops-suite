import click
from ssrf_command_console.version import __version__

@click.group()
def cli():
    """SSRF Command Console"""
    pass

@cli.command()
def version():
    """Show version information."""
    click.echo(f"ssrf-command-console version {__version__}")

def main():
    cli()
