"""Add exception handling support."""
import json

from client_3 import start_process, create_client, SETCMD, kill

import mayaserver

def sendrecv(socket, data):
    tosend = json.dumps(data)
    socket.send(tosend)
    recved = socket.recv()
    code, response = json.loads(recved)
    if code == mayaserver.SUCCESS:
        return response
    if code == mayaserver.UNHANDLED_ERROR:
        raise RuntimeError(response)
    assert code == mayaserver.INVALID_METHOD
    raise RuntimeError('Sent invalid method to server: %s' % response)


if __name__ == '__main__':
    SETCMD('_exceptions')
    proc = start_process()
    sock = create_client()
    try:
        sendrecv(sock, ('spam', ''))
    except RuntimeError as ex:
        print 'Got indended error!', ex
    try:
        sendrecv(sock, ('eval', 'a + b'))
    except RuntimeError as ex:
        print 'Got indended error!', ex
    print 'Shutting down.'
    kill(proc.pid)
