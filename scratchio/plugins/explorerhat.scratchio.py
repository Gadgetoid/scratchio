import time
import plugin

class Plugin(plugin.Plugin):
    def __init__(self, scratch):
        import explorerhat

        self.name = 'explorerhat'
        self.target = explorerhat
        plugin.Plugin.__init__(self, scratch)

        self.target._pwm = None

        def servo(position):
            if self.target._pwm is None:
                explorerhat.GPIO.setup(18, explorerhat.GPIO.OUT)
                self.target._pwm = explorerhat.GPIO.PWM(18, 50)
                self.target._pwm.start(0)

            try:
                position = float(position)
            except ValueError:
                print("Error: Could not convert position '{}' to float!".format(position))
                return

            self.target._pwm.ChangeDutyCycle(position)

        self.target.servo = servo

        def touch_handler(channel, event):
            #print("Got touch {} {}".format(channel, event))
            scratch.sensor_update('explorerhat_touch_{}'.format(channel),event == 'press', 0)
            scratch.broadcast('explorerhat:update')

        self.target.touch.pressed(touch_handler)
        self.target.touch.released(touch_handler)

        def input_handler(name,pin):
            scratch.sensor_update('explorerhat_input_{}'.format(name),pin.read() == 1, 0)
            scratch.broadcast('explorerhat:update')

        self.target.input.one.changed(lambda x: input_handler('one',x))
        self.target.input.two.changed(lambda x: input_handler('two',x))
        self.target.input.three.changed(lambda x: input_handler('three',x))
        self.target.input.four.changed(lambda x: input_handler('four',x))

    def run(self):
        analog = self.target.analog.read()
        for key in analog.keys():
            #print('explorerhat_analog_{} = {}'.format(key, analog[key]))
            self._scratch.sensor_update('explorerhat_analog_{}'.format(key), analog[key], 0)

        self._scratch.broadcast('explorerhat:update')
        time.sleep(1)
