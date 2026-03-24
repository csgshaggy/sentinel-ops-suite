from click.testing import CliRunner
from ssrf_command_console.cli import cli


def test_version_command():
    runner = CliRunner()
    result = runner.invoke(cli, ["version"])
    assert result.exit_code == 0
    assert "ssrf-command-console version" in result.output
