import json
import traceback
import zmq
import mayaserver


def runserver(handshake_port):
    sock = zmq.Context().socket(zmq.REP)
    realport = sock.bind_to_random_port('tcp://127.0.0.1')

    handshakesock = zmq.Context().socket(zmq.REQ)
    handshakesock.connect('tcp://127.0.0.1:%s' % handshake_port)
    handshakesock.send(str(realport))
    handshakesock.recv() # acknowledgement
    # ... server loop is the same ...

    while True:
        recved = sock.recv()
        func, arg = json.loads(recved)
        try:
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
