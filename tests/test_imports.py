from ssrf_command_console.core import hello

def test_hello():
    assert hello() == "ssrf_command_console package is active"
