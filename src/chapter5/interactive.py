# import maya.standalone
# maya.standalone.initialize(name='python')
#
import contextlib
# import maya.cmds as cmds
import pymel.core as pmc


def interactive():
    """
    Code for all the interactive prompts throughout the chapter.

    >>> def nextsel():
    ...     while True:
    ...         yield []
    ...         yield ['single']
    ...         yield ['single', 'double']
    >>> getnextsel = nextsel().next
    >>> # version with a list
    >>> selections = []
    >>> for i, sel in enumerate(nextsel()):
    ...     selections.append(sel)
    ...     if i == 3:
    ...         break
    >>> selections
    []
    >>>
    >>> # awesome version with a generator
    >>> getnextsel = nextsel().next
    >>> selections = [
    ...     getnextsel(),
    ...     getnextsel(),
    ...     getnextsel()
    ... ]
    >>> selections
    []

    >>> import pymel.core as pmc
    >>> menu = pmc.menu('DemoMenu')
    >>> def callback(_):
    ...     print 'Hello, reader!'
    >>> menuitem = pmc.menuItem(
    ...     parent=menu, label='Greet', command=callback)

    >>> menuitem
    ''

    >>> import mayahelpers
    >>> menuitemqt = mayahelpers.uipath_to_qobject(menuitem)
    >>> menuitemqt
    <Qt object>
    >>> pal = menuitemqt.palette()
    >>> newcolor = pal.highlight().color()
    >>> pal.setColor(pal.Window, newcolor)
    >>> menuitemqt.setPalette(pal)

    >>> menuitemqt.setPalette(QtGui.QPalette()) # reset the palette!
    >>> import newmenumarker
    >>> newmenumarker.register_menuitem(menuitem)

    >>> reload(newmenumarker)
    >>> menuitemqt.setPalette(QtGui.QPalette())
    >>> newmenumarker.register_menuitem(menuitem)

    >>> reload(newmenumarker)
    >>> items = newmenumarker.make_test_items()
    >>> for item in items:
    ...     newmenumarker.register_menuitem(item)
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()
