import json
import traceback
import zmq

def runserver():
    sock = zmq.Context().socket(zmq.REP)
    sock.bind('tcp://127.0.0.1:5454')
    while True:
        recved = sock.recv()
        func, arg = json.loads(recved)
        try:
            if func == 'exec':
                exec arg in globals(), globals()
                response = None
            elif func == 'eval':
                response = eval(arg, globals(), globals())
            pickled = json.dumps([200, response])
        except Exception:
            pickled = json.dumps([500, ''.join(traceback.format_exc())])
        sock.send(pickled)
