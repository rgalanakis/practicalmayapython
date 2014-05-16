from nodefactory_final import OpenMaya, OpenMayaMPx

import sys
sys.COMPUTES = []

# nodefactory.py

def create_attrmaker(
        attrspec, ln, sn,
        affectors=(), default=None):

    def createattr(nodeclass):
        fnattr = attrspec.createfnattr()
        attrobj = attrspec.create(fnattr, ln, sn)
        if default is not None:
            attrspec.setdefault(fnattr, default)

        isinput = not bool(affectors)
        fnattr.setWritable(isinput)
        fnattr.setStorable(isinput)

        nodeclass.addAttribute(attrobj)
        setattr(nodeclass, ln, attrobj)

        for affectedby in affectors:
            inattrobj = getattr(nodeclass, affectedby)
            nodeclass.attributeAffects(inattrobj, attrobj)
    return createattr


def create_node(nodespec, nodename, typeid, attrmakers): #(1)
    def compute(*_): #(2)
        sys.COMPUTES.append('hi') # REMOVE ME!
        print 'Compute not yet implemented.'
    methods = {'compute': compute}
    nodetype = type(nodename, nodespec.nodebase(), methods) #(3)
    tid = OpenMaya.MTypeId(typeid) #(4)
    def creator(): #(5)
        return OpenMayaMPx.asMPxPtr(nodetype())
    def init(): #(6)
        for makeattr in attrmakers:
            makeattr(nodetype)
    def register(plugin): #(7)
        nodespec.register(plugin, nodename, tid, creator, init)
    def deregister(plugin):
        nodespec.deregister(plugin, tid)
    return register, deregister #(8)


# end nodefactory.py

# circlernode.py

from nodefactory_final import (
    NT_DEPENDSNODE, A_FLOAT, #create_attrmaker, create_node
)
_deregister_funcs = [] #(1)
def floatattr(*args, **kwargs): #(2)
    return create_attrmaker(A_FLOAT, *args, **kwargs)
def register_circler(fnplugin): #(3)
    inputnames = ['input', 'scale', 'frames']
    reg, dereg = create_node(
        NT_DEPENDSNODE, 'circler', 0x60005, [
            floatattr('input', 'in'),
            floatattr('scale', 'sc', default=10.0),
            floatattr('frames', 'fr', default=48.0),
            floatattr('outSine', 'os', inputnames),
            floatattr('outCosine', 'oc', inputnames),
    ])
    reg(fnplugin)
    _deregister_funcs.append(dereg)

def _toplugin(mobject):
    return OpenMayaMPx.MFnPlugin(mobject, 'Marcus Reynir', '0.01')
def initializePlugin(mobject):
    register_circler(_toplugin(mobject)) #(4)
def uninitializePlugin(mobject):
    plugin = _toplugin(mobject) #(5)
    for func in _deregister_funcs:
        func(plugin)
