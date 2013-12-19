import json
import zmq


def runserver():
    sock = zmq.Context().socket(zmq.REP)
    sock.bind('tcp://127.0.0.1:5454')
    while True:
        recv = json.loads(sock.recv())
        sock.send(json.dumps('Pinged with %s' % recv))
