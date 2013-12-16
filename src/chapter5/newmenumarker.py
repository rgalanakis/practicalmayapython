import pymel.core as pmc
import mayautils
from qtshim import QtGui


# Version 1
# Changes font

def register_menuitem_1(menuItemPathStr):
    action = mayautils.uipath_to_qtobject(menuItemPathStr)
    font = action.font()
    font.setBold(True)
    action.setFont(font)

# Version 2
# Reset font on click.

def register_menuitem_2(menuItemPathStr):
    action = mayautils.uipath_to_qtobject(menuItemPathStr)
    font = action.font()
    font.setBold(True)
    action.setFont(font)
    def setdefault():
        action.setFont(QtGui.QFont())
    action.triggered.connect(setdefault)


def make_test_items():
    menu = pmc.menu('DemoMenu',
                    parent=mayautils.get_main_window_name())
    def makeitem(ind):
        def callback(_):
            print 'Item', ind
        return pmc.menuItem(
            parent=menu, label='Item %s' % ind, command=callback)

    items = [makeitem(i) for i in range(5)]
    for item in items:
        register_menuitem(item.name())


# Version 3
# Adds persistent caching

import json
import os


_CACHE_FILENAME = os.path.join(
    os.environ['MAYA_APP_DIR'],
    'newmenumarkingsystem.json')

def _loadcache():
    try:
        with open(_CACHE_FILENAME) as f:
            return json.load(f)
    except IOError:
        return {}

def _savecache(cache):
    with open(_CACHE_FILENAME, 'w') as f:
        json.dump(cache, f)

def register_menuitem_3(menuItemPathStr):
    if menuItemPathStr in _loadcache():
        return
    action = mayautils.uipath_to_qtobject(menuItemPathStr)
    font = action.font()
    font.setBold(True)
    action.setFont(font)
    def setdefault():
        action.setFont(QtGui.QFont())
        cache = _loadcache()
        cache[menuItemPathStr] = None
        _savecache(cache)

    action.triggered.connect(setdefault)


register_menuitem = register_menuitem_3
