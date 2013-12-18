import json
import zmq
import pymel.core as pmc

def runserver():
    sock = zmq.Context().socket(zmq.REP)
    sock.bind('tcp://127.0.0.1:5454')
    while True:
        recv = json.loads(sock.recv())
        version = pmc.about(version=True)
        sock.send(json.dumps('Pinged. Version: %s' % version))
