"""Hooks up conversion to character creator."""

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'chapter2'))

import maya.OpenMaya as OpenMaya
import pymel.core as pmc
import hierarchyconvertergui as hierconvgui
import mayautils
import _hierarchyconvertermayastate
import charcreator #(1)

def _replace_callback(func):
    oldCBID = getattr(_hierarchyconvertermayastate, 'cbid', None)
    if oldCBID is not None:
        OpenMaya.MEventMessage.removeCallback(oldCBID)
    cbid = OpenMaya.MEventMessage.addEventCallback(
        'SelectionChanged', func)
    _hierarchyconvertermayastate.cbid = cbid

_window = None

def show():
    global _window
    if _window is None:
        cont = hierconvgui.HierarchyConverterController()
        def emit_selchanged(_):
            cont.selectionChanged.emit(
                pmc.selected(type='transform'))
        _replace_callback(emit_selchanged)
        parent = mayautils.get_maya_window()
        _window = hierconvgui.create_window(cont, parent)
        def onconvert(prefix): #(2)
            settings = dict(
                charcreator.SETTINGS_DEFAULT,
                prefix=unicode(prefix)) #(3)
            charcreator.convert_hierarchies_main(settings)
        _window.convertClicked.connect(onconvert) #(4)
    _window.show()
