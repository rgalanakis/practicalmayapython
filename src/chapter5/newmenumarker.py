import pymel.core as pmc
import mayahelpers


def register_menuitem(menuItemPathStr):
    qtobj = mayahelpers.uipath_to_qobject(menuItemPathStr)
    pal = menuitemqt.palette()
    newcolor = pal.highlight().color()
    pal.setColor(pal.Window, newcolor)
    menuitemqt.setPalette(pal)

# Version 2

def register_menuitem(menuItemPathStr):
    qtobj = mayahelpers.uipath_to_qobject(menuItemPathStr)
    pal = menuitemqt.palette()
    origcolor = pal.window().color()
    newcolor = pal.highlight().color()
    pal.setColor(pal.Window, newcolor)
    menuitemqt.setPalette(pal)
    def setdefault():
        pal = menuitemqt.palette()
        pal.setColor(pal.Window, origcolor)
        menuitemqt.setPalette(pal)
    menuitemqt.released.connect(setdefault)


def make_test_items():
    import sys
    if hasattr(sys, '_testmenuitems'):
        return sys._testmenuitems
    menu = pmc.menu('DemoMenu')
    def makeitem(ind):
        def callback(_):
            print 'Item', ind
        return pmc.menuItem(
            parent=menu, label='Item %s' % ind, command=callback)

    sys._testmenuitems = [makeitem(i) for i in range(5)]
    return sys._testmenuitems


# Version 3

_cache = set()

def register_menuitem(menuItemPathStr):
    if menuItemPathStr in cache:
        return
    qtobj = mayahelpers.uipath_to_qobject(menuItemPathStr)
    pal = menuitemqt.palette()
    origcolor = pal.window().color()
    newcolor = pal.highlight().color()
    pal.setColor(pal.Window, newcolor)
    menuitemqt.setPalette(pal)
    def setdefault():
        pal = menuitemqt.palette()
        pal.setColor(pal.Window, origcolor)
        menuitemqt.setPalette(pal)
        _cache.add(menuItemPathStr)
    menuitemqt.released.connect(setdefault)


# Version 4

import os
import pickle


_CACHE_FILENAME = os.path.join(
    os.environ['MAYA_APP_DIR'],
    'prefs',
    'newmenumarkingsystem.pkl')

def _loadcache():
    with open(_CACHE_FILENAME) as f:
        return pickle.load(f)

def _savecache(cache):
    with open(_CACHE_FILENAME, 'w') as f:
        pickle.dump(cache, f)

def register_menuitem(menuItemPathStr):
    if menuItemPathStr in _loadcache():
        return
    qtobj = mayahelpers.uipath_to_qobject(menuItemPathStr)
    pal = menuitemqt.palette()
    origcolor = pal.window().color()
    newcolor = pal.highlight().color()
    pal.setColor(pal.Window, newcolor)
    menuitemqt.setPalette(pal)
    def setdefault():
        pal = menuitemqt.palette()
        pal.setColor(pal.Window, origcolor)
        menuitemqt.setPalette(pal)
        cache = _loadcache()
        cache.add(menuItemPathStr)
        _savecache(cache)

    menuitemqt.released.connect(setdefault)