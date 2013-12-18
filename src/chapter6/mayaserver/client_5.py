"""Add atexit (lifetime management)."""
import os
import subprocess
from client_2 import create_client, MAYAEXE, MAYAPYLIB
from client_4 import sendrecv

VERSION = '_4'

import atexit

def start_process():
    script = 'python("import mayaserver.server%s;mayaserver.server%s.runserver()");' % (VERSION, VERSION)
    environ = dict(os.environ)
    pypath = environ.get('PYTHONPATH', '')
    environ['PYTHONPATH'] = os.pathsep.join([pypath, MAYAPYLIB])
    proc = subprocess.Popen([MAYAEXE, '-command', script], env=environ)
    atexit.register(proc.kill)
    return proc

if __name__ == '__main__':
    p = start_process()
    try:
        sock = create_client()
        got = sendrecv(sock, ('eval', 'a + b'))
        print 'Got: %r' % got
    except Exception as ex:
        print 'Error!'
        print ex.args[0]
