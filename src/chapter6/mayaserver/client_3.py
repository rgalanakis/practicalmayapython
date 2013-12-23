"""
Exec and eval support (with execution scope)
is added to the server and hooked up here.
"""

from client_2 import start_process, create_client, sendrecv, SETCMD

if __name__ == '__main__':
    SETCMD('_sendrecv')
    proc = start_process()
    sock = create_client()
    goteval = sendrecv(sock, ('eval', '1 + 1'))
    print 'Got Eval: %r' % goteval
    sendrecv(sock, ('exec', 'a = 3'))
    sendrecv(sock, ('exec', 'a *= 2'))
    gotexec = sendrecv(sock, ('eval', 'a'))
    print 'Got Exec: %r' % gotexec

