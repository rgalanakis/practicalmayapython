"""Hooks up the converter state shim to hold selection changed callback."""

import maya.OpenMaya as OpenMaya
import pymel.core as pmc
import hierarchyconvertergui as hierconvgui
import mayautils
import _hierarchyconvertermayastate

def _replace_callback(onSelChanged):
    oldCBID = getattr(_hierarchyconvertermayastate, 'cbid', None)
    if oldCBID is not None:
        OpenMaya.MEventMessage.removeCallback(oldCBID)
    cbid = OpenMaya.MEventMessage.addEventCallback(
        'SelectionChanged', onSelChanged)
    _hierarchyconvertermayastate.cbid = cbid

_window = None

def show():
    global _window
    if _window is None:
        cont = hierconvgui.HierarchyConverterController()
        def onSelChanged(_):
            cont.selectionChanged.emit(
                pmc.selected(type='transform'))
        _replace_callback(onSelChanged)
        parent = mayautils.get_maya_window()
        _window = hierconvgui.create_window(cont, parent)
    _window.show()
