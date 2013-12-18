import zmq


def process_request(request):
    return request


def loop1():
    sock = zmq.Context().socket(zmq.REP)
    sock.bind('tcp://127.0.0.1:5555')
    while True:
        request = sock.recv()
        response = process_request(request)
        sock.send(response)


def client1():
    sock = zmq.Context().socket(zmq.REQ)
    sock.connect('tcp://127.0.0.1:5555')
    for i in range(3):
        sock.send(str(i))
        response = sock.recv()
        print 'Client1 got', repr(response)


import json

def loop2():
    sock = zmq.Context().socket(zmq.REP)
    sock.bind('tcp://127.0.0.1:5556')
    while True:
        request = json.loads(sock.recv())
        response = process_request(request)
        sock.send(json.dumps(response))


def client2():
    sock = zmq.Context().socket(zmq.REQ)
    sock.connect('tcp://127.0.0.1:5556')
    for i in range(3):
        sock.send(json.dumps(i))
        response = json.loads(sock.recv())
        print 'Client2 got', repr(response)


def loop3():
    import operator

    sock = zmq.Context().socket(zmq.REP)
    sock.bind('tcp://127.0.0.1:5557')
    while True:
        request = json.loads(sock.recv())
        methodname, args = request
        if methodname == '+':
            func = operator.add
        elif methodname == '-':
            func = operator.sub
        response = func(*args)
        sock.send(json.dumps(response))


def client3():
    sock = zmq.Context().socket(zmq.REQ)
    sock.connect('tcp://127.0.0.1:5557')
    for op in '+', '-':
        sock.send(json.dumps([op, (2, 3)]))
        response = json.loads(sock.recv())
        print 'Client3 got', repr(response)


def loop4():
    import logging
    logger = logging.getLogger(__name__)
    import operator
    import traceback

    sock = zmq.Context().socket(zmq.REP)
    sock.bind('tcp://127.0.0.1:5558')
    def doloop():
        request = json.loads(sock.recv())
        methodname, args = request
        if methodname == '+':
            func = operator.add
        elif methodname == '-':
            func = operator.sub
        try:
            response = func(*args)
            pickled = json.dumps([200, response])
        except Exception:
            response = ''.join(traceback.format_exc())
            pickled = json.dumps([500, response])
        sock.send(pickled)
    while True:
        try:
            doloop()
        except Exception:
            # send email to admins
            logger.exception('Unhandled error!')


def client4():
    sock = zmq.Context().socket(zmq.REQ)
    sock.connect('tcp://127.0.0.1:5558')
    sock.send(json.dumps(['+', (2, 3)]))
    code, response = json.loads(sock.recv())
    print 'Client4 got', code, response
    assert code == 200
    assert response == 5
    sock.send(json.dumps(['+', (2, '0')]))
    code, response = json.loads(sock.recv())
    assert code == 500
    assert 'Traceback' in response
    print 'Client4 got', code, response


import sys
import threading

if __name__ == '__main__':
    for loop, client in [
        (loop1, client1),
        (loop2, client2),
        (loop3, client3),
        (loop4, client4),
    ]:
        threading.Thread(target=loop).start()
        client()
        print
    sys.exit(0)
