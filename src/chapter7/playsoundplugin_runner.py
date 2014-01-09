
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

def pluginrunner():
    """
>>> import pymel.core as pmc

>>> patch_loadunload()

>>> import time
>>> pmc.loadPlugin('playsoundplugin_1.py')
>>> pmc.playSound()
>>> time.sleep(2)
>>> pmc.unloadPlugin('playsoundplugin_1.py')

>>> import time
>>> pmc.loadPlugin('playsoundplugin_2.py')
>>> pmc.playSound()
>>> time.sleep(2)
>>> pmc.playSound(wavname='gorilla')
>>> time.sleep(2)
>>> pmc.unloadPlugin('playsoundplugin_2.py')

    """

if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
