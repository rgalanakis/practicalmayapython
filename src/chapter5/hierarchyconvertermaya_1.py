"""Simple window. Hides behind Maya."""

import hierarchyconvertergui as hierconvgui

_window = None

def show():
    global _window
    if _window is None:
        cont = hierconvgui.HierarchyConverterController()
        _window = hierconvgui.create_window(cont)
    _window.show()
