"""Run this with a testrunner in a vanilla Python (not mayapy!)."""

from mayatestcase import MayaTestCase


class FooTests(MayaTestCase):

    def testPass(self):
        self.assertTrue(True)

    def testFail(self):
        # This should raise an assertion error on the client
        self.assertFalse(True)
