from uiutils import QtCore, QtGui, wrapinstance

import maya.OpenMayaUI as OpenMayaUI
import pymel.core as pmc


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
    return None


def get_main_window_name():
    return pmc.MelGlobals()['gMainWindow']
