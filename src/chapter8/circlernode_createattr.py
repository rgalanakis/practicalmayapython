from nodefactory_final import A_FLOAT

# nodefactory.py

def create_attr(
        nodeclass, attrspec, ln, sn,
        affectors=(), default=None):
    fnattr = attrspec.createfnattr() #(1)
    attrobj = attrspec.create(fnattr, ln, sn) #(2)
    if default is not None:
        attrspec.setdefault(fnattr, default) #(3)

    isinput = not bool(affectors) #(4)
    fnattr.setWritable(isinput)
    fnattr.setStorable(isinput)

    nodeclass.addAttribute(attrobj) #(5)
    setattr(nodeclass, ln, attrobj) #(6)

    for affectedby in affectors: #(7)
        inattrobj = getattr(nodeclass, affectedby)
        nodeclass.attributeAffects(inattrobj, attrobj)

# end nodefactory.py

# duplicate bunch of shit so it works as a plugin
from circlernode_apistyle import create, Circler, nodeName, nodeTypeID, _toplugin
def initializePlugin(mobject):
    plugin = _toplugin(mobject)
    plugin.registerNode(nodeName, nodeTypeID, create, init)
def uninitializePlugin(mobject):
    plugin = _toplugin(mobject)
    plugin.deregisterNode(nodeTypeID)

# circlernode.py

#from nodefactory import create_attr, A_FLOAT

def init():
    create_attr(Circler, A_FLOAT, 'input', 'in')
    create_attr(Circler, A_FLOAT, 'scale', 'sc', default=10.0)
    create_attr(Circler, A_FLOAT, 'frames', 'fr', default=48.0)
    inputnames = ['input', 'scale', 'frames']
    create_attr(Circler, A_FLOAT, 'outSine', 'so', inputnames)
    create_attr(Circler, A_FLOAT, 'outCosine', 'co', inputnames)
