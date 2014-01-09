from maya import OpenMayaMPx
import pymel.core as pmc

pluginName = 'zeroPosition'

class temporarily_disable_undo(object):
    def __enter__(self):
        self.orig = pmc.undoInfo(stateWithoutFlush=True, q=True)
        pmc.undoInfo(stateWithoutFlush=False)
    def __exit__(self, *_):
        pmc.undoInfo(stateWithoutFlush=self.orig)


class ZeroOutSelected(OpenMayaMPx.MPxCommand):
    def doIt(self, args):
        self.objs = pmc.selected(type='transform')
        self.originals = [list(n.translate.get()) for n in self.objs]
        self.redoIt()

    def redoIt(self):
        with temporarily_disable_undo():
            for o in self.objs:
                o.translate.set(0, 0, 0)

    def undoIt(self):
        with temporarily_disable_undo():
            for o, pos in zip(self.objs, self.originals):
                o.translate.set(*pos)

    def isUndoable(self):
        return True


def createPlugin():
    return OpenMayaMPx.asMPxPtr(ZeroOutSelected())

def _toplugin(mobject):
    return OpenMayaMPx.MFnPlugin(
        mobject, 'Marcus Reynir', '0.01')

def initializePlugin(mobject):
    plugin = _toplugin(mobject)
    plugin.registerCommand(pluginName, createPlugin)

def uninitializePlugin(mobject):
    plugin = _toplugin(mobject)
    plugin.deregisterCommand(pluginName)
