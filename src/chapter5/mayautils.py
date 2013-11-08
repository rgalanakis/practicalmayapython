import shiboken
from PySide import QtGui, QtCore

def wrapinstance(ptr):
    """Like sip.wrapinstance, but for PySide."""
    # pointers for Qt should always be long integers
    ptr = long(ptr)
    # Get the QObject for this pointer,
    # so we can get the class info and the real type eventually.
    qobj = shiboken.wrapInstance(ptr, QtCore.QObject)
    metaobj = qobj.metaObject()
    realcls = None
    # QObject is the base class for all Qt objects,
    # so we'll get here eventually! 
    while realcls != QtCore.QObject:
        clsname = metaobj.className()
        # Look for this class on QtGui or QtCore.
        realcls = getattr(QtGui, clsname, None)
        if realcls is None:
            realcls = getattr(QtCore, clsname, None)
    # Finally, return the same pointer/object 
    # as its most specific type. 
    return shiboken.wrapInstance(ptr, realcls)


import maya.OpenMayaUI as OpenMayaUI

def get_maya_window():
    """Return the QMainWindow for the main Maya window."""

    winptr = OpenMayaUI.MQtUtil.mainWindow()
    if winptr is None:
        raise RuntimeError('No Maya window found.')
    window = wrapinstance(winptr)
    assert isinstance(window, QtGui.QMainWindow)
    return window


def uipath_to_qtobject(pathstr):
    """Return the QtObject for a Maya UI path to a control,
    layout, or menu item.
    Return None if no item is found.
    """
    ptr = OpenMayaUI.MQtUtil.findControl(pathstr)
    if ptr is None:
        ptr = OpenMayaUI.MQtUtil.findLayout(pathstr)
    if ptr is None:
        ptr = OpenMayaUI.MQtUtil.findMenuItem(pathstr)
    if ptr is not None:
        return wrapinstance(ptr)
