
def interactive():
    """
Code for all the interactive prompts throughout the chapter.

>>> import myset
>>> s1 = myset.MySet()
>>> s2 = myset.MySet()
>>> s1.add(1)
>>> s2.add('a')
>>> s1.items()
[1]
>>> s2.items()
['a']

>>> myset.MySet.__dict__
[...('__init__', <function __init__ at 0x...>),
 ('__module__', 'myset'),
 ('add', <function add at 0x...>),
 ('items', <function items at 0x...>),
 ('remove', <function remove at 0x...>)]
>>> s = myset.MySet()
>>> s.__dict__
{'_state': {}}

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
>>> joint = OpenMayaAnim.MFnIkJoint() #(1)
>>> joint.create()
>>> joint.setDegreesOfFreedom(True, False, True) #(2)
>>> utils = [OpenMaya.MScriptUtil() for su in range(3)] #(3)
>>> ptrs = [su.asBoolPtr() for su in utils] #(4)
>>> joint.getDegreesOfFreedom(*ptrs) #(5)
>>> [OpenMaya.MScriptUtil.getBool(ptr) for ptr in ptrs] #(6)
[1, 0, 1]

>>> import pymel.core, os
>>> for p in os.getenv('MAYA_PLUG_IN_PATH').split(os.pathsep):
...     print p
/Users/rgalanakis/Library/Preferences/Autodesk/maya/plug-ins
/Users/Shared/Autodesk/maya/plug-ins
    """

if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)

ignore = """
> value = False;
> Print(value);
False
> MakeTrue(&value);
> Print(value);
True
"""

ignore2 = """
face_to_vert_inds_and_normals = {
    face0_id: [
        [vert0_index, vert1_index, vert2_index],
        [vert0_norm, vert1_norm, vert2_norm]
    ],
    face1_id: [
        [vert1_index, vert2_index, vert3_index],
        [vert1_norm, vert2_norm, vert3_norm]
    ],
    ...
}
"""
