class Plugin:
    name = "pelm"
    description = "PELM core plugin"

    def run(self):
        return {"status": "ok", "plugin": self.name}
