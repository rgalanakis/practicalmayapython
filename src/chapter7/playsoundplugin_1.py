from maya import OpenMayaMPx #(1)
import playsound

class SoundPlayer(OpenMayaMPx.MPxCommand): #(2)
    def doIt(self, args): #(3)
        playsound.play_sound(playsound.GOBBLE)

def create_plugin(): #(4)
    return OpenMayaMPx.asMPxPtr(SoundPlayer())

plugin_name = 'playSound' #(5)

def _toplugin(mobject): #(6)
    return OpenMayaMPx.MFnPlugin(
        mobject, 'Marcus Reynir', '0.01')

def initializePlugin(mobject): #(7)
    plugin = _toplugin(mobject)
    plugin.registerCommand(plugin_name, create_plugin)

def uninitializePlugin(mobject): #(8)
    plugin = _toplugin(mobject)
    plugin.deregisterCommand(plugin_name)
