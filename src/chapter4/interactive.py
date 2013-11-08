# import maya.standalone
# maya.standalone.initialize(name='python')
#
import contextlib
# import maya.cmds as cmds
import pymel.core as pmc

import mayautils


def interactive():
    """
    Code for all the interactive prompts throughout the chapter.

    >>> leftfoot = pmc.polySphere(name='left_foot')
    >>> leftfoot.setTranslation(5, 0, 0)
    # ...other code that changes left_foot
    >>> rightfoot = pmc.polySphere(name='right_foot')
    >>> rightfoot.setTranslation(-5, 0, 0)
    # ...same code, but for right_foot

    >>> def makefoot(prefix, x=1):
    ...     foot = pmc.polySphere(name=prefix + '_foot')
    ...     foot.setTranslation(5 * x, 0, 0)
    ...     # ...other code that changes foot
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

    >>> with open('myfile.txt') as f:
    ...     text = f.read()

    >>> text = open('myfile.txt').read()
    
    >>> f = None # open can fail, so make sure the variable is referenced
    >>> try:
    ...     f = open('myfiles.txt')
    ... else: # only happens if open succeeds
    ...     text = f.read()
    ... finally:
    ...     if f: # If open failed, f is still None
    ...         f.close()

    >>> class MyContextManager(object):
    ...     def __enter__(self):
    ...         pass
    ...     def __exit__(self, exc_type, exc_value, exc_tb):
    ...         pass

    >>> @contextlib.contextmanager
    ... def safeopen(*args, **kwargs):
    ...     f = None
    ...     try:
    ...         f = open(*args, **kwargs)
    ...     else:
    ...         # Assigned to the "as <name>"
    ...         # part of the "with" statement.
    ...         yield f
    ...     finally:
    ...         if f:
    ...             f.close()
    >>>
    >>> with safeopen('myfile.txt') as f:
    ...     text = f.read()

    >>> with mayautils.undo_chunk():
    ...     pass # Some code

    >>> pmc.undoInfo(openChunk=True)
    >>> try:
    ...     for f in pmc.ls(type='file'):
    ...         f.ftn.set(f.ftn.get().lower())
    ...     pmc.undoInfo(closeChunk=True)
    ... except:
    ...     pmc.undoInfo(closeChunk=True)
    ...     pmc.undo()
    ...     raise

    >>> with mayautils.undo_on_error():
    ...     for f in pmc.ls(type='file'):
    ...         f.ftn.set(f.ftn.get().lower())

    >>> def make_foot(prefix):
    ...     return pmc.joint(prefix + '_foot')
    >>> with mayautils.undo_chunk():
    ...     leftfoot = makefoot('left')

    >>> @mayautils.undo_chunk
    >>> def make_foot(prefix):
    ...     return pmc.joint(prefix + '_foot')
    >>> leftfoot = makefoot('left')

    >>> def makefoot(prefix):
    ...     return pmc.joint(prefix + '_foot')
    >>> leftfoot = makefoot('left')

    >>> def footmaker():
    ...     def inner(prefix):
    ...         return pmc.joint(prefix + '_foot')
    ...     return inner
    >>> m = footmaker()
    >>> m('left')
    Joint('left_foot')
    
    >>> def makefoot(prefix):
    ...     return pmc.joint(prefix + '_foot')
    >>> def announce(func):
    ...     # needs to take *args and **kwargs so 
    ...     # inner has the same signature as func
    ...     def inner(*args, **kwargs):
    ...         print 'Calling %s(*%s, **%s)' % (
    ...             func.__name__, args, kwargs)
    ...         return func(*args, **kwargs)
    ...     return inner
    >>> loudmakefoot = announce(makefoot)
    >>> loudmakefoot('left')
    Calling makefoot(('left',), {})
    Joint('left_foot')

    >>> makefoot = announce(makefoot)
    >>> makefoot('left')
    Calling makefoot(('left',), {})
    Joint('left_foot')

    >>> @announce
    ... def makefoot(prefix):
    ...     return pmc.joint(prefix + '_foot')
    >>> makefoot('left')
    Calling makefoot(('left',), {})
    Joint('left_foot')
    
    >>> @contextlib.contextmanager
    ... def selection_preserved():
    ...     sel = list(pmc.selected())
    ...     try:
    ...         yield
    ...     finally:
    ...         pmc.select(sel, replace=True)
    >>>
    >>> def export_meshes(path):
    ...     objs = [o for o in pmc.ls(type='mesh') 
    ...             if '_char_' in o.name()]
    ...     pmc.select(objs, replace=True)
    ...     pmc.superExporter(path)
    >>>
    >>> with selection_preserved():
    ...     export_meshes('C:\\temp.xyz')
    
    >>> def preserve_selection(func):
    ...     def inner(*args, **kwargs):
    ...         sel = list(pmc.selected())
    ...         result = func(*args, **kwargs)
    ...         pmc.select(sel, replace=True)
    ...         return result
    ...     return inner
    >>> 
    >>> @preserve_selection
    ... def export_meshes(path):
    ...     objs = [o for o in pmc.ls(type='mesh') 
    ...             if '_char_' in o.name()]
    ...     pmc.select(objs)
    ...     pmc.superExporter(path)

    >>> with mayautils.at_time(0):
    ...     metadata.timelineData('Animation Start')

    >>> open(r'\\not_a_unc\spam\eggs.txt', 'w')
    IOError: [Errno 2] No such file or directory: ''

    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()
