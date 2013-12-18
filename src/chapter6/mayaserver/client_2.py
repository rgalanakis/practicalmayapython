"""Launches Maya with a startup command that will run the server.
Uses a basic 'Ping' command to get the Maya version.
Adds serialization.
Shows handle inheritance.
"""

VERSION = '_2'

import json
import os
import subprocess
import zmq

MAYAEXE = r'C:\Program Files\Autodesk\Maya 2011 Subscription Advantage Pack\bin\mayabatch.exe'#r'C:\Program Files\Autodesk\Maya2014\bin\maya.exe'
MAYAPYLIB = r'C:\pydev\practicalmayapython\src\chapter6'#r'C:\mayapybook\pylib'


def start_process():
    script = 'python("import mayaserver.server%s;mayaserver.server%s.runserver()");' % (VERSION, VERSION)
    environ = dict(os.environ)
    pypath = environ.get('PYTHONPATH', '')
    environ['PYTHONPATH'] = os.pathsep.join([pypath, MAYAPYLIB])
    proc = subprocess.Popen([MAYAEXE, '-command', script], env=environ)
    return proc

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
    p = start_process()
    sock = create_client()
    got = sendrecv(sock, 'Ping')
    print 'Got: %r. Shutting down.' % got
    p.kill()
