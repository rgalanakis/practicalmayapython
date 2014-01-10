from maya import OpenMayaMPx
import pymel.core

class DemoCommand(OpenMayaMPx.MPxCommand):
    pass

def create_plugin():
    return OpenMayaMPx.asMPxPtr(DemoCommand())

plugin_name = 'demoCommand'

def _toplugin(mobject):
    return OpenMayaMPx.MFnPlugin(
        mobject, 'Marcus Reynir', '0.01')

def uninitializePlugin(mobject):
    _toplugin(mobject).deregisterCommand(plugin_name)

def initializePlugin(mobject):
    plugin = _toplugin(mobject)
    plugin.registerCommand(plugin_name, create_plugin)


# // pymel.core : Updating pymel with pre-loaded plugins: deferpymel