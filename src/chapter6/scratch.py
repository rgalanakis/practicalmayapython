
import sys
import zmq

if sys.argv[-1] == 'client':
    print 'Client is going to send.'
    reqsock = zmq.Context().socket(zmq.REQ)
    reqsock.connect('tcp://127.0.0.1:5555')
    reqsock.send('Hello from client!')
    recv = reqsock.recv()
    print 'Client received', recv, 'exiting.'
else:
    print 'Server is listening.'
    repsock = zmq.Context().socket(zmq.REP)
    repsock.bind('tcp://127.0.0.1:5555')
    recv = repsock.recv()
    print 'Server received', recv
    repsock.send('Hello from server!')
    print 'Server sent, exiting.'
