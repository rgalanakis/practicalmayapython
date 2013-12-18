"""Adds exec and eval support (with execution scopes)."""

import client_2
client_2.VERSION = '_3'
from client_2 import start_process, create_client, sendrecv

if __name__ == '__main__':
    p = start_process()
    sock = create_client()
    goteval = sendrecv(sock, ('eval', '1 + 1'))
    print 'Got Eval: %r' % goteval
    sendrecv(sock, ('exec', 'a = 3'))
    sendrecv(sock, ('exec', 'a *= 2'))
    gotexec = sendrecv(sock, ('eval', 'a'))
    print 'Got Exec: %r' % gotexec

    print 'Shutting down.'
    p.kill()
