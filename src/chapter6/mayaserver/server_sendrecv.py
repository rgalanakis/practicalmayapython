import json
import zmq

def runserver():
    sock = zmq.Context().socket(zmq.REP)
    sock.bind('tcp://127.0.0.1:5454')
    while True:
        recved = sock.recv()
        func, arg = json.loads(recved)
        if func == 'exec':
            exec arg in globals(), globals()
            tosend = None
        elif func == 'eval':
            tosend = eval(arg, globals(), globals())
        picktosend = json.dumps(tosend)
        sock.send(picktosend)
