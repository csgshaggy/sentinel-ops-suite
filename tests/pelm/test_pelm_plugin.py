from tools.plugins.pelm import PELMPlugin

def test_pelm_plugin_runs():
    plugin = PELMPlugin()
    result = plugin.run()
    assert result["status"] == "executed"
