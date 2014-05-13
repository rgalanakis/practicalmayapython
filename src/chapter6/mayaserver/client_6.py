"""Add timeouts."""
import json, zmq, mayaserver
from client_4 import create_client, start_process, SETCMD

import time #(1)

def sendrecv(socket, data, timeoutSecs=10.0): #(2)
    socket.send(json.dumps(data))
    starttime = time.time() #(3)
    while True: #(4)
        try:
            recved = socket.recv(zmq.NOBLOCK) #(5)
            break #(6)
        except zmq.Again: #(7)
            if time.time() - starttime > timeoutSecs: #(8)
                raise
            time.sleep(0.1) #(9)

    code, response = json.loads(recved) #(10)
    # ...same code as before...

    if code == mayaserver.SUCCESS:
        return response
    if code == mayaserver.UNHANDLED_ERROR:
        raise RuntimeError(response)
    if code == mayaserver.INVALID_METHOD:
        raise RuntimeError('Sent invalid method: %s' % response)
    raise RuntimeError('Unhandled response: %s, %s' % (
        code, response))


if __name__ == '__main__':
    SETCMD('_exceptions')
    start_process()
    sock = create_client()
    sendrecv(sock, ('exec', 'import time')) #(1)
    try:
        sendrecv(sock, ('exec', 'time.sleep(5)'), .1) #(2)
    except zmq.Again:
        print 'Timed out successfully!'
        sock = create_client() #(3)
    sendrecv(sock, ('eval', '1 + 1')) #(4)
    print 'And recovered successfully!'
