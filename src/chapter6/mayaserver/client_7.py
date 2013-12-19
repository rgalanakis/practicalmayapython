"""Add handshake support and logging."""

import atexit, os, subprocess, zmq
from client_2 import MAYAPYLIB, MAYAEXE, SETCMD
from client_6 import TimeoutError, sendrecv

COMMAND = ('python("import mayaserver.server;'
           'mayaserver.server.runserver(%s)");') #(1)

COMMAND = SETCMD('_handshake', COMMAND)

def start_server_and_socketgetter():
    handshakesock = zmq.Context().socket(zmq.REP)
    handshakeport = handshakesock.bind_to_random_port('tcp://127.0.0.1')
    script = COMMAND % handshakeport
    def startproc():
        environ = dict(os.environ)
        pypath = environ.get('PYTHONPATH', '')
        environ['PYTHONPATH'] = os.pathsep.join([pypath, MAYAPYLIB])
        process = subprocess.Popen([MAYAEXE, '-command', script], env=environ)
        atexit.register(process.kill)
    startproc()
    realport = int(handshakesock.recv())
    handshakesock.send('')
    handshakesock.close()

    def create_realsock():
        realsock = zmq.Context().socket(zmq.REQ)
        endpoint = 'tcp://127.0.0.1:%s' % realport
        realsock.connect(endpoint)
        return realsock
    return create_realsock


if __name__ == '__main__':
    def start_and_get_pid():
        getsock = start_server_and_socketgetter()
        sock = getsock()
        sendrecv(sock, ('exec', 'import os'))
        return sendrecv(sock, ('eval', 'os.getpid()'))
    srv1Pid = start_and_get_pid()
    srv2Pid = start_and_get_pid()
    print 'Client proc %s started Maya procs: %s, %s' % (
        os.getpid(), srv1Pid, srv2Pid)
    createsock = start_server_and_socketgetter()
    sock = createsock()
    sendrecv(sock, ('exec', 'import time'))
    try:
        sendrecv(sock, ('exec', 'time.sleep(5)'), .1)
        print 'Did not time out :('
    except TimeoutError:
        print 'Timed out successfully!'
        sock = createsock()
    sendrecv(sock, ('eval', '1 + 1'))
    print 'And recovered successfully!'
