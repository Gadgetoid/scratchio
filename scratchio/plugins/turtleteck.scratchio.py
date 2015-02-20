import plugin
class Plugin(plugin.Plugin):
    def __init__(self, scratch):
        import RPi.GPIO
        self.name = 'turtleteck'
        self.target = RPi.GPIO
        plugin.Plugin.__init__(self, scratch)
        @scratch.on_message('^turtleteck\ forward ')
        def forward(msg):
            print("Wheee, forward!", msg)
        @scratch.on_message('^turtleteck\ backward ')
        def backward(msg):
            print("Oooh, backward!", msg)
