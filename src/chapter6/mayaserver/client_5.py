"""Add atexit."""
import os
import subprocess

from client_2 import MAYAEXE, MAYAPYLIB, SETCMD, create_client, kill
from client_4 import sendrecv
COMMAND = SETCMD('_exceptions')

import atexit


def start_process():
    environ = dict(os.environ)
    pypath = environ.get('PYTHONPATH', '')
    environ['PYTHONPATH'] = os.pathsep.join([pypath, MAYAPYLIB])
    process = subprocess.Popen(
        [MAYAEXE, '-command', COMMAND], env=environ)
    atexit.register(kill, process.pid) #(1)
    return process

if __name__ == '__main__':
    start_process()
    sock = create_client()
    sendrecv(sock, ('eval', 'a + b'))
