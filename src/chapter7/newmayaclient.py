import os, sys
libdir = os.path.join(os.path.dirname(__file__), '', '..', 'chapter6')
os.environ['PYTHONPATH'] += os.pathsep + libdir
sys.path.append(libdir)

import zmq
import mayaserver.client as oldmayaclient

class MayaAutomationClient(object):
    def __init__(self): #(1)
        self.realport = oldmayaclient.start_process()
        self.reqsock = self._create_client()

    def _create_client(self):
        return oldmayaclient.create_client(self.realport)

    def sendrecv(self, *args, **kwargs): #(2)
        try: #(3)
            return oldmayaclient.sendrecv(
                self.reqsock, *args, **kwargs)
        except zmq.Again:
            self.reqsock = self._create_client()
            raise


def testit():
    """
>>> import newmayaclient
>>> cl = newmayaclient.MayaAutomationClient()
>>> cl.sendrecv(('eval', '1 + 1'))
2
    """
if __name__ == '__main__':
    import doctest
    doctest.testmod()
