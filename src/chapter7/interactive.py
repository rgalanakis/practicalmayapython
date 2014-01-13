
def interactive():
    """
Code for all the interactive prompts throughout the chapter.

# Show how modules are objects and how to make custom types/instances

>>> import myset
>>> myset.add(1)
>>> myset.add(2)
>>> myset.items()
[1, 2]
>>> myset.remove(3)
Traceback (most recent call last):
KeyError: 3
>>> myset.remove(2)
>>> myset.items()
[1]

>>> myset.__dict__
{...}

>>> import myset
>>> s = myset.MySet()
>>> s.add(1)
>>> s.add(2)
>>> s.items()
[1, 2]
>>> s.remove(3)
Traceback (most recent call last):
KeyError: 3
>>> s.remove(2)
>>> s.items()
[1]

>>> s1 = myset.MySet()
>>> s2 = myset.MySet()
>>> s1.add(1)
>>> s2.add('a')
>>> s1.items()
[1]
>>> s2.items()
['a']

# Show awfulness of API

>>> import pymel.core as pmc
>>> objname = 'myobj'
>>> _ = pmc.joint(name=objname)

>>> from maya import OpenMaya
>>> sellist = OpenMaya.MSelectionList()
>>> sellist.add(objname) #Can't initialize a list with items.
>>> mobj = OpenMaya.MObject()
>>> sellist.getDependNode(0, mobj) #Pass by reference
>>> jntdepnode = OpenMaya.MFnDependencyNode(mobj) #Function sets
>>> jntdepnode.name()
u'myobj'

## Name to OpenMaya node

>>> trans, shape = pmc.polyCube(name='mynode')

>>> pmc.PyNode('mynode')
nt.Transform(u'mynode')

>>> sellist = OpenMaya.MSelectionList() #(1)
>>> sellist.add('mynode') #(2)
>>> node = OpenMaya.MObject() #(3)
>>> sellist.getDependNode(0, node) #(4)
>>> node #(5)
<maya.OpenMaya.MObject; proxy of <Swig Object of type 'MObject...

## OpenMaya node to name

>>> pynode = trans
>>> mobject = node

>>> pynode.name()
u'mynode'

>>> OpenMaya.MFnDependencyNode(mobject).name()
u'mynode'

>>> p = pmc.PyNode('perspShape')
>>> p.__apimfn__()
<maya.OpenMaya.MFnCamera; proxy of <Swig Object of type 'MFnCa...
>>> p.__apimdagpath__()
<maya.OpenMaya.MDagPath; proxy of <Swig Object of type 'MDagPa...
>>> a = p.focalLength
>>> a
Attribute(u'perspShape.focalLength')
>>> a.__apimplug__()
<maya.OpenMaya.MPlug; proxy of <Swig Object of type 'MPlug *' ...

## Hash

>>> hash(pynode) #doctest: +SKIP
409350872
>>> OpenMaya.MObjectHandle(mobject).hashCode() #doctest: +SKIP
409350872


>>> from maya import OpenMaya, OpenMayaAnim
>>> joint = OpenMayaAnim.MFnIkJoint( #(1)
...     OpenMayaAnim.MFnIkJoint().create())
>>> joint.setDegreesOfFreedom(True, False, True) #(2)
>>> utils = [OpenMaya.MScriptUtil() for su in range(3)] #(3)
>>> ptrs = [su.asBoolPtr() for su in utils] #(4)
>>> joint.getDegreesOfFreedom(*ptrs) #(5)
>>> [OpenMaya.MScriptUtil.getBool(ptr) for ptr in ptrs] #(6)
[1, 0, 1]

    """

if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)

ignore = """
> value = new bool()
> print(value)
False
> makeTrue(value)
> print(value)
True
"""