import maya.standalone
maya.standalone.initialize(name='python')

import maya.cmds as cmds
import pymel.core as pmc


def interactive():
    """
    Code for all the interactive prompts throughout the chapter.

    >>> mynode = cmds.joint()

    >>> cmds.listConnections(mynode, type='transform')
    []
    >>> cmds.listConnections(mynode, exactType='transform')
    []
    >>> cmds.listConnections(mynode, containerType='cont')
    []
    >>> cmds.listConnections(mynode, type='transform', containerType='cont')
    Traceback:

    >>> cmds.ls(type='transform')
    []
    >>> cmds.ls(exactType='transform')
    []
    >>> cmds.ls(containerType='cont')
    []

    >>> cmds.listRelatives(type='transform')
    []
    >>> cmds.listRelatives(exactType='transform')
    Traceback:

    >>> def get_all_root_joints():
    ...     roots = []
    ...     for jnt in pmc.ls(type='joint'):
    ...         if jnt.getParent() is None:
    ...             roots.append(jnt)
    ...     return roots

    >>> def is_root_joint(obj):
    ...     return obj.type() == 'joint' and obj.getParent() is None
    >>> all_roots = [o for o in pmc.ls() if is_root_joint(o)]
    >>> new_roots = [o for o in pmc.importFile(**...) if is_root_joint(o)]

    >>> all_roots = [o for o in pmc.ls() if is_root_joint(o)]
    >>> first_root = None
    >>> if all_roots:
    ...     first_root = all_roots[0]
    >>> first_root
    Joint1

    >>> def first_or_default(sequence, default=None):
    ...     for item in sequence:
    ...         return item
    ...     return default

    >>> first_or_default([o for o in pmc.ls() if is_root_joint(o)])
    Joint1

    >>> def first_or_default(sequence, predicate=None, default=None):
    ...     for item in sequence:
    ...         if predicate is None or predicate(item):
    ...             return item
    ...     return default

    >>> first_or_default(pmc.ls(), is_root_joint)
    Joint1

    >>> first_or_default([1, 2, 3])
    1
    >>> first_or_default([], default='hi!')
    hi!

    >>> [i + 1 for i in [1, 2, 3]]
    [2, 3, 4]
    >>> [i for i in [1, 2, 3] if i > 2]
    [3]
    >>> [(i, chr(i)) for i in [65, 66, 67]]
    [(64, 'A'), (65, 'B'), (66, 'C')]

    >>> map(lambda i: i + 1, [1, 2, 3])
    [2, 3, 4]
    >>> filter(lambda i: i > 2, [1, 2, 3])
    [3]

    >>> filter(is_root_joint, pmc.ls())
    Joint1
    >>> [o for o in pmc.ls() if is_root_joint(o)]
    Joint1

    >>> import minspect
    >>> minspect.syspath()

    >>> import os, shutil, minspect
    >>> py = os.path.splitext(minspect.__file__)[0] + '.py'
    >>> shutil.move(py, '~/practicalmayapython/pylib')
    >>> pyc = os.path.splitext(minspect.__file__)[0] + '.pyc'
    >>> os.remove(pyc)

    >>> val = [1]
    >>> d1 = {'a': val}
    >>> d2 = dict(d1) # Make the copy
    >>> id(d1) == id(d2)
    False
    >>> id(d1['a']) == id(d2['a'])
    True

    >>> import skeletonutils
    >>> map(skeletonutils.convert_to_skeleton, pmc.selection())

    >>> items = [1, 2, 3]
    >>> stritems = [str(i) for i in items]
    >>> stritems
    ['1', '2', '3']
    >>> ', '.join(stritems)
    '1, 2, 3'

    >>> import namespaceutils
    >>> with namespaceutils.as_current(o.parentNamespace()):
    ...     pmc.joint() # Created in o's namespace.

    >>> j = pmc.joint()
    >>> c = pmc.camera()
    >>> c.translate.x.connect(j.translate.x)
    >>> [r for r in j.listRelatives() if minspect.isExactType(j, 'camera')]
    [Camera]
    >>> iscam = minspect.TypeFilterer('camera', True)
    >>> [r for r in j.listRelatives() if iscam(r)]
    [Camera]

    >>> def spam(pynode):
    ...     parent = pynode.getParent()
    ...     for i in range(ONE_MILLION):
    ...         parent.somethingSlow(i)
    ...     return parent
    >>> def spam(pynode):
    ...     parent = pynode.getParent().longName()
    ...     for i in range(ONE_MILLION):
    ...         maya.cmds.somethingSlow(parent, i)
    ...     return pmc.PyNode(parent)
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()
