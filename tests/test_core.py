from ssrf_command_console.core.engine import hello


def test_hello():
    assert hello() == "ssrf_command_console core engine active"
