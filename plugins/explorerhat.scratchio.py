import plugin
class Plugin(plugin.Plugin):
    def __init__(self, scratch):
        import explorerhat
        self.target = explorerhat
        plugin.Plugin.__init__(self, scratch)

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

