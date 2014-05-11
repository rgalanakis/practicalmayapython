import pymel.core as pmc
import mayautils
from qtshim import QtGui


# Version 1
# Changes font

def register_menuitem_1(menuitem_path):
    action = mayautils.uipath_to_qtobject(menuitem_path)
    font = action.font()
    font.setBold(True)
    action.setFont(font)

# Version 2
# Reset font on click.

def register_menuitem_2(menuitem_path):
    action = mayautils.uipath_to_qtobject(menuitem_path)
    font = action.font()
    font.setBold(True)
    action.setFont(font)
    def setdefault():
        action.setFont(QtGui.QFont())
    action.triggered.connect(setdefault)


def make_test_items():
    menu = pmc.menu(
        'DemoMenu', parent=mayautils.get_main_window_name())
    def makeitem(ind):
        def callback(_):
            print 'Item', ind
        item = pmc.menuItem(
            parent=menu, label='Item %s' % ind, command=callback)
        register_menuitem(item.name())
    for i in range(5):
        makeitem(i)



# Version 3
# Adds persistent caching

import json #(1)
import os

_REG_FILENAME = os.path.join( #(2)
    os.environ['MAYA_APP_DIR'],
    'newmenumarkingsystem.json')

def _loadregisry():
    try:
        with open(_REG_FILENAME) as f: #(3)
            return json.load(f)
    except IOError: #(4)
        return {}

def _saveregistry(registry):
    with open(_REG_FILENAME, 'w') as f: #(5)
        json.dump(registry, f)

def register_menuitem_3(menuitem_path):
    if menuitem_path in _loadregisry(): #(6)
        return
    action = mayautils.uipath_to_qtobject(menuitem_path)
    font = action.font()
    font.setBold(True)
    action.setFont(font)
    def setdefault():
        action.setFont(QtGui.QFont())
        registry = _loadregisry() #(7)
        registry[menuitem_path] = None
        _saveregistry(registry) #(8)
    action.triggered.connect(setdefault)


register_menuitem = register_menuitem_3
