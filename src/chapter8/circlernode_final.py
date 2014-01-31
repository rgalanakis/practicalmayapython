import math
from maya import OpenMayaMPx
from nodefactory_final import (
    NT_DEPENDSNODE, A_FLOAT, create_attrmaker, create_node
)

_deregister_funcs = []
def floatattr(*args, **kwargs):
    return create_attrmaker(A_FLOAT, *args, **kwargs)
def make_transformer(mathfunc):
    def inner(input, scale, frames):
        angle = 6.2831853 * (input / frames)
        return mathfunc(angle) * scale
    return inner
sin = make_transformer(math.sin)
cosine = make_transformer(math.cos)

def register_circler(plugin):
    inputnames = ['input', 'scale', 'frames']
    reg, dereg = create_node(
        NT_DEPENDSNODE, 'circler', 0x60005,
        [
            floatattr('input', 'in'),
            floatattr('scale', 'sc', default=10.0),
            floatattr('frames', 'fr', default=48.0),
            floatattr('outSine', 'so',
                affectors=inputnames,
                transformer=sin),
            floatattr('outCosine', 'co',
                affectors=inputnames,
                transformer=cosine),
        ])
    reg(plugin)
    _deregister_funcs.append(dereg)

def _toplugin(mobject):
    return OpenMayaMPx.MFnPlugin(
        mobject, 'Marcus Reynir', '0.01')

def initializePlugin(mobject):
    plugin = _toplugin(mobject)
    register_circler(plugin)

def uninitializePlugin(mobject):
    plugin = _toplugin(mobject)
    for func in _deregister_funcs:
        func(plugin)
