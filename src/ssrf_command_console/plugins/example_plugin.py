from .base import SSRFPlugin

class ExamplePlugin(SSRFPlugin):
    name = "example"

    def run(self, **kwargs):
        return {"status": "ok", "message": "Example plugin executed."}
