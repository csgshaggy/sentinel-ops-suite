class SSRFPlugin:
    """
    Base class for all SSRF Console plugins.
    """

    name: str = "unnamed"

    def run(self, **kwargs):
        raise NotImplementedError("Plugins must implement run().")
