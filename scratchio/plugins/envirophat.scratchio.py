import time

import plugin


class Plugin(plugin.Plugin):
    def __init__(self, scratch):
        import envirophat
        self.name = 'envirophat'
        self.target = envirophat

        plugin.Plugin.__init__(self, scratch)

    def run(self):
        analog = self.target.analog.read_all()
        for x in range(4):
            #print('envirophat_analog{} = {}'.format(x, analog[x]))
            self._scratch.sensor_update('envirophat_analog{}'.format(x), analog[x], 0)

        r, g, b = self.target.light.rgb()
        self._scratch.sensor_update('envirophat_light_r', r, 0)
        self._scratch.sensor_update('envirophat_light_g', g, 0)
        self._scratch.sensor_update('envirophat_light_b', b, 0)

        x, y, z = self.target.motion.accelerometer()
        self._scratch.sensor_update('envirophat_motion_x', x, 0)
        self._scratch.sensor_update('envirophat_motion_y', y, 0)
        self._scratch.sensor_update('envirophat_motion_z', z, 0)

        heading = self.target.motion.heading()
        self._scratch.sensor_update('envirophat_heading', heading, 0)

        temp = self.target.weather.temperature()
        self._scratch.sensor_update('envirophat_temperature', temp, 0)

        pressure = self.target.weather.pressure()
        self._scratch.sensor_update('envirophat_pressure', pressure, 0)
        

        self._scratch.broadcast('envirophat:update')
        time.sleep(1)
