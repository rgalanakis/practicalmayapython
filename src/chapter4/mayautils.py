import pymel.core as pmc
import maya.cmds as cmds


class undo_chunk(object):
    def __enter__(self):
        pmc.undoInfo(openChunk=True)
    def __exit__(self, *_):
        pmc.undoInfo(closeChunk=True)


def chunk_undo(func):
    def inner(*args, **kwargs):
        pmc.undoInfo(openChunk=True)
        try:
            return func(*args, **kwargs)
        finally:
            pmc.undoInfo(closeChunk=True)
    return inner


def preserve_selection(func):
    def inner(*args, **kwargs): #(1)
        sel = list(pmc.selected()) #(2)
        result = func(*args, **kwargs) #(3)
        pmc.select(sel, replace=True) #(4)
        return result #(5)
    return inner #(6)


pmc.superExporter = lambda *_: None

@preserve_selection
def export_char_meshes(path):
    objs = [o for o in pmc.ls(type='mesh') 
            if '_char_' in o.name()]
    pmc.select(objs)
    pmc.superExporter(path)


class undo_on_error(object):
    def __enter__(self):
        pmc.undoInfo(openChunk=True)
    def __exit__(self, exc_type, exc_val, exc_tb):
        pmc.undoInfo(closeChunk=True)
        if exc_val is not None:
            pmc.undo()


class set_file_prompt(object):
    def __init__(self, state):
        self.state = state
        self.oldstate = None
    def __enter__(self):
        self.oldstate = cmds.file(q=True, prompt=True)
        cmds.file(prompt=self.state)
    def __exit__(self, *_):
        if self.oldstate is not None:
            cmds.file(prompt=self.oldstate)


class at_time(object):
    def __init__(self, t):
        self.t = t
        self.oldt = None
    def __enter__(self):
        self.oldt = pmc.getCurrentTime()
        pmc.setCurrentTime(self.t)
    def __exit__(self, *_):
        if self.oldt is not None:
            pmc.setCurrentTime(self.oldt)


class with_unit(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.oldlin, self.oldang, self.oldtim = None, None, None
    def __enter__(self):
        self.oldlin = pmc.currentUnit(q=True, linear=True)
        self.oldang = pmc.currentUnit(q=True, angle=True)
        self.oldtim = pmc.currentUnit(q=True, time=True)
        pmc.currentUnit(*self.args, **self.kwargs)
    def __exit__(self, *_):
        if self.oldlin is not None:
            pmc.currentUnit(linear=self.oldlin)
        if self.oldang is not None:
            pmc.currentUnit(angle=self.oldang)
        if self.oldtim is not None:
            pmc.currentUnit(time=self.oldtim)


class render_layer_active(object):
    def __init__(self, renderlayer):
        self.renderlayer = renderlayer
        self.orig_layer = None
    def __enter__(self):
        self.orig_layer = pmc.nodetypes.RenderLayer.currentLayer()
        self.renderlayer.setCurrent()
    def __exit__(self, *_):
        if self.orig_layer is not None:
            self.orig_layer.setCurrent()


class set_namespace_active(object):
    def __init__(self, ns):
        if ns == '':
            # This would be too ambiguous, so prohibit it
            raise ValueError('argument cannot be an empty string')
        self.ns = ns
        self.oldns = None
    def __enter__(self):
        self.oldns = pmc.namespaceInfo(currentNamespace=True)
        pmc.namespace(setNamespace=self.ns)
    def __exit__(self, *_):
        if self.oldns is not None:
            oldns = ':' + self.oldns.lstrip(':')
            pmc.namespace(setNamespace=oldns)

import unittest

class Tests(unittest.TestCase):
    def setUp(self):
        for m in pmc.ls(type='joint'):
            if pmc.objExists(m):
                pmc.delete(m)

    def testUndoChunk(self):
        with undo_chunk():
            pmc.joint(), pmc.joint()
        self.assertEqual(len(pmc.ls(type='joint')), 2)
        pmc.undo()
        self.assertFalse(pmc.ls(type='joint'))

    def testChunkUndo(self):
        @chunk_undo
        def spam():
            pmc.joint(), pmc.joint()
        spam()
        self.assertEqual(len(pmc.ls(type='joint')), 2)
        pmc.undo()
        self.assertFalse(pmc.ls(type='joint'))

    def testPreserveSelection(self):
        j1 = pmc.joint()
        j2 = pmc.joint()
        @preserve_selection
        def spam():
            pmc.select(j2)
            self.assertEqual(pmc.selected(), [j2])
        pmc.select(j1)
        spam()
        self.assertEqual(pmc.selected(), [j1])

    def testUndoOnError(self):
        def doit():
            with undo_on_error():
                pmc.joint()
                raise NotImplementedError()
        self.assertRaises(NotImplementedError, doit)
        self.assertFalse(pmc.ls(type='joint'))

    def testSetFilePrompt(self):
        cmds.file(prompt=False)
        with set_file_prompt(True):
            self.assertTrue(cmds.file(q=True, prompt=True))
        self.assertFalse(cmds.file(q=True, prompt=True))

    def testAtTime(self):
        pmc.setCurrentTime(1)
        with at_time(2):
            self.assertEqual(pmc.getCurrentTime(), 2)
        self.assertEqual(pmc.getCurrentTime(), 1)

    def testWithUnit(self):
        def assertUnit(kw, ideal):
            self.assertEqual(pmc.currentUnit(q=True, **{kw: True}), ideal)
        pmc.currentUnit(angle='rad')
        pmc.currentUnit(linear='cm')
        pmc.currentUnit(time='sec')
        with with_unit(angle='deg'):
            with with_unit(linear='m'):
                with with_unit(time='min'):
                    assertUnit('angle', 'deg')
                    assertUnit('linear', 'm')
                    assertUnit('time', 'min')
        assertUnit('angle', 'rad')
        assertUnit('linear', 'cm')
        assertUnit('time', 'sec')

    def testSetNamespace(self):
        self.assertRaises(ValueError, set_namespace_active, '')
        pmc.namespace(add='before')
        pmc.namespace(add='after')
        pmc.namespace(set='before')
        self.assertEqual('before', pmc.namespaceInfo(cur=True))
        with set_namespace_active(':after'):
            self.assertEqual('after', pmc.namespaceInfo(cur=True))
        self.assertEqual('before', pmc.namespaceInfo(cur=True))
        with set_namespace_active(':'):
            self.assertEqual(':', pmc.namespaceInfo(cur=True))
        self.assertEqual('before', pmc.namespaceInfo(cur=True))

    def testSetRenderLayer(self):
        cam1 = pmc.camera()[0]
        defaultlayer = pmc.nodetypes.RenderLayer.defaultRenderLayer()
        newlayer = pmc.createRenderLayer()
        defaultlayer.setCurrent()
        with render_layer_active(newlayer):
            cam2 = pmc.camera()[0]
            self.assertEqual(pmc.nodetypes.RenderLayer.currentLayer(), newlayer)
        self.assertEqual(pmc.nodetypes.RenderLayer.currentLayer(), defaultlayer)
        self.assertTrue(defaultlayer.inLayer(cam1))
        self.assertTrue(newlayer.inLayer(cam2))


if __name__ == '__main__':
    unittest.main()
