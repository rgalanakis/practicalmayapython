import json #(1)
import zmq

def runserver(): #(2)
    sock = zmq.Context().socket(zmq.REP)
    sock.bind('tcp://127.0.0.1:5454') #(3)
    while True: #(4)
        recv = json.loads(sock.recv())
        sock.send(json.dumps('Pinged with %s' % recv))
