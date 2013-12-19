"""
Adds a simple client/server and process management.

- how to kill a process.
- send the -command argument to Maya.
- create a client
- sendrecv
"""
import atexit
import json
import subprocess
import zmq

from client_1 import MAYAEXE, kill

# We do this so we can have the string here for copying,
# but override it in code. See _ORIG_COMMAND
COMMAND = ('python("import mayaserver.server;'
           'mayaserver.server.runserver()");') #(1)

def start_process():
    process = subprocess.Popen(
        [MAYAEXE, '-command', COMMAND]) # (2)
    atexit.register(kill, process.pid)
    return process

_ORIG_COMMAND = COMMAND
def SETCMD(suffix, orig=_ORIG_COMMAND):
    global COMMAND
    COMMAND = orig.replace('.server', '.server' + suffix)
    return COMMAND

def create_client():
    socket = zmq.Context().socket(zmq.REQ)
    socket.connect('tcp://127.0.0.1:5454')
    return socket

def sendrecv(socket, data):
    tosend = json.dumps(data)
    socket.send(tosend)
    recved = socket.recv()
    unpickrecved = json.loads(recved)
    return unpickrecved


if __name__ == '__main__':
    SETCMD('_pingable')
    proc = start_process()
    sock = create_client()
    got = sendrecv(sock, 'Ping')
    print 'Got: %r. Shutting down.' % got
