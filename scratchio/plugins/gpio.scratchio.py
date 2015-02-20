import plugin
class Plugin(plugin.Plugin):
    def __init__(self, scratch):
        import RPi.GPIO
        self.name = 'gpio'
        self.target = RPi.GPIO
        plugin.Plugin.__init__(self, scratch)
