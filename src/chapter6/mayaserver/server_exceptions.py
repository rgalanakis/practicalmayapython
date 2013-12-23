import json
import traceback #(1)
import zmq
import mayaserver #(1)

def runserver():
    sock = zmq.Context().socket(zmq.REP)
    sock.bind('tcp://127.0.0.1:5454')
    while True:
        recved = sock.recv()
        try: #(2)
            func, arg = json.loads(recved)
            code = mayaserver.SUCCESS #(3)
            response = None
            if func == 'exec':
                exec arg in globals(), globals()
            elif func == 'eval':
                response = eval(arg, globals(), globals())
            else:
                code =  mayaserver.INVALID_METHOD #(4)
                response = func
            pickled = json.dumps([code, response])
        except Exception: #(5)
            pickled = json.dumps([
                mayaserver.UNHANDLED_ERROR,
                ''.join(traceback.format_exc())])
        sock.send(pickled)
