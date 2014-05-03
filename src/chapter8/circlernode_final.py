import math
from maya import OpenMayaMPx
from nodefactory_final import (create_node, NT_DEPENDSNODE,
    float_input, float_output)

_deregister_funcs = []

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
            float_input('input', 'in'),
            float_input('scale', 'sc', default=10.0),
            float_input('frames', 'fr', default=48.0),

            float_output(
                'outSine', 'so',
                affectors=inputnames,
                transformer=sin),
            float_output(
                'outCosine', 'co',
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
