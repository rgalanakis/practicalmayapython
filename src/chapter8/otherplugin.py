from maya import OpenMayaMPx
import nodefactory_final as nodefactory

_deregister_funcs = []

def register_otherdemo(plugin):
    reg, dereg = nodefactory.create_node(
        nodefactory.NT_DEPENDSNODE, 'otherdemo', 0x60006,
        [
            nodefactory.create_attrmaker(
                nodefactory.A_COLOR, 'color', 'c'),
            nodefactory.create_attrmaker(
                nodefactory.A_ENUM, 'enum', 'e', default=1,
                fields=[
                    ['field1', 1],
                    ['field2', 2]]),
            nodefactory.create_attrmaker(
                nodefactory.A_STRING, 'string', 's', default='hi'),
        ])
    reg(plugin)
    _deregister_funcs.append(dereg)


def register_transformdemo(plugin):
    reg, dereg = nodefactory.create_node(
        nodefactory.NT_TRANSFORMNODE, 'transformdemo', 0x60007, [])
    reg(plugin)
    _deregister_funcs.append(dereg)


def _toplugin(mobject):
    return OpenMayaMPx.MFnPlugin(
        mobject, 'Marcus Reynir', '0.01')

def initializePlugin(mobject):
    plugin = _toplugin(mobject)
    register_otherdemo(plugin)
    register_transformdemo(plugin)

def uninitializePlugin(mobject):
    plugin = _toplugin(mobject)
    for func in _deregister_funcs:
        func(plugin)
