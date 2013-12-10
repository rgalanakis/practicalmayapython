import sys
import pymel.core as pmc

def deleteall():
    for n in pmc.ls(type='joint') + pmc.ls(type='file'):
        pmc.delete(n)

def replacefiles():
    for f in pmc.ls(type='file'):
        pmc.delete(f)
    files = []
    for i in range(3):
        n = pmc.createNode('file')
        n.ftn.set('FTN%s' % i)
        files.append(n)
    files[1].ftn.lock()


def interactive():
    """
    Code for all the interactive prompts throughout the chapter.

>>> leftfoot = pmc.polySphere(name='left_foot')[0]
>>> leftfoot.translate.set(5, 0, 0)
>>> # ...other code that changes left_foot
>>> rightfoot = pmc.polySphere(name='right_foot')[0]
>>> rightfoot.translate.set(-5, 0, 0)
>>> # ...same code, but for right_foot

>>> def makefoot(prefix, x=1):
...     foot = pmc.polySphere(name=prefix + '_foot')[0]
...     foot.translate.set(5 * x, 0, 0)
...     # ...other code that changes foot
...     return foot
>>> leftfoot = makefoot('left', 1)
>>> rightfoot = makefoot('right', -1)

>>> pmc.undoInfo(openChunk=True)
>>> try:
...     leftfoot = makefoot('left', 1)
... finally:
...     pmc.undoInfo(closeChunk=True)
>>> pmc.undoInfo(openChunk=True)
>>> try:
...     rightfoot = makefoot('right', -1)
... finally:
...     pmc.undoInfo(closeChunk=True)

>>> import mayautils
>>> with mayautils.undo_chunk():
...     leftfoot = makefoot('left', 1)
>>> with mayautils.undo_chunk():
...     rightfoot = makefoot('right', -1)

>>> @mayautils.chunk_undo
... def makefoot(prefix, x=1):
...     foot = pmc.polySphere(name=prefix + '_foot')[0]
...     foot.translate.set(5 * x, 0, 0)
...     # Other code that changes foot
>>> leftfoot = makefoot('left', 1)
>>> rightfoot = makefoot('right', -1)

>>> def add(a, b):
...     return a + b
>>> add(1, 2)
3
>>> add.__call__
<method-wrapper '__call__' of function object at 0x0...>
>>> add.__call__(1, 2)
3

>>> def nothing(func):
...     return func
>>> nothing(add)(1, 2)
3

>>> def makeadd():
...     def add(a, b):
...         return a + b
...     return add
>>> makeadd()(1, 2)
3

>>> def makeadd(adder):
...     def inner(a, b):
...         return adder(a, b)
...     return inner
>>> makeadd(add)(1, 2)
3

>>> def announce(adder):
...     def inner(a, b):
...         print 'Adding', a, b
...         result = adder(a, b)
...         print 'Got', result
...         return result
...     return inner
>>> announce(add)(1, 2)
Adding 1 2
Got 3
3

>>> def announce(func):
...     def inner(a, b):
...         print 'Calling', func.__name__, a, b
...         result = func(a, b)
...         print 'Got', result
...         return result
...     return inner
>>> def subtract(a, b):
...     return a - b
>>> announce(subtract)(1, 2)
Calling subtract 1 2
Got -1
-1

>>> def announce(func):
...     def inner(*args, **kwargs):
...         print 'Calling', func.__name__, args, kwargs
...         result = func(*args, **kwargs)
...         print 'Got', result
...         return result
...     return inner
>>> def add3(a, b, c):
...     return a + b + c
>>> announce(add)(1, 2)
Calling add (1, 2) {}
Got 3
3
>>> announce(add3)(1, 2, 3)
Calling add3 (1, 2, 3) {}
Got 6
6

>>> loud_add = announce(add)
>>> loud_add(1, 2)
Calling add (1, 2) {}
Got 3
3

>>> add = announce(add)
>>> add(1, 2)
Calling add (1, 2) {}
Got 3
3

>>> @announce
... def divide(a, b):
...     return a / b
>>> divide(10, 2)
Calling divide (10, 2) {}
Got 5
5

>>> mayautils.export_char_meshes('')

>>> with open('myfile.txt') as f:
...     text = f.read()

>>> text = open('myfile.txt').read()

# open can fail,
# so make sure the variable is referenced
>>> f = None
>>> try:
...     f = open('myfile.txt')
...     text = f.read() # only happens if open succeeds
... finally:
...     if f: # If open failed, f is still None
...         f.close()

>>> class MyContextManager(object):
...     def __enter__(self):
...         pass
...     def __exit__(self, exc_type, exc_value, exc_tb):
...         pass

>>> with MyContextManager():
...     pass

>>> class safeopen(object):
...     def __init__(self, *args, **kwargs):
...         self.args = args
...         self.kwargs = kwargs
...         self.f = None
...     def __enter__(self):
...         self.f = open(*self.args, **self.kwargs)
...         return self.f
...     def __exit__(self, *exc_info):
...         if self.f:
...             self.f.close()

>>> with safeopen('myfile.txt') as f:
...     text = f.read()

>>> class demo(object):
...     def __init__(self):
...         print 'init' #(1)
...     def __enter__(self):
...         print 'entered' #(2)
...         return 'hello!' #(3)
...     def __exit__(self, *exc_info):
...         print 'exited. Exc_info:', exc_info #(4)
...         #return True

>>> with demo() as d:
...     print 'd is', d
init
entered
d is hello!
exited. Exc_info: (None, None, None)
>>> with demo() as d:
...     raise RuntimeError('hi') #doctest: +SKIP
init
entered
exited. Exc_info: (<type 'exceptions.RuntimeError'>, RuntimeError('hi',), <traceback object at 0x0...)
Traceback (most recent call last):
RuntimeError: hi

>>> deleteall()

>>> with mayautils.undo_chunk():
...     pmc.joint(), pmc.joint()
(nt.Joint(u'joint1'), nt.Joint(u'joint2'))
>>> pmc.ls(type='joint')
[nt.Joint(u'joint1'), nt.Joint(u'joint2')]
>>> pmc.undo()
>>> pmc.ls(type='joint')
[]

>>> replacefiles()

>>> pmc.undoInfo(openChunk=True)
>>> try:
...     for f in pmc.ls(type='file'):
...         f.ftn.set(f.ftn.get().lower())
...     pmc.undoInfo(closeChunk=True)
... except:
...     pmc.undoInfo(closeChunk=True)
...     pmc.undo()
...     raise
Traceback (most recent call last):
RuntimeError: setAttr: The attribute 'file2.fileTextureName' is locked or connected and cannot be modified.
<BLANKLINE>
>>> [f.ftn.get() for f in pmc.ls(type='file')]
[u'FTN0', u'FTN1', u'FTN2']

>>> replacefiles()

>>> with mayautils.undo_on_error():
...     for f in pmc.ls(type='file'):
...         f.ftn.set(f.ftn.get().lower())
Traceback (most recent call last):
RuntimeError: setAttr: The attribute 'file2.fileTextureName' is locked or connected and cannot be modified.
<BLANKLINE>
>>> [f.ftn.get() for f in pmc.ls(type='file')]
[u'FTN0', u'FTN1', u'FTN2']

>>> import mock, sys
>>> with mock.patch('sys.executable'):
...     print sys.executable
<MagicMock name='executable' id='...'>
>>> @mock.patch('sys.executable', mock.MagicMock())
... def foo():
...     print sys.executable
>>> foo()
<MagicMock id='...'>

>>> @deco_using_func('func deco')
... def decorated_func1():
...     return
>>> decorated_func1()
Hello from func deco
>>> @deco_using_cls('class deco')
... def decorated_func2():
...     return
>>> decorated_func2()
Hello from class deco

>>> def deco1(func):
...     def inner():
...         print 'deco1'
...         return func()
...     return inner
>>> def deco2(func):
...     def inner():
...         print 'deco2'
...         return func()
...     return inner
>>> @deco1
... @deco2
... def func():
...     print 'inside func'
>>> func()
deco1
deco2
inside func

>>> def func2():
...     print 'inside func2'
>>> func2 = deco1(deco2(func2))
>>> func2()
deco1
deco2
inside func2
"""

def deco_using_func(key):
    def _deco(func):
        def inner(*args, **kwargs):
            print 'Hello from', key
            return func(*args, **kwargs)
        return inner
    return _deco

class deco_using_cls(object):
    def __init__(self, key):
        self.key = key
    def __call__(self, func):
        def inner(*args, **kwargs):
            print 'Hello from', self.key
            return func(*args, **kwargs)
        return inner


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
    sys.exit(0)
