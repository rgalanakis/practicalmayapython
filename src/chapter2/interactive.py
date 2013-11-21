import maya.standalone
maya.standalone.initialize(name='python')

import pymel.core as pmc

def deleteall():
    pmc.newFile(f=True)

def interactive():
    """
    Code for all the interactive prompts throughout the chapter.

>>> import maya.cmds as cmds
>>> j1 = cmds.joint()
>>> j2 = cmds.joint()
>>> cmds.setParent(j2, j1) #doctest: +SKIP

>>> cmds.ls(type='transform')
[...u'joint1', u'joint2'...]
>>> cmds.ls(exactType='joint')
[u'joint1', u'joint2']

>>> cmds.listConnections(j1, type='transform')
[u'joint2']
>>> cmds.listConnections(j1, exactType='transform')
Traceback (most recent call last):
TypeError: Invalid arguments for flag 'exactType'.  Expected int, got str

>>> cmds.listConnections(j1, type='joint', exactType=True)
[u'joint2']

>>> cmds.listRelatives(j1, type='joint')
[u'joint2']
>>> cmds.listRelatives(j1, exactType='transform')
Traceback (most recent call last):
TypeError: Invalid flag 'exactType'

>>> import pymel.core as pmc
>>> pmc.delete(pmc.ls(type='joint'))

>>> j1 = pmc.joint()
>>> j2 = pmc.joint()
>>> import minspect
>>> [o for o in pmc.listConnections(j1)
...  if minspect.is_exact_type(o, 'joint')]
[nt.Joint(u'joint2')]

>>> import os
>>> import sys
>>> def say(s, use_stdout=True, stream=None):
...     if stream is None:
...         if use_stdout:
...             stream = sys.stdout
...         else:
...             stream = sys.stderr
...     stream.write(s + os.linesep)

>>> # Someone needs a simple debug printer to stdout
>>> say('hi') #doctest: +SKIP
>>> # Someone needed to print to stderr, so adds a flag.
>>> say('hi', use_stdout=True) #doctest: +SKIP
>>> # Someone needed an arbitrary stream, so adds support.
>>> say('hi', use_stdout=True, stream=None) #doctest: +SKIP

>>> def get_all_root_joints():
...     roots = []
...     for jnt in pmc.ls(type='joint'):
...         if jnt.getParent() is None:
...             roots.append(jnt)
...     return roots
>>> get_all_root_joints()
[nt.Joint(u'joint1')]

>>> def is_root_joint(obj):
...     return obj.type() == 'joint' and obj.getParent() is None
>>> all_roots = [o for o in pmc.ls() if is_root_joint(o)]
>>> new_roots = [o for o in pmc.importFile(some_file_path)
...             if is_root_joint(o)] #doctest: +SKIP

>>> all_roots = [o for o in pmc.ls() if is_root_joint(o)]
>>> first_root = None
>>> if all_roots:
...     first_root = all_roots[0]
>>> first_root
nt.Joint(u'joint1')

>>> def first_or_default(sequence, default=None):
...     for item in sequence:
...         return item  # Return the first item
...     return default  # Return default if no items

>>> first_root = first_or_default(
...     o for o in pmc.ls() if is_root_joint(o))
>>> first_root
nt.Joint(u'joint1')

>>> def first_or_default(sequence, predicate=None, default=None):
...     for item in sequence:
...         if predicate is None or predicate(item):
...             return item
...     return default

>>> first_root = first_or_default(pmc.ls(), is_root_joint)
>>> first_root
nt.Joint(u'joint1')

>>> first_or_default([1, 2, 3])
1
>>> first_or_default([], default='hi!')
'hi!'

>>> s = 'hi!'
>>> [c.upper() for c in s if c.isalpha()]
['H', 'I']

>>> [i + 1 for i in [1, 2, 3]]
[2, 3, 4]
>>> [i for i in [1, 2, 3] if i > 2]
[3]
>>> [(i, chr(i)) for i in [65, 66, 67]]
[(65, 'A'), (66, 'B'), (67, 'C')]

>>> map(lambda i: i + 1, [1, 2, 3])
[2, 3, 4]
>>> filter(lambda i: i > 2, [1, 2, 3])
[3]

>>> filter(is_root_joint, pmc.ls())
[nt.Joint(u'joint1')]
>>> [o for o in pmc.ls() if is_root_joint(o)]
[nt.Joint(u'joint1')]

>>> def spam(adjective):
...     return adjective + ' spam'
>>> def spamneggs(adjective):
...     return spam(adjective) + ' + eggs'
>>> spamneggs('Boring')
'Boring spam + eggs'

>>> def spamneggs(adjective):
...     def spam(adjective):
...         return adjective + ' spam'
...     return spam(adjective) + ' + eggs'
>>> spamneggs('Decent')
'Decent spam + eggs'

>>> def spamneggs(adjective):
...     def spam():
...         return adjective + ' spam'
...     return spam() + ' + eggs'
>>> spamneggs('Wonderful')
'Wonderful spam + eggs'

>>> deleteall()

>>> j1 = pmc.joint(name='J1')
>>> j2 = pmc.joint(name='J2')
>>> j3 = pmc.joint(name='J3')
>>> import skeletonutils
>>> skeletonutils.ancestors(j1)
[]
>>> skeletonutils.ancestors(j3)
[nt.Joint(u'J2'), nt.Joint(u'J1')]

>>> reload(skeletonutils) #doctest: +SKIP
>>> skeletonutils.uniqueroots([j1, j2])
[nt.Joint(u'J1')]
>>> skeletonutils.uniqueroots([j2])
[nt.Joint(u'J2')]

>>> deleteall()

>>> objs = pmc.joint(), pmc.polySphere(), pmc.camera()
>>> [o for o in pmc.ls() if minspect.is_exact_type(o, 'camera')]
[...nt.Camera(u'cameraShape1')]
>>> [o for o in pmc.ls() if minspect.is_type(o, 'transform')]
[...nt.Joint(u'joint1'), nt.Transform(u'pSphere1'), nt.Transform(u'camera1')]

>>> deleteall()

>>> j1, j2 = pmc.joint(), pmc.joint()
>>> j2.translateX.set(10)
>>> [j for j in pmc.ls(type='joint') if j.translateX.get() > 0]
[nt.Joint(u'joint2')]

>>> def head(sequence, count):
...     result = []
...     for item in sequence:
...         if len(result) == count:
...             break
...         result.append(item)
...     return result
>>> head(pmc.ls(), 2)
[nt.Time(u'time1'), nt.SequenceManager(u'sequenceManager1')]

>>> def tail(sequence, count):
...     result = list(sequence)
...     return result[-count:]
>>> tail(pmc.ls(), 2)
[nt.Joint(u'joint1'), nt.Joint(u'joint2')]

>>> deleteall()

>>> objs = pmc.joint(), pmc.joint()
>>> def remove_selected_slow(objs):
...     return [item for item in objs if item not in pmc.selected()]
>>> pmc.select(objs[0])
>>> remove_selected_slow(objs)
[nt.Joint(u'joint2')]

>>> def remove_selected_faster(objs):
...     selected = pmc.selected()
...     return [item for item in objs if item not in selected]
>>> pmc.select(objs[0])
>>> remove_selected_faster(objs)
[nt.Joint(u'joint2')]

>>> def get_hierarchy_slow(typename):
...     node = pmc.createNode(typename)
...     result = node.nodeType(inherited=True)
...     pmc.delete(node)
...     return result
>>> get_hierarchy_slow('joint')
[u'containerBase', u'entity', u'dagNode', u'transform', u'joint']

>>> _hierarchy_cache = {}
>>> def get_hierarchy_fast(typename):
...     result = _hierarchy_cache.get(typename)
...     if result is None:
...         node = pmc.createNode(typename)
...         result = node.nodeType(inherited=True)
...         pmc.delete(node)
...         _hierarchy_cache[typename] = result
...     return result
>>> get_hierarchy_fast('joint')
[u'containerBase', u'entity', u'dagNode', u'transform', u'joint']

>>> deleteall()

>>> def add_influences_slow(cl, infls):
...     for infl in infls:
...         cl.addInfluence(infl)
>>> def add_influences_fast(cl, infls):
...     cl.addInfluence(infls)
>>> j1 = pmc.joint()
>>> cluster = pmc.skinCluster(j1, pmc.polyCube()[0])[0]
>>> add_influences_slow(cluster, [pmc.joint(), pmc.joint()])
>>> add_influences_fast(cluster, [pmc.joint(), pmc.joint()])

"""


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
