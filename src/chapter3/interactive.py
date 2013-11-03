# import maya.standalone
# maya.standalone.initialize(name='python')
#
# import maya.cmds as cmds
# import pymel.core as pmc


def interactive():
    """
    Code for all the interactive prompts throughout the chapter.

    >>> s = SystemError('a', 1)
    >>> [t.__name__ for t in type(s).__mro__]
    ['SystemError', 'StandardError', 'Exception', 'BaseException', 'object']
    >>> s.args
    ('a', 1)
    >>> s.message # Don't use this!
    ''
    >>> s.args[0] # Use this instead
    'a'

    >>> spam, cleanup = lambda: None, lambda: None
    >>> import logging
    >>> logger = logging.getLogger()

    >>> try:
    ...     spam()
    ... except IOError as ex:
    ...     print 'IOError:', ex.errno
    ...     pass 
    ... except (KeyError, ValueError):
    ...     raise SystemError()
    ... except OSError:
    ...     logger.error('Woah!')
    ...     raise
    ... finally:
    ...     cleanup()
    
    >>> def foo():
    ...     return 'a' + 1
    >>> foo()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "<stdin>", line 2, in <module>
    TypeError: cannot concatenate 'str' and 'int' objects

    >>> import sys
    >>> try:
    ...     'a' + 1
    ... except TypeError:
    ...     si = sys.exc_info()
    >>> print si[0]
    <type 'exceptions.TypeError'>
    >>> print si[1]
    cannot concatenate 'str' and 'int' objects
    >>> print si[2] # doctest: +ELLIPSIS
    <traceback object at 0x...>

    >>> import pymel.core as pmc
    >>> def rename_first_child():
    ...     o = pmc.selected()[0]
    ...     realname = o.name().split('_')[1]
    ...     o.getChildren()[0].rename('_' + realname)
    >>> try:
    ...     rename_first_child()
    ... except IndexError as ex:
    ...     print repr(ex)
    IndexError: list index out of range

    >>> def set_pos(objs):
    ...     for o in objs:
    ...         o.translate.set([100,50, 25])
    >>> j1, j2, j3 = pmc.joint(), pmc.joint(), pmc.joint()
    >>> j2.translate.lock()
    >>> set_pos([j1, j2, j3])

    >>> for f in pmc.ls(type='file'):
    ...     f.ftn.set(f.ftn.get().lower())

    >>> original_data = []
    >>> try:
    ...     for f in pmc.ls(type='file'):
    ...         ftn = f.ftn.get()
    ...         f.ftn.set(ftn.lower())
    ...         original_data.append([f, ftn])
    ... except:
    ...     for f, ftn in original_data:
    ...         f.ftn.set(ftn)
    ...     raise

    >>> pmc.undoInfo(openChunk=True)
    >>> try:
    ...     for f in pmc.ls(type='file'):
    ...         f.ftn.set(f.ftn.get().lower())
    ...     pmc.undoInfo(closeChunk=True)
    ... except:
    ...     pmc.undoInfo(closeChunk=True)
    ...     pmc.undo()
    ...     raise

    >>> pmc.undoInfo(openChunk=True)
    >>> try:
    ...     for f in pmc.ls(type='file'):
    ...         f.ftn.set(f.ftn.get().lower())
    ...     pmc.undoInfo(closeChunk=True)
    ... except RuntimeError as ex:
    ...     pmc.undoInfo(closeChunk=True)
    ...     if 'SOMETHING' in ex.args[0]:
    ...         pmc.undo()
    ...         pmc.warning('Cannot set attribute, fix and try again.')
    ...     else:
    ...         raise
    ... except:
    ...     pmc.undoInfo(closeChunk=True)
    ...     raise

    >>> 1 + '1'
    Traceback (most recent call last):
      File "<console>", line 1, in <module>
    TypeError: unsupported operand type(s) for +: 'int' and 'str'
    >>> import excepthandling
    >>> 1 + '1'
    Hello!

    >>> import logging
    >>> log_filenames = set() # Avoid duplicates
    >>> for logger in logging.Logger.manager.loggerDict.values():
    ...     for handler in logger.handlers:
    ...         try:
    ...             log_filenames.add(handler.baseFilename)
    ...         except AttributeError:
    ...             pass
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()
