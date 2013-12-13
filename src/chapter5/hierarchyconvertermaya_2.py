"""Window is parented properly."""

import hierarchyconvertergui as hierconvgui
import mayautils

_window = None

def show():
    global _window
    if _window is None:
        cont = hierconvgui.HierarchyConverterController()
        parent = mayautils.get_maya_window()
        _window = hierconvgui.create_window(cont, parent)
    _window.show()
