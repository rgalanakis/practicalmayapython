
def patch_loadunload():
    import pymel.core as pmc
    oldload = pmc.loadPlugin
    oldunload = pmc.unloadPlugin
    def load(*args):
        oldload(*args)
    def unload(*args):
        oldunload(*args)
    pmc.loadPlugin = load
    pmc.unloadPlugin = unload
""
def pluginrunner():
    """
>>> import pymel.core as pmc

>>> patch_loadunload()

>>> pmc.loadPlugin('zerooutplugin.py')
>>> j = pmc.joint()
>>> j.translate.set(10, 10, 10)
>>> pmc.zeroPosition()
>>> j.translate.get()
dt.Vector([0.0, 0.0, 0.0])
>>> pmc.undo()
>>> j.translate.get()
dt.Vector([10.0, 10.0, 10.0])
>>> pmc.unloadPlugin('zerooutplugin.py')
    """

if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
