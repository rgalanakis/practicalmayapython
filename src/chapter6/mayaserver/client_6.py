"""Add handshake support and logging."""
import atexit, os, subprocess, zmq
from client_2 import MAYAPYLIB, MAYAEXE
from client_5 import sendrecv

def start_server_and_connect():
    hndshkSock = zmq.Context().socket(zmq.REP)
    hndshkPort = hndshkSock.bind_to_random_port('tcp://127.0.0.1')
    script = ('python("import mayaserver.server_6;mayaserver.server_6.runserver(%s)");' % hndshkPort)
    def startproc():
        environ = dict(os.environ)
        pypath = environ.get('PYTHONPATH', '')
        environ['PYTHONPATH'] = os.pathsep.join([pypath, MAYAPYLIB])
        proc = subprocess.Popen([MAYAEXE, '-command', script], env=environ)
        atexit.register(proc.kill)
    startproc()
    reqPort = int(hndshkSock.recv())
    hndshkSock.send('')
    hndshkSock.close()

    reqSock = zmq.Context().socket(zmq.REQ)
    reqSock.connect('tcp://127.0.0.1:%s' % reqPort)
    return reqSock


if __name__ == '__main__':
    def start_and_get_pid():
        sock = start_server_and_connect()
        sendrecv(sock, ('exec', 'import os'))
        return sendrecv(sock, ('eval', 'os.getpid()'))
    srv1Pid = start_and_get_pid()
    srv2Pid = start_and_get_pid()
    print 'Client proc %s started Maya procs: %s, %s' % (
        os.getpid(), srv1Pid, srv2Pid)
