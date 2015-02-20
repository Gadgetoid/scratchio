class Plugin():
    def __init__(self, scratch):
        import pibrella
        self.pibrella = pibrella

        def input_handler(pin):
            scratch.sensor_update('pibrella_button',pin.read() == 1, 0)
            scratch.broadcast('pibrella:update')
        self.pibrella.button.changed(input_handler)
 
        @scratch.on_message('^pibrella:')
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
            if hasattr(pibrella, _collection):
                #print("Found: ",_collection)
                collection = getattr(pibrella,_collection)
                if _item in str(collection).split(', '):
                    pin = collection[_item]
                    if hasattr(pin,_function):
                        getattr(pin,_function)(*_args)
