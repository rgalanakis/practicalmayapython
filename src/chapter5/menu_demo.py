import pymel.core as pmc

import mayautils
from qtshim import QtGui



def demo1_createmenu():
    import mayautils
    menu = pmc.menu(
        'DemoMenu', parent=mayautils.get_main_window_name())

    def callback(_):
        print 'Hello, reader!'
    menuitem = pmc.menuItem(
        parent=menu, label='Greet', command=callback)

    print repr(menuitem)
    # ui.SubMenuItem('MayaWindow|DemoMenu|menuItem254')

    return menuitem


def demo2_changecolor(menuitem):
    action = mayautils.uipath_to_qtobject(menuitem) #(1)
    font = action.font() #(2)
    font.setBold(True) #(3)
    action.setFont(font) #(4)
    return action


def reset_font(action):
    from qtshim import QtGui
    action.setFont(QtGui.QFont())


def demo4_register(menuitem):
    import newmenumarker
    reload(newmenumarker)
    newmenumarker.register_menuitem_3(menuitem)
