"""Add timeouts."""
import atexit, json, os, subprocess, zmq
from client_2 import MAYAPYLIB, MAYAEXE
from client_5 import sendrecv

import time

class TimeoutError(Exception):
    pass

def sendrecv(sock, data, timeoutS=10):
    sock.send(json.dumps(data))

    starttime = time.time()
    while True:
        try:
            recved = sock.recv(zmq.NOBLOCK)
            break
        except zmq.ZMQError as ex:
            if ex.errno != zmq.EAGAIN:
                raise
            if time.time() - starttime > timeoutS:
                raise TimeoutError()
            time.sleep(timeoutS / 50.0)

    code, response = json.loads(recved)
    if code != 200:
        raise Exception(response)
    return response


if __name__ == '__main__':
    def start_and_get_pid():
        sock = start_server_and_connect()
        sendrecv(sock, ('exec', 'import os'))
        return sendrecv(sock, ('eval', 'os.getpid()'))
    srv1Pid = start_and_get_pid()
    srv2Pid = start_and_get_pid()
    print 'Client proc %s started Maya procs: %s, %s' % (
        os.getpid(), srv1Pid, srv2Pid)
