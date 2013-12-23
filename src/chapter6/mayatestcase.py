"""This is a really rough implementation but demonstrates the
core ideas."""

import os
import unittest
try:
    import maya
    ISMAYA = True
except ImportError:
    maya, ISMAYA = None, False

from mayaserver.client import start_process, create_client, sendrecv

class MayaTestCase(unittest.TestCase):

    def _setUp(self):
        cls = self.__class__
        if hasattr(cls, '_setupRan'):
            return

        cls.reqport = start_process()
        cls.reqsock =  create_client(cls.reqport)
        appendstr = 'import sys; sys.path.append(%r)' % (
            os.path.dirname(__file__))
        sendrecv(cls.reqsock, ('exec', appendstr))
        cls.testmodule = cls.__module__
        cls.testalias = cls.testmodule.replace('.', '_')
        impstr = 'import %s as %s' % (cls.testmodule, cls.testalias)
        sendrecv(cls.reqsock, ('exec', impstr))
        MayaTestCase._setupRan = True

    def run(self, result=None):
        if ISMAYA:
            unittest.TestCase.run(self, result)
            return

        def wrappedTest():
            self.__testMethodName = self._testMethodName
            try:
                self._wrappedTest()
            finally:
                self._testMethodName = self.__testMethodName
        self.setUp = lambda: None
        self.tearDown = lambda: None
        self._setUp()
        setattr(self, self._testMethodName, wrappedTest)
        unittest.TestCase.run(self, result)

    def _wrappedTest(self):
        strargs = dict(testmodule=self.testalias,
            testcase=self.__class__.__name__,
            testfunc=self._testMethodName)
        teststr = """tc = {testmodule}.{testcase}("{testfunc}")
try:
    tc.setUp()
    tc.{testfunc}()
finally:
    tc.tearDown()""".format(**strargs)
        try:
            sendrecv(self.reqsock, ('exec', teststr))
        except RuntimeError as ex:
            if 'AssertionError' in str(ex):
                raise AssertionError(*ex.args)
            raise
