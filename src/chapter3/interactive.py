import pymel.core as pmc


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

    >>> import sys
    >>> sys.stderr = sys.stdout

try:
    spam.eggs()
except AttributeError:
    spam.ham()

if hasattr(spam, 'eggs'):
    spam.eggs()
else:
    spam.ham()

count = 100

if spam:
    for i in xrange(count):
        eggs(i)


>>> ex = SystemError('a', 1)
>>> [t.__name__ for t in type(ex).__mro__]
['SystemError', 'StandardError', 'Exception', 'BaseException', 'object']
>>> ex.args
('a', 1)
>>> dir(ex)
['__class__', '__delattr__', ...'args', 'message']

>>> try:
...     1 + 'a'
... except:
...     print 'Errored!'
Errored!

>>> try:
...     1 + 'a'
... except TypeError:
...     print 'Errored!'
Errored!

>>> try:
...     1 + 'a'
... except (TypeError, RuntimeError):
...     print 'Errored!'
Errored!

>>> try:
...     1 + 'a'
... except RuntimeError:
...     print 'RuntimeError!'
... except TypeError:
...     print 'TypeError!'
TypeError!

>>> try:
...     1 + 'a'
... except TypeError as ex:
...     print repr(ex)
TypeError("unsupported operand type(s) for +: 'int' and 'str'",)

>>> try: #doctest: +SKIP
...     1 + 'a'
... except TypeError:
...     print 'Errored!'
...     raise
Errored!
Traceback (most recent call last):
TypeError: unsupported operand type(s) for +: 'int' and 'str'

>>> try:
...     1 + 'a'
... except TypeError:
...     raise KeyError('hi!')
Traceback (most recent call last):
KeyError: 'hi!'

>>> try:
...     1 + 'a'
... except TypeError:
...     print 'Errored!'
... finally:
...     print 'Cleaned up.'
Errored!
Cleaned up.

>>> 1 + 'a'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 2, in <module>
TypeError: unsupported operand type(s) for +: 'int' and 'str'

>>> import sys
>>> try:
...     1 + 'a'
... except TypeError:
...     si = sys.exc_info()
>>> print si[0]
<type 'exceptions.TypeError'>
>>> print repr(si[1])
TypeError("unsupported operand type(s) for +: 'int' and 'str'",)
>>> print si[2]
<traceback object at 0x0...>


>>> def rename_first_child():
...     try:
...         o = pmc.selected()[0]
...         realname = o.name().split('_')[1]
...         o.getChildren()[0].rename('_' + realname)
...     except Exception as ex:
...         print 'Could not rename first child:'
...         print ex
>>> rename_first_child()
Could not rename first child:
list index out of range

>>> def set_pos(objs):
...     for o in objs:
...         o.translate.set([100,50, 25])
>>> j1, j2, j3 = pmc.joint(), pmc.joint(), pmc.joint()
>>> j2.translate.lock()
>>> set_pos([j1, j2, j3])
Traceback (most recent call last):
RuntimeError: setAttr: The attribute 'joint2.translate' is locked or connected and cannot be modified.
<BLANKLINE>

>>> replacefiles()

>>> for f in pmc.ls(type='file'):
...     f.ftn.set(f.ftn.get().lower())
Traceback (most recent call last):
RuntimeError: setAttr: The attribute 'file2.fileTextureName' is locked or connected and cannot be modified.
<BLANKLINE>
>>> [f.ftn.get() for f in pmc.ls(type='file')]
[u'ftn0', u'FTN1', u'FTN2']

>>> replacefiles()

>>> original_data = []
>>> try:
...     for f in pmc.ls(type='file'):
...         ftn = f.ftn.get()
...         f.ftn.set(ftn.lower())
...         original_data.append([f, ftn])
... except Exception:
...     for f, ftn in original_data:
...         f.ftn.set(ftn)
...     raise
Traceback (most recent call last):
RuntimeError: setAttr: The attribute 'file2.fileTextureName' is locked or connected and cannot be modified.
<BLANKLINE>
>>> [f.ftn.get() for f in pmc.ls(type='file')]
[u'FTN0', u'FTN1', u'FTN2']

>>> replacefiles()

>>> pmc.undoInfo(openChunk=True)
>>> try:
...     for f in pmc.ls(type='file'):
...         f.ftn.set(f.ftn.get().lower())
...     pmc.undoInfo(closeChunk=True)
... except Exception:
...     pmc.undoInfo(closeChunk=True)
...     pmc.undo()
...     raise
Traceback (most recent call last):
RuntimeError: setAttr: The attribute 'file2.fileTextureName' is locked or connected and cannot be modified.
<BLANKLINE>
>>> [f.ftn.get() for f in pmc.ls(type='file')]
[u'FTN0', u'FTN1', u'FTN2']

>>> replacefiles()

>>> import sys
>>> pmc.undoInfo(openChunk=True)
>>> try:
...     for f in pmc.ls(type='file'):
...         f.ftn.set(f.ftn.get().lower())
...     pmc.undoInfo(closeChunk=True)
... except RuntimeError as ex:
...     pmc.undoInfo(closeChunk=True)
...     if ex.args[0].startswith('setAttr: The attribute '):
...         pmc.undo()
...         sys.stderr.write(
...             'Cannot set attribute, fix and try again.\\n')
...         sys.stderr.write(ex.args[0] + '\\n')
...     else:
...          raise
... except Exception:
...     pmc.undoInfo(closeChunk=True)
...     raise
Cannot set attribute, fix and try again.
setAttr: The attribute 'file2.fileTextureName' is locked or connected and cannot be modified.
<BLANKLINE>
>>> [f.ftn.get() for f in pmc.ls(type='file')]
[u'FTN0', u'FTN1', u'FTN2']

>>> a = 1
>>> def spam(eggs=3):
...     b = 2
...     return a + b + eggs
>>> spam
<function spam at 0x0...>
>>> spam.func_defaults
(3,)
>>> sorted(spam.func_globals.keys())
['__builtins__', ..., 'a', ..., 'spam'...]

>>> def eggs():
...     1 + '1'
>>> try:
...     eggs()
... except TypeError:
...     tb = sys.exc_info()[2]
>>> tb
<traceback object at 0x0...>
>>> tb.tb_frame
<frame object at 0x0...>
>>> tb.tb_next
<traceback object at 0x0...>
>>> sorted(tb.tb_frame.f_globals.keys())
['__builtins__', ...'a', ...'pmc', ...'spam', ..., 'tb'...]
>>> tb.tb_frame.f_code.co_filename #doctest: +SKIP
'<console>'
"""


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
