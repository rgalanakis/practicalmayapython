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
    sock = zmq.Context().socket(zmq.REP)
    sock.bind('tcp://127.0.0.1:5557')
    while True:
        request = json.loads(sock.recv())
        func, args = request
        a, b = args
        if func == '+':
            response = a + b
        elif func == '-':
            response = a - b
        sock.send(json.dumps(response))


def client3():
    sock = zmq.Context().socket(zmq.REQ)
    sock.connect('tcp://127.0.0.1:5557')
    for op in '+', '-':
        sock.send(json.dumps([op, (2, 3)]))
        response = json.loads(sock.recv())
        print 'Client3 got', repr(response)


def loop4():

    sock = zmq.Context().socket(zmq.REP)
    sock.bind('tcp://127.0.0.1:5558')

    import traceback # (1)
    while True:
        recved = sock.recv()
        try:
            func, args = json.loads(recved)
            a, b = args
            if func == '+':
                response = a + b
                code = 1 #(2)
            elif func == '-':
                response = a - b
                code = 1 #(2)
            else: #(3)
                code = 2
                response = 'Invalid method: ' + func
            pickled = json.dumps([code, response])
        except Exception: #(4)
            code = 3
            response = ''.join(traceback.format_exc())
            pickled = json.dumps([code, response])
        sock.send(pickled)


def client4():
    sock = zmq.Context().socket(zmq.REQ)
    sock.connect('tcp://127.0.0.1:5558')
    sock.send(json.dumps(['+', (2, 3)]))
    code, response = json.loads(sock.recv())
    print 'Client4 got', code, response
    assert code == 0
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
