import click
from ssrf_command_console.cli import cli

assert isinstance(cli, click.core.Group), "CLI must export a Click Group"

expected = {"version", "hello", "scan", "payload", "enum", "plugins", "doctor"}
missing = expected - set(cli.commands.keys())
assert not missing, f"Missing top-level commands: {missing}"

print("[OK] CLI structure validated.")
