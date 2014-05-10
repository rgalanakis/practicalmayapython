"""Hook up selection changed."""

import maya.OpenMaya as OpenMaya
import pymel.core as pmc
import hierarchyconvertergui as hierconvgui
import mayautils

_window = None

def show():
    global _window
    if _window is None:
        cont = hierconvgui.HierarchyConverterController()
        def emit_selchanged(_): #(1)
            cont.selectionChanged.emit(
                pmc.selected(type='transform'))
        OpenMaya.MEventMessage.addEventCallback( #(2)
            'SelectionChanged', emit_selchanged)
        parent = mayautils.get_maya_window()
        _window = hierconvgui.create_window(cont, parent)
    _window.show()
