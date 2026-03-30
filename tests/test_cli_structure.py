from ssrf_command_console.cli import cli
import click


def test_cli_is_group():
    assert isinstance(cli, click.core.Group)


def test_top_level_commands():
    expected = {"version", "hello", "scan", "payload", "enum", "plugins", "doctor"}
    assert expected.issubset(set(cli.commands.keys()))


def test_scan_subcommands():
    scan = cli.commands["scan"]
    assert isinstance(scan, click.core.Group)
    assert {"run", "profiles", "validate"}.issubset(scan.commands.keys())


def test_payload_subcommands():
    payload = cli.commands["payload"]
    assert isinstance(payload, click.core.Group)
    assert {"list", "generate", "test"}.issubset(payload.commands.keys())


def test_enum_subcommands():
    enum = cli.commands["enum"]
    assert isinstance(enum, click.core.Group)
    assert {"dns", "http", "cloud"}.issubset(enum.commands.keys())


def test_plugins_subcommands():
    plugins = cli.commands["plugins"]
    assert isinstance(plugins, click.core.Group)
    assert {"list", "run"}.issubset(plugins.commands.keys())


def test_doctor_subcommands():
    doctor = cli.commands["doctor"]
    assert isinstance(doctor, click.core.Group)
    assert {"env", "plugins", "structure"}.issubset(doctor.commands.keys())
