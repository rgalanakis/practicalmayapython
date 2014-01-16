import unittest
import pymel.core as pmc

def is_almost_equal(seq1, seq2):
    for s1, s2 in zip(seq1, seq2):
        if abs(s1 - s2) > 0.000001:
            return False
    return True


class Base(unittest.TestCase):

    pluginname = None

    def setUp(self):
        self.nodes = []
        pmc.loadPlugin(self.pluginname)

    def tearDown(self):
        pmc.delete(self.nodes)
        pmc.flushUndo()
        pmc.unloadPlugin(self.pluginname)

    def createNode(self, name):
        n = pmc.createNode(name)
        self.nodes.append(n)
        return n

    def assertTrans(self, xform, ideal):
            got = list(xform.translate.get())
            self.assertTrue(
                is_almost_equal(got, ideal), '%s != %s' % (got, ideal))

class CirclerTests(Base):

    pluginname = 'circlernode_final.py'

    def make_circler_nodes(self):
        spherexform = pmc.polySphere()[0]
        spherexform.translate.set([44, 55, 66])
        circler = self.createNode('circler')
        pmc.PyNode('time1').outTime.connect(circler.input)
        circler.outSine.connect(spherexform.translateX)
        circler.outCosine.connect(spherexform.translateY)
        return spherexform, circler

    def testCircler(self):
        xform, circ = self.make_circler_nodes()
        circ.scale.set(4)
        circ.frames.set(12)
        pmc.currentTime(3)
        self.assertTrans(xform, [4, 0, 66])
        pmc.currentTime(6)
        self.assertTrans(xform, [0, -4, 66])


class ApiStyleCirclerTests(CirclerTests):
    pluginname = 'circlernode_apistyle.py'


class OtherPluginTests(Base):
    pluginname = 'otherplugin.py'

    def testOtherDemo(self):
        n = self.createNode('otherdemo')

        self.assertEqual(n.string.get(), 'hi')
        n.string.set('world')
        self.assertEqual(n.string.get(), 'world')

        self.assertEqual(n.enum.get(), 1)
        n.enum.set(2)
        self.assertEqual(n.enum.get(), 2)

        self.assertEqual(list(n.color.get()), [0, 0, 0])
        n.color.set([20, 30, 40])
        self.assertEqual(list(n.color.get()), [20, 30, 40])

    def testTransform(self):
        n = self.createNode('transformdemo')

        self.assertEqual(list(n.translate.get()), [0, 0, 0])
        n.translate.set([1, 2, 3])
        self.assertEqual(list(n.translate.get()), [1, 2, 3])


if __name__ == '__main__':
    unittest.main()
