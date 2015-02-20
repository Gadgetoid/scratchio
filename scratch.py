#!/usr/bin/env python
import time, socket, atexit, signal, re
from pim import AsyncWorker, StoppableThread
from array import array
from Queue import PriorityQueue, Queue

sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sck.connect(('127.0.0.1',42001))
sck.settimeout(0.5)

output = PriorityQueue()
event_queue = PriorityQueue()
handler_queue = Queue()

buf = []

_recv = None
_send = None
_event = None
_sensor_handlers = {}
_broadcast_handlers = {}

def quit():
    _recv.stop()
    _send.stop()
    _event.stop()

def broadcast(message, priority=10):
    output.put((priority,to_scratch_message("broadcast \"{}\"".format(message))))

def sensor_update(sensor, value, priority=10):
    value = str(value)
    if isinstance(value, str):
        value = value.replace('"','""')
        output.put((priority,to_scratch_message("sensor-update \"{}\" \"{}\"".format(sensor, value))))
    elif isinstance(value, int) or isinstance(value, float):
        output.put((priority,to_scratch_message("sensor-update \"{}\" {}".format(sensor, str(value)))))

def to_scratch_message(cmd):
    # Taken from scratra, Taken from chalkmarrow
    n = len(cmd)
    a = array('c')
    a.append(chr((n >> 24) & 0xFF))
    a.append(chr((n >> 16) & 0xFF))
    a.append(chr((n >>  8) & 0xFF))
    a.append(chr(n & 0xFF))
    return a.tostring() + cmd

def event():
    while not handler_queue.empty():
        message_type, path, handler = handler_queue.get()
        if message_type == 'broadcast':
            _broadcast_handlers[path] = handler
        elif message_type == 'sensor-update':
            _sensor_handlers[path] = handler
    if not event_queue.empty():
        current_event = event_queue.get()
        if current_event[1] == 'broadcast':
            value = current_event[2]
            for regex, handler in _broadcast_handlers.iteritems():
                if callable(handler) and re.match(regex, str(value)) != None:
                    handler(value)
        elif current_event[1] == 'sensor-update':
            sensor, value = current_event[2:4]
            for x in (None, sensor):
                if x in _sensor_handlers and callable(_sensor_handlers[x]):
                    _sensor_handlers[x](sensor,value)
        event_queue.task_done()
    time.sleep(0.001)
    return True

def send():
    if not output.empty():
        priority, message = output.get()
        sck.send(message)
        #print('Sending', message)
        output.task_done()
    time.sleep(0.001)
    return True

def recv():
    try:
        header = sck.recv(4)
    except socket.timeout:
        return True
    #print(header)
    if header:
        header = map(ord, header)
        msg_len = header[0] << 24 | header[1] << 16 | header[2] << 8 | header[3]
        msg = sck.recv(msg_len)
        msg = msg.split(' ')
        if msg[0] == 'broadcast':
            value = msg[1][1:-1]
            value = value.replace('""','"')
            try:
                if value.find('.') and str(float(value)) == value:
                    value = float(value)
            except ValueError:
                pass
            try:
                if str(int(value)) == value:
                    value = int(value)
            except ValueError:
                pass
            if value == "true":
                value = True
            elif value == "false":
                value = False
            event_queue.put((0,'broadcast',value))
        if msg[0] == 'sensor-update':
            sensor = msg[1][1:-1]
            value = msg[2]
            if value.startswith('"'):
                value = value[1:-1]
                if value == "true":
                    value = True
                if value == "false":
                    value = False
            elif value.find('.') != -1:
                value = float(value)
            else:
                value = int(value)
            event_queue.put((0,'sensor-update',sensor,value))
            #print(msg)
    return True

def on_message(message = None):
    def register(handler):
        handler_queue.put(('broadcast', message, handler))
        #global _broadcast_handlers
        #_broadcast_handlers[message] = handler
    return register

def on_change(sensor):
    def register(handler):
        handler_queue.put(('sensor-update', sensor, handler))
        #global _sensor_handlers
        #_sensor_handlers[sensor] = handler  
    return register

_recv = AsyncWorker(recv)
_recv.start()
_send = AsyncWorker(send)
_send.start()
_event = AsyncWorker(event)
_event.start()
atexit.register(quit)


if __name__ == 'main':
    broadcast('go')

    @on_message('ack')
    def ack(msg):
        print('Got ACK')

    @on_change('test')
    def change(sensor, value):
        print(sensor,value)
        broadcast('hi')

#while True:
#    time.sleep(1)
#    broadcast('hi')
#    sensor_update("changeme",999)

    signal.pause()
