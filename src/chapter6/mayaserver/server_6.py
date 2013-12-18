import json
import logging
import traceback
import zmq

logger = logging.getLogger(__name__)

def runserver(hndshkPort):
    sock = zmq.Context().socket(zmq.REP)
    realport = sock.bind_to_random_port('tcp://127.0.0.1')
    logger.info('Handshaking on %s, sending %s',
                hndshkPort, realport)

    hndshkSock = zmq.Context().socket(zmq.REQ)
    hndshkSock.connect('tcp://127.0.0.1:%s' % hndshkPort)
    hndshkSock.send(str(realport))
    hndshkSock.recv() # acknowledgement
    logger.info('Handshake finished, looping.')

    while True:
        recved = sock.recv()
        func, arg = json.loads(recved)
        logger.debug('Recved: %s', recved)
        try:
            if func == 'exec':
                exec arg in globals(), globals()
                response = None
            elif func == 'eval':
                response = eval(arg, globals(), globals())
            logger.debug('Sending: %s', response)
            pickled = json.dumps([200, response])
        except Exception:
            logger.exception('Error!')
            pickled = json.dumps([500, ''.join(traceback.format_exc())])
        sock.send(pickled)
