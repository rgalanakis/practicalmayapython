import pymel.core as pmc

import mayautils
from qtshim import QtGui



def demo1_createmenu():
    import mayautils
    menu = pmc.menu('DemoMenu', parent=mayautils.get_main_window_name())
    def callback(_):
        print 'Hello, reader!'
    menuitem = pmc.menuItem(
        parent=menu, label='Greet', command=callback)

    print 'MenuItem:'
    print menuitem # MayaWindow|DemoMenu|menuItem254

    return menuitem


def demo2_changecolor(menuitem):
    action = mayautils.uipath_to_qtobject(menuitem)
    menuitemqt = action.associatedWidgets()[0]
    print 'MenuItemQt:'
    print menuitemqt
    pal = menuitemqt.palette()
    newcolor = pal.highlight().color()
    pal.setColor(pal.Window, newcolor)
    menuitemqt.setPalette(pal)
    return menuitemqt


def resetpalette(menuitemqt):
    menuitemqt.setPalette(QtGui.QPalette()) # reset the palette!


def demo4_register(menuitem):
    import newmenumarker
    reload(newmenumarker)
    newmenumarker.register_menuitem_3(menuitem)
