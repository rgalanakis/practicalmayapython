import hierarchyconvertergui as hierconvgui

_window = None

def show():
    global _window
    if _window is None:
        cont = hierconvgui.HierarchyConverterController()
        _window = hierconvgui.create_window(cont)
    _window.show()


# Version 2


import hierarchyconvertergui as hierconvgui
import mayahelpers

_window = None

def show():
    global _window
    if _window is None:
        cont = hierconvgui.HierarchyConverterController()
        parent = mayahelpers.get_maya_window()
        _window = hierconvgui.create_window(cont, parent)
    _window.show()


# Version 3

import maya.OpenMaya as OpenMaya
import pymel.core as pmc
import hierarchyconvertergui as hierconvgui
import mayahelpers

_window = None

def show():
    global _window
    if _window is None:
        cont = hierconvgui.HierarchyConverterController()
        def onSelChanged(_):
            cont.selectionChanged.emit(
                pmc.selected(type='transform'))
        openMaya.MEventMessage.addEventCallback(
            'SelectionChanged', onSelChanged)
        parent = mayahelpers.get_maya_window()
        _window = hierconvgui.create_window(cont, parent)
    _window.show()

# Version 4

import maya.OpenMaya as OpenMaya
import pymel.core as pmc
import hierarchyconvertergui as hierconvgui
import mayahelpers
import _hierarchyconvertermayastate

def _replace_callback(onSelChanged):
    oldCBID = getattr(hierarchyconvertermayastate, 'cbid', None)
    if oldCBID is not None:
        OpenMaya.MEventMessage.removeCallback(oldCBID)
    cbid = openMaya.MEventMessage.addEventCallback(
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
        parent = mayahelpers.get_maya_window()
        _window = hierconvgui.create_window(cont, parent)
    _window.show()


# Version 5

import maya.OpenMaya as OpenMaya
import pymel.core as pmc
import hierarchyconverter
import hierarchyconvertergui as hierconvgui
import mayahelpers
import _hierarchyconvertermayastate

def _replace_callback(onSelChanged):
    oldCBID = getattr(hierarchyconvertermayastate, 'cbid', None)
    if oldCBID is not None:
        OpenMaya.MEventMessage.removeCallback(oldCBID)
    cbid = openMaya.MEventMessage.addEventCallback(
        'SelectionChanged', onSelChanged)
    _hierarchyconvertermayastate.cbid = cbid

_window = None

def show():
    global _window
    if _window is None:
        cont = hierconv.HierarchyConverterController()
        def onSelChanged(_):
            cont.selectionChanged.emit(
                pmc.selected(type='transform'))
        _replace_callback(onSelChanged)
        parent = mayahelpers.get_maya_window()
        _window = hierconv.create_window(cont, parent)
        def onconvert(prefix):
            settings = dict(
                hierarchyconverter.DEFAULT_SETTINGS,
                prefix=prefix)
            hierarchyconverter.convert_hierarchies_main(settings)
        _window.convertClicked.connect(onconvert)
    _window.show()