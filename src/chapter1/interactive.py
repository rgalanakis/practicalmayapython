import maya.standalone
maya.standalone.initialize(name='python')

import maya.cmds as cmds
import pymel.core as pmc


def interactive():
    """
    Code for all the interactive prompts throughout the chapter.

    >>> import sys
    >>> for p in sys.path:
    ...     print p

    >>> import minspect
    >>> minspect
    <module 'minspect' from 'C:\Maya\site-packages\minspect.py'>

    >>> import minspect
    >>> reload(minspect)
    >>> minspect.syspath()

    >>> import pymel.core as pmc
    >>> shape, xform = pmc.polySphere()

    >>> type(xform)
    <type 'Transform'>
    >>> type(shape)
    <type 'Shape'>

    >>> dir(xform)

    >>> getattr(xform, 'getShape')
    <bound method Transform.getShape of <Transform instance at 0x0>>
    >>> getattr(xform, 'translate')
    <Attribute instance at 0x0>

    >>> import inspect
    >>> allattrs = [getattr(xform, a) for a in dir(xform)]
    >>> [a for a in allattrs if inspect.ismethod(a)]
    [TODO: <methods>]
    >>> [a for a in allattrs if isinstance(a, pmc.Attribute)]
    [TODO: <attributes>]

    >>> j = pmc.joint()
    >>> j.type()
    'joint'
    >>> type(j)
    <typepymel.nodetypes.Joint>
    >>> type(j).__bases__
    ((type pymel.nodetypes.Transform),)

    >>> type(j).__mro__
    [TODO]

    >>> type(xform)
    <type Transform>
    >>> type(xform).__mro__
    [Transform, DagNode, ..., DependNode, PyNode, ProxyUnicode]
    >>> type(x.translate)
    Attribute
    >>> type(x.translate).__mro__
    [Attribute, PyNode, ProxyUnicode]

    >>> type(j).__mro__
    [Joint, Transform, DagNode, DependNode, PyNode, ProxyUnicode]

    >>> xform.translate
    Attribute
    >>> t = t.translate.get()
    >>> t
    [0, 0, 0]

    >>> str(t)  # Calls 't.__str__()', which returns a simple
                # string representation of an object.
    [0, 0, 0]
    >>>t # Same as str(t)
    [0, 0, 0]
    >>> repr(t)  # Calls 't.__repr__()', which returns a
                 # more in-depth representation.
    Vector(0, 0, 0)

    >>> for c in t:
    ...     print c
    0
    0
    0

    >>> t[0], t[1], t[2]
    (0, 0, 0)

    >>> [1, 2, 3] + [4, 5, 6] # Regular Python lists
    [1, 2, 3, 4, 5, 6]
    >>> repr(t + [1, 2, 3])
    Vector(1, 2, 3)

    >>> t.x  # Familiar name-based access
    1
    >>> t.length()
    0.5

    >>> reload(minspect)
    >>> minspect.test_pyToHelpStr() (6)
    #### TODO: Assertion error (7)

    >>> reload(minspect).test_pyToHelpStr()
    TODO: Traceback line

    >>> import pymel.core.nodetypes
    >>> pymel.core.nodetypes.__name__
    'pymel.core.nodetypes'

    >>> import types
    >>> type(pymel.core.nodetypes) == types.ModuleType
    True

    >>> reload(minspect).test_pyToHelpStr()
    TODO: Traceback error line

    >>> type(pmc.nodetypes.Joint)
    TODO: <type>
    >>> pmc.nodetypes.Joint.__name__
    'Joint'
    >>> pmc.nodetypes.Joint.__module__
    'pymel.core.nodetypes'

    >>>classUserDefined(object): pass
    >>>classNotUserDefined(list): pass
    >>> isinstance(UserDefined(), types.Instance)
    True
    >>> isinstance(NotUserDefined(), types.Instance)
    False

    >>> joint = pmc.nodetypes.Joint()
    >>> type(joint.children)
    <type 'instancemethod'>
    >>> isinstance(joint.children, types.MethodType)

    >>> classMyClass(object):
    ... def mymethod(self):
    ...     pass
    ... @classmethod
    ... def myclassmethod(cls):
    ...     pass
    ... @staticmethod
    ... def mystaticmethod():
    ....    pass

    >>> MyClass().mymethod.im_self
    <__main__.MyClass object as 0x0xxxx>
    >>> MyClass().mymethod.im_class
    <class '__main__.MyClass'>
    >>> MyClass().mymethod.im_func
    <functionmymethod at 0x000>

    >>> def spam():
    ...     def eggs():
    ...         pass
    ...     pass

    >>> get10 = lambda: 10
    >>> type(get10)
    <type 'function'>
    >>> class MyClass(object):
    ...     @staticmethod
    ...     def mystaticmethod():
    ...         pass
    >>> type(MyClass.mystaticmethod)
    <type 'function'>
    >>> type(MyClass().mystaticmethod)
    <type 'function'>

    >>> import mhelp
    >>> mhelp.pmhelp('joint') # Will open a browser and search for "joint"
    >>> mhelp.pmhelp(pmcpmcpmc) # Will open a browser to the pymel.core module page.
    >>> mhelp.pmhelp(1) # Will print out help for integers.
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()
