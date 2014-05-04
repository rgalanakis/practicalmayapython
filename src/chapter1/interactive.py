import pymel.core as pmc

def deleteall():
    pmc.newFile(f=True)

def interactive():
    """
Code for all the interactive prompts throughout the chapter.

>>> print 'Hello, Maya!'
Hello, Maya!
>>> def hello():
...     return 'Hello, Maya!'
...
>>> hello()
'Hello, Maya!'

>>> import sys
>>> for p in sys.path:
...     print p #doctest: +SKIP
C:\Program Files\Autodesk\Maya2013\bin\python26.zip
C:\Program Files\Autodesk\Maya2013\Python\DLLs
C:\Program Files\Autodesk\Maya2013\Python\lib
C:\Program Files\Autodesk\Maya2013\Python\lib\plat-win
C:\Program Files\Autodesk\Maya2013\Python\lib\lib-tk
C:\Program Files\Autodesk\Maya2013\bin
C:\Program Files\Autodesk\Maya2013\Python
C:\Program Files\Autodesk\Maya2013\Python\lib\site-packages

>>> import sys
>>> 'C:\\mayapybook\\pylib' in sys.path #doctest: +SKIP
True
>>> import minspect
>>> minspect
<module 'minspect' from '...\minspect.py'>

>>> import sys
>>> '~/mayapybook/pylib' in sys.path #doctest: +SKIP
True
>>> import minspect
>>> minspect #doctest: +SKIP
<module 'minspect' from '.../minspect.py'>

>>> import minspect
>>> reload(minspect)
<module 'minspect' from '...\minspect.py'>
>>> minspect.syspath() #doctest: +SKIP
C:\Program Files\Autodesk\Maya2013\bin\python26.zip
C:\Program Files\Autodesk\Maya2013\Python\DLLs
C:\Program Files\Autodesk\Maya2013\Python\lib
C:\Program Files\Autodesk\Maya2013\Python\lib\plat-win
C:\Program Files\Autodesk\Maya2013\Python\lib\lib-tk
C:\Program Files\Autodesk\Maya2013\bin
C:\Program Files\Autodesk\Maya2013\Python
C:\Program Files\Autodesk\Maya2013\Python\lib\site-packages

>>> import maya.standalone
>>> maya.standalone.initialize()
>>> import pymel.core as pmc
>>> xform, shape = pmc.polySphere()

>>> type(xform)
<class 'pymel.core.nodetypes.Transform'>
>>> type(shape)
<class 'pymel.core.nodetypes.PolySphere'>

>>> dir(xform)
['LimitType', 'MAttrClass', ..., 'zeroTransformPivots']

>>> getattr(xform, 'getShape')
<bound method Transform.getShape of nt.Transform(u'pSphere1')>
>>> getattr(xform, 'translate')
Attribute(u'pSphere1.translate')

>>> import inspect
>>> methods = []
>>> for a in dir(xform):
...     attr = getattr(xform, a)
...     if inspect.ismethod(attr):
...         methods.append(attr)
>>> attrs = xform.listAttr()
>>> methods
[<bound method Transform.__add__ of nt.Transform(u'pSphere1')>, ...]
>>> attrs
[Attribute(u'pSphere1.message'), ...]

>>> type([])
<type 'list'>
>>> type(type([]))
<type 'type'>
>>> type(xform)
<class 'pymel.core.nodetypes.Transform'>

>>> pmc.joint()
nt.Joint(u'joint1')
>>> pmc.polySphere()
[nt.Transform(u'pSphere2'), nt.PolySphere(u'polySphere2')]
>>> pmc.ls(type='joint')
[nt.Joint(u'joint1')]
>>> pmc.ls(type='transform')
[...nt.Joint(u'joint1'), nt.Transform(u'pSphere1'), ...]
>>> pmc.ls(type='shape')
[...nt.Mesh(u'pSphereShape1'), ...]

>>> j = pmc.joint()
>>> j.type()
u'joint'
>>> type(j)
<class 'pymel.core.nodetypes.Joint'>
>>> type(j).__bases__
(<class 'pymel.core.nodetypes.Transform'>,)
>>> j.translate, j.rotate
(Attribute(u'joint2.translate'), Attribute(u'joint2.rotate'))

>>> type(j).__mro__
(<class 'pymel.core.nodetypes.Joint'>, <class 'pymel.core.nodetypes.Transform'>, <class 'pymel.core.nodetypes.DagNode'>, <class 'pymel.core.nodetypes.Entity'>, <class 'pymel.core.nodetypes.ContainerBase'>, <class 'pymel.core.nodetypes.DependNode'>, <class 'pymel.core.general.PyNode'>, <class 'pymel.util.utilitytypes.ProxyUnicode'>, <type 'object'>)

>>> reload(minspect)
<module 'minspect' from '...\minspect.py'>
>>> minspect.info(xform)
Info for pSphere1
Attributes:
  pSphere1.message
  pSphere1.caching
  ...
MEL type: transform
MRO:
  Transform
  DagNode
  Entity
  ContainerBase
  DependNode
  PyNode
  ProxyUnicode
  object

>>> type(xform).__mro__
(<class 'pymel.core.nodetypes.Transform'>, <class 'pymel.core.nodetypes.DagNode'>, <class 'pymel.core.nodetypes.Entity'>, <class 'pymel.core.nodetypes.ContainerBase'>, <class 'pymel.core.nodetypes.DependNode'>, <class 'pymel.core.general.PyNode'>, <class 'pymel.util.utilitytypes.ProxyUnicode'>, <type 'object'>)
>>> type(xform.translate).__mro__
(<class 'pymel.core.general.Attribute'>, <class 'pymel.core.general.PyNode'>, <class 'pymel.util.utilitytypes.ProxyUnicode'>, <type 'object'>)

>>> type(pmc.joint()).__mro__
(<class 'pymel.core.nodetypes.Joint'>, <class 'pymel.core.nodetypes.Transform'>, ..., <type 'object'>)

>>> xform.translate
Attribute(u'pSphere1.translate')
>>> t = xform.translate.get()
>>> print t
[0.0, 0.0, 0.0]

>>> vect = xform.translate.get()
>>> lst = [0.0, 0.0, 0.0]
>>> str(vect)
'[0.0, 0.0, 0.0]'
>>> str(lst)
'[0.0, 0.0, 0.0]'
>>> print t, lst # The print implicitly calls str(t)
[0.0, 0.0, 0.0] [0.0, 0.0, 0.0]
>>> repr(t) # repr returns a more detailed string for an object
'dt.Vector([0.0, 0.0, 0.0])'
>>> repr(lst)
'[0.0, 0.0, 0.0]'

>>> t = xform.translate.get()
>>> for c in t:
...     print c
0.0
0.0
0.0

>>> t[0], t[1], t[2]
(0.0, 0.0, 0.0)

>>> [1, 2, 3] + [4, 5, 6] # Regular Python lists
[1, 2, 3, 4, 5, 6]
>>> repr(t + [1, 2, 3])
'dt.Vector([1.0, 2.0, 3.0])'

>>> t.x += 5 # Familiar name-based access
>>> t.y += 2
>>> t.x
5.0
>>> t.length() # And helpers!
5.385...

>>> def move_along_x(xform, vec):
...     t = xform.translate.get()
...     t[0] += vec[0]
...     xform.translate.set(t)
>>> j = pmc.joint()
>>> move_along_x(j, [1, 0, 0])
>>> j.translate.get()
dt.Vector([1.0, 0.0, 0.0])
>>> move_along_x(j, j.translate.get())
>>> j.translate.get()
dt.Vector([2.0, 0.0, 0.0])

>>> pmc.joint
<function joint at 0x0...>
>>>

>>> help
Type help() for interactive help, or help(object) for help about object.

>>> import minspect # (1)
>>> reload(minspect)
<module 'minspect' from '...\minspect.py'>
>>> minspect.test_py_to_helpstrFAIL() # (2)
Traceback (most recent call last):
AssertionError: ...

>>> reload(minspect).test_py_to_helpstrFAIL()
Traceback (most recent call last):
AssertionError: ...

>>> import pymel.core.nodetypes
>>> pymel.core.nodetypes.__name__
'pymel.core.nodetypes'

>>> import types
>>> isinstance(pymel.core.nodetypes, types.ModuleType)
True

>>> reload(minspect).test_py_to_helpstrFAIL()
Traceback (most recent call last):
AssertionError: ...

>>> pmc.nodetypes.Joint
<class 'pymel.core.nodetypes.Joint'>
>>> pmc.nodetypes.Joint.__name__
'Joint'
>>> pmc.nodetypes.Joint.__module__
'pymel.core.nodetypes'

>>> class UserDefined(object): pass
>>> class NotUserDefined: pass
>>> isinstance(UserDefined(), types.InstanceType)
False
>>> isinstance(NotUserDefined(), types.InstanceType)
True

>>> joint = pmc.nodetypes.Joint()
>>> type(joint.getTranslation)
<type 'instancemethod'>
>>> isinstance(joint.getTranslation, types.MethodType)
True

>>> class MyClass(object):
...     def mymethod(self):
...         pass
...     @classmethod # (1)
...     def myclassmethod(cls):
...         pass
...     @staticmethod # (2)
...     def mystaticmethod():
...         pass
>>> MyClass().mymethod # (3)
<bound method MyClass.mymethod of <__main__.MyClass object at...
>>> MyClass.mymethod # (4)
<unbound method MyClass.mymethod>

>>> MyClass().mymethod.im_self
<__main__.MyClass object at 0x0...>
>>> MyClass().mymethod.im_class
<class '__main__.MyClass'>
>>> MyClass().mymethod.im_func
<function mymethod at 0x0...>

>>> def spam():
...     def eggs():
...         pass
...     pass

>>> get10 = lambda: 10
>>> type(get10)
<type 'function'>
>>> class MyClass(object):
...     @staticmethod
...     def mystaticmethod(): pass
>>> type(MyClass.mystaticmethod)
<type 'function'>
>>> type(MyClass().mystaticmethod)
<type 'function'>

>>> obj = None

# Version 1
>>> module = None
>>> if isinstance(obj, types.ModuleType):
...     module = obj.__name__

# Version 2
>>> module = None
>>> if hasattr(obj, '__name__'):
...     module = obj.__name__

# Version 3
>>> module = getattr(obj, '__name__', None)

# Version 4
>>> try:
...     module = obj.__name__
... except AttributeError:
...     module = None

>>> import minspect
>>> reload(minspect)
<module 'minspect' from '...\minspect.py'>

# Comment the below line to launch a browser.
>>> minspect.webbrowser.open = lambda *_: None

>>> # Will open a browser and search for "joint"
>>> minspect.pmhelp('joint')
>>> # Will open a browser to the pymel.core.nodetypes module page.
>>> minspect.pmhelp(pmc.nodetypes)
>>> # Will print out help for integers.Help on int object:
>>> minspect.pmhelp(1)
Help on int object:
<BLANKLINE>
class int(object)
 |  int(x[, base]) -> integer
...

>>> pmc.select(pmc.joint())
>>> exec "import pymel.core as pmc; import minspect;minspect.pmhelp(pmc.selected()[0])"
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
