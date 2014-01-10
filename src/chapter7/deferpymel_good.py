from maya import cmds, OpenMayaMPx

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

# ... other code is the same ...

def initializePlugin(mobject):
    plugin = _toplugin(mobject)
    def register():
        import pymel.core as pmc
        plugin.registerCommand(plugin_name, create_plugin)
    cmds.evalDeferred(register)


# # pymel.core : Updating pymel with pre-loaded plugins: deferpymel, fbxmaya, objExport
