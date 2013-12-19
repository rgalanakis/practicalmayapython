import json
import traceback
import zmq

import mayaserver

def runserver():
    sock = zmq.Context().socket(zmq.REP)
    sock.bind('tcp://127.0.0.1:5454')
    while True:
        recved = sock.recv()
        try:
            func, arg = json.loads(recved)
            code = mayaserver.SUCCESS
            response = None
            if func == 'exec':
                exec arg in globals(), globals()
            elif func == 'eval':
                response = eval(arg, globals(), globals())
            else:
                code =  mayaserver.INVALID_METHOD
                response = func
            pickled = json.dumps([code, response])
        except Exception:
            pickled = json.dumps([
                mayaserver.UNHANDLED_ERROR,
                ''.join(traceback.format_exc())])
        sock.send(pickled)
