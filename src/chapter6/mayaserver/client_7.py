"""Add handshake support and logging."""

import atexit, os, subprocess, zmq
from client_1 import MAYAEXE, kill
from client_2 import SETCMD
from client_6 import sendrecv

COMMAND = ('python("import mayaserver.server;'
           'mayaserver.server.runserver(%s)");') #(1)

ORIGCOMMAND = COMMAND
COMMAND = SETCMD('_handshake', COMMAND)

def start_process():
    handshakesock = zmq.Context().socket(zmq.REP) #(2)
    handshakeport = handshakesock.bind_to_random_port(
        'tcp://127.0.0.1')
    command = COMMAND % handshakeport #(3)
    process = subprocess.Popen(
        [MAYAEXE, '-command', command]) #(4)
    atexit.register(kill, process)
    appport = int(handshakesock.recv()) #(5)
    handshakesock.send('')
    handshakesock.close() #(6)
    return appport #(7)

def create_client(port): #(8)
    socket = zmq.Context().socket(zmq.REQ)
    socket.connect('tcp://127.0.0.1:%s' % port)
    return socket


if __name__ == '__main__':
    def start_and_get_pid():
        appport = start_process()
        sock = create_client(appport)
        sendrecv(sock, ('exec', 'import os'))
        return sendrecv(sock, ('eval', 'os.getpid()'))
    srv1Pid = start_and_get_pid()
    srv2Pid = start_and_get_pid()
    print 'Client proc %s started Maya procs: %s, %s' % (
        os.getpid(), srv1Pid, srv2Pid)
