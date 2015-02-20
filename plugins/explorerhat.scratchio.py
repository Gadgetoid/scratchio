class Plugin():
    def __init__(self, scratch):
        import explorerhat
        self.explorerhat = explorerhat
        def touch_handler(channel, event):
            #print("Got touch {} {}".format(channel, event))
            scratch.sensor_update('explorerhat_touch_{}'.format(channel),event == 'press', 0)
            scratch.broadcast('explorerhat:update')
        self.explorerhat.touch.pressed(touch_handler)
        self.explorerhat.touch.released(touch_handler)
        def input_handler(name,pin):
            scratch.sensor_update('explorerhat_input_{}'.format(name),pin.read() == 1, 0)
            scratch.broadcast('explorerhat:update')
        self.explorerhat.input.one.changed(lambda x: input_handler('one',x))
        self.explorerhat.input.two.changed(lambda x: input_handler('two',x))
        self.explorerhat.input.three.changed(lambda x: input_handler('three',x))
        self.explorerhat.input.four.changed(lambda x: input_handler('four',x))

        @scratch.on_message('^explorerhat:')
        def handle_message(message):
            #print(message)
            message = message.split(':')
            if len(message) < 4:
                return False
            _collection = message[1]
            _item       = message[2]
            _function   = message[3].replace('()','')
            _args       = []
            
            # Parse arguments if () at end of function
            if _function.endswith(')'):
                temp = _function.split('(')
                _function = temp[0]
                _args = temp[1][:-1].replace(' ','').split(',')
                for arg,val in enumerate(_args):
                    try:
                        if str(int(val)) == val:
                            val = int(val)
                        elif str(float(val)) == val:
                            val = float(val)
                    except ValueError:
                        val = _args[arg]
                    finally:
                        _args[arg] = val
                
            #print("Scratch said",message)
            if hasattr(explorerhat, _collection):
                #print("Found: ",_collection)
                collection = getattr(explorerhat,_collection)
                if _item in str(collection).split(', '):
                    pin = collection[_item]
                    if hasattr(pin,_function):
                        getattr(pin,_function)(*_args)
