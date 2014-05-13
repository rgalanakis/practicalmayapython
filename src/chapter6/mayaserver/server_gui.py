import json
import threading
import traceback
import zmq
import mayaserver

from maya.utils import executeInMainThreadWithResult

def runserver(handshake_port):
    threading.Thread(
        target=_runserver, args=[handshake_port]).start()

def _eval(s):
    return eval(s, globals(), globals())

def _exec(s):
    exec s in globals(), globals()

def _runserver(handshake_port):
    sock = zmq.Context().socket(zmq.REP)
    appport = sock.bind_to_random_port('tcp://127.0.0.1')

    handshakesock = zmq.Context().socket(zmq.REQ)
    handshakesock.connect('tcp://127.0.0.1:%s' % handshake_port)
    handshakesock.send(str(appport))
    handshakesock.recv() # acknowledgement
    handshakesock.close()

    while True:
        recved = sock.recv()
        func, arg = json.loads(recved)
        try:
            code = mayaserver.SUCCESS
            response = None
            if func == 'exec':
                executeInMainThreadWithResult(_exec, arg)
            elif func == 'eval':
                response = executeInMainThreadWithResult(
                    _eval, arg)
            else:
                code =  mayaserver.INVALID_METHOD
                response = func
            pickled = json.dumps([code, response])
        except Exception:
            pickled = json.dumps([
                mayaserver.UNHANDLED_ERROR,
                ''.join(traceback.format_exc())])
        sock.send(pickled)
