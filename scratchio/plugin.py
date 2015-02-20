class Plugin():
    def __init__(self, scratch):
        self._vars = {}

        print("Registering handlers for {}".format(self.name.lower()))
        @scratch.on_change('^{}:'.format(self.name.lower()))
        def handle_update(sensor, value):
            sensor = sensor.split(':')[1]
            print("New variable",sensor,value)
            self._vars[sensor] = value
 
        @scratch.on_message('^{}:'.format(self.name.lower()))
        def handle_message(message):
            print("New broadcast",message)
            message = message.split(':')

            obj = self.target
            for idx,path in enumerate(message[1:]):
                path, args = self._parse_args(path)
                if hasattr(obj, path):
                    obj = getattr(obj, path)
                    if idx == len(message[1:])-1 and callable(obj):
                        print('Calling with args', path, args)
                        try:
                            obj(*args)
                        except RuntimeError as e:
                            print('Failed:',e.message)
                        except ValueError as e:
                            print('Failed:',e.message)

    def _parse_args(self, path):
        args = []
        path = path.replace('()','')
        # Parse arguments if () at end of function
        if path.endswith(')'):
            temp = path.split('(')
            path = temp[0]
            args = temp[1][:-1].split(',')
            for arg,val in enumerate(args):
                args[arg] = self._parse_var(val)
        return (path, args)

    def _parse_var(self, var):
        var = var.strip()
        parsed = var
        #print('Parsing var',var)
        if var.startswith('%') and var[1:] in self._vars:
            parsed = self._vars[var[1:]]
        elif var.startswith('"') and var.endswith('"'):
            parsed = var[1:-1]
        elif var.startswith("'") and var.endswith("'"):
            parsed = var[1:-1]
        elif hasattr(self.target,var):
            parsed = getattr(self.target,var)
        else:
            try:
                if str(int(var)) == var:
                    parsed = int(var)
                elif str(float(var)) == var:
                    parsed = float(var)
            except ValueError:
                parsed = var
        return parsed
                
