class Plugin():
    def __init__(self, scratch):
        import RPi.GPIO
        self.gpio = RPi.GPIO
        self.gpio.setmode(self.gpio.BCM)
        @scratch.on_message('^gpio:')
        def handle_message(message):
            print(message)
