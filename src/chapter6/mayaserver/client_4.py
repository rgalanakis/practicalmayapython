"""Add exception handling support."""
import json

import client_2
client_2.VERSION = '_4'
from client_2 import start_process, create_client

def sendrecv(socket, data):
    tosend = json.dumps(data)
    socket.send(tosend)
    recved = socket.recv()
    code, response = json.loads(recved)
    if code != 200:
        raise Exception(response)
    return response

if __name__ == '__main__':
    p = start_process()
    try:
        sock = create_client()
        got = sendrecv(sock, ('eval', 'a + b'))
        print 'Got: %r' % got
    except Exception as ex:
        print 'Error!'
        print ex.args[0]
    finally:
        print 'Shutting down.'
        p.kill()
