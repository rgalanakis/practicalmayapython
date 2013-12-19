"""Add timeouts."""
import json, zmq, mayaserver
from client_4 import create_client, start_process, SETCMD

import time

class TimeoutError(Exception):
    pass


def sendrecv(socket, data, timeoutS=10.0):
    socket.send(json.dumps(data))
    starttime = time.time()
    while True:
        try:
            recved = socket.recv(zmq.NOBLOCK)
            break
        except zmq.ZMQError as ex:
            if ex.errno != zmq.EAGAIN:
                raise
            if time.time() - starttime > timeoutS:
                raise TimeoutError()
            time.sleep(timeoutS / 50.0)

    code, response = json.loads(recved)
    if code == mayaserver.SUCCESS:
        return response
    if code == mayaserver.UNHANDLED_ERROR:
        raise RuntimeError(response)
    assert code == mayaserver.INVALID_METHOD
    raise RuntimeError('Sent invalid method to server: %s' % response)


if __name__ == '__main__':
    SETCMD('_exceptions')
    start_process()
    sock = create_client()
    sendrecv(sock, ('exec', 'import time'))
    try:
        sendrecv(sock, ('exec', 'time.sleep(5)'), .1)
        print 'Did not time out :('
    except TimeoutError:
        print 'Timed out successfully!'
        sock = create_client()
    sendrecv(sock, ('eval', '1 + 1'))
    print 'And recovered successfully!'
