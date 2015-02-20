import plugin
class Plugin(plugin.Plugin):
    def __init__(self, scratch):
        import pibrella
        self.target = pibrella
        self.name = 'Pibrella'
        plugin.Plugin.__init__(self, scratch)

        def input_handler(pin):
            scratch.sensor_update('pibrella_button',pin.read() == 1, 0)
            scratch.broadcast('pibrella:update')
        self.target.button.changed(input_handler)

