"""Add exception handling support."""
import json

from client_3 import start_process, create_client, SETCMD

import mayaserver #(1)

def sendrecv(socket, data):
    tosend = json.dumps(data)
    socket.send(tosend)
    recved = socket.recv()
    code, response = json.loads(recved) #(2)
    if code == mayaserver.SUCCESS: #(3)
        return response
    if code == mayaserver.UNHANDLED_ERROR: #(4)
        raise RuntimeError(response)
    if code == mayaserver.INVALID_METHOD: #(5)
        raise RuntimeError('Sent invalid method: %s' % response)
    raise RuntimeError('Unhandled response: %s, %s' % (
        code, response)) #(6)


if __name__ == '__main__':
    SETCMD('_exceptions')
    proc = start_process()
    sock = create_client()
    try:
        sendrecv(sock, ('spam', '')) #(7)
    except RuntimeError as ex:
        print 'Got intended error!', ex
    try:
        sendrecv(sock, ('eval', '1/0')) #(8)
    except RuntimeError as ex:
        print 'Got intended error!', ex
