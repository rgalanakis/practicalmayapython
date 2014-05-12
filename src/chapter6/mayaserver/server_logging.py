import json
import zmq

import logging

log = logging.getLogger(__name__)

def runserver(handshake_port):
    sock = zmq.Context().socket(zmq.REP)
    appport = sock.bind_to_random_port('tcp://127.0.0.1')
    log.info('Handshaking on %s, sending %s',
             handshake_port, appport)
    # ... do handshake ...
    log.info('Handshake finished, looping.')
    while True:
        recved = json.loads(sock.recv())
        log.debug('recv: %s', recved)
        # ... request processing ...
        log.debug('send: %s', tosend)
        sock.send(json.dumps(tosend))
