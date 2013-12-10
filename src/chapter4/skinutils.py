import unittest

import pymel.core as pmc


class denormalized_skin_1(object):
    """Turns off skin cluster normalization and maintaining
    max influrnces."""
    def __init__(self, skinCl):
        self.skinCl = skinCl
        self.maxInfl, self.norm = None, None
    def __enter__(self):
        self.maxInfl = self.skinCl.maintainMaxInfluences.get()
        self.norm = self.skinCl.setNormalizeWeights(q=True)
        self.skinCl.maintainMaxInfluences.set(False)
        self.skinCl.setNormalizeWeights(0)
    def __exit__(self, *_):
        if self.maxInfl is not None:
            self.skinCl.maintainMaxInfluences.set(self.maxInfl)
        if self.norm is not None:
            self.skinCl.setNormalizeWeights(self.norm)


_denormalized_skins = set() #(1)
class denormalized_skin_2(object):
    """Turns off skin cluster normalization and maintaining
    max influrnces."""
    def __init__(self, skinCl):
        self.skinCl = skinCl
        self.maxInfl, self.norm = None, None
    def __enter__(self):
        if self.skinCl in _denormalized_skins: #(2)
            return
        _denormalized_skins.add(self.skinCl) #(3)
        self.maxInfl = self.skinCl.maintainMaxInfluences.get()
        self.norm = self.skinCl.setNormalizeWeights(q=True)
        self.skinCl.maintainMaxInfluences.set(False)
        self.skinCl.setNormalizeWeights(0)
    def __exit__(self, *_):
        _denormalized_skins.discard(self.skinCl) #(4)
        if self.maxInfl is not None: #(5)
            self.skinCl.maintainMaxInfluences.set(self.maxInfl)
        if self.norm is not None:
            self.skinCl.setNormalizeWeights(self.norm)


denormalized_skin = denormalized_skin_2

def swap_influence_1(skinCl, vert, inflA, inflB):
    """For a given vertex,
    swaps the weight between two influences."""
    valA = pmc.skinPercent(skinCl, vert, q=True, t=inflA)
    valB = pmc.skinPercent(skinCl, vert, q=True, t=inflB)
    with denormalized_skin(skinCl):
        pmc.skinPercent(skinCl, vert, tv=[inflA, valB])
        pmc.skinPercent(skinCl, vert, tv=[inflB, valA])

def swap_influence_2(skinCl, vert, inflA, inflB):
    """For a given vertex,
    swaps the weight between two influences."""
    with denormalized_skin(skinCl):
        swap_influence_fast(skinCl, vert, inflA, inflB)

def swap_influence_fast(skinCl, vert, inflA, inflB):
    """For a given vertex,
    swaps the weight between two influences.
    `skinCl` should be denormalized before calling this function.
    See `denormalized_skin`.
    """
    valA = pmc.skinPercent(skinCl, vert, q=True, t=inflA)
    valB = pmc.skinPercent(skinCl, vert, q=True, t=inflB)
    pmc.skinPercent(skinCl, vert, tv=[inflA, valB])
    pmc.skinPercent(skinCl, vert, tv=[inflB, valA])


class Tests(unittest.TestCase):

    def setUp(self):
        for t in 'joint', 'skinCluster', 'polyPlane':
            for o in pmc.ls(type=t):
                if pmc.objExists(o):
                    pmc.delete(o)

    def _testSwap(self, func, swap):
        global denormalized_skin
        denormalized_skin = func
        joints = [
            pmc.joint(p=(-3.0, 0.0,-12.0)),
            pmc.joint(p=(-3.0, 0.0, -5.0)),
            pmc.joint(p=(1.0, 0.0, 5.5)),
            pmc.joint(p=(6.0, 0.0, 10.0))]
        plane = pmc.polyPlane(w=20.0,h=20.0,sx=25,sy=25)[0]
        cl = pmc.skinCluster(joints, plane)[0]
        def getweight(ind):
            return pmc.skinPercent(cl, plane.vtx[0], q=True, t=joints[ind])
        self.assertEqual(getweight(0), 0.0)
        self.assertEqual(getweight(1), 0.5)
        swap(cl, plane.vtx[0], joints[0], joints[1])
        self.assertEqual(getweight(0), 0.5)
        self.assertEqual(getweight(1), 0.0)

    def testDenorm1Swap1(self):
        self._testSwap(denormalized_skin_1, swap_influence_1)

    def testDenorm1Swap2(self):
        self._testSwap(denormalized_skin_1, swap_influence_2)

    def testDenorm2Swap2(self):
        self._testSwap(denormalized_skin_2, swap_influence_2)


if __name__ == '__main__':
    unittest.main()
