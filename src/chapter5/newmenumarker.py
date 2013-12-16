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

_CACHE_FILENAME = os.path.join( #(2)
    os.environ['MAYA_APP_DIR'],
    'newmenumarkingsystem.json')

def _loadcache():
    try:
        with open(_CACHE_FILENAME) as f: #(3)
            return json.load(f)
    except IOError: #(4)
        return {}

def _savecache(cache):
    with open(_CACHE_FILENAME, 'w') as f: #(5)
        json.dump(cache, f)

def register_menuitem_3(menuitem_path):
    if menuitem_path in _loadcache(): #(6)
        return
    action = mayautils.uipath_to_qtobject(menuitem_path)
    font = action.font()
    font.setBold(True)
    action.setFont(font)
    def setdefault():
        action.setFont(QtGui.QFont())
        cache = _loadcache() #(7)
        cache[menuitem_path] = None
        _savecache(cache) #(8)
    action.triggered.connect(setdefault)


register_menuitem = register_menuitem_3
