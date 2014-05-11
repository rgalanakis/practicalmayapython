"""
Provides a common interface between PyQt4 and PySide.
"""

try:
    from PySide import QtCore, QtGui
    import shiboken
    Signal = QtCore.Signal

    def _getcls(name):
        result = getattr(QtGui, name, None)
        if result is None:
            result = getattr(QtCore, name, None)
        return result

    def wrapinstance(ptr):
        """Converts a pointer (int or long) into the concrete
        PyQt/PySide object it represents."""
        # pointers for Qt should always be long integers
        ptr = long(ptr)
        # Get the pointer as a QObject, and use metaObject
        # to find a better type.
        qobj = shiboken.wrapInstance(ptr, QtCore.QObject)
        metaobj = qobj.metaObject()
        # Look for the real class in qt namespaces.
        # If not found, walk up the hierarchy.
        # When we reach the top of the Qt hierarchy,
        # we'll break out of the loop since we'll eventually
        # reach QObject.
        realcls = None
        while realcls is None:
            realcls = _getcls(metaobj.className())
            metaobj = metaobj.superClass()
        # Finally, return the same pointer/object
        # as its most specific type.
        return shiboken.wrapInstance(ptr, realcls)

except ImportError:
    from PyQt4 import QtCore, QtGui
    Signal = QtCore.pyqtSignal
    import sip
    def wrapinstance(ptr):
        """Converts a pointer (int or long) into the concrete
        PyQt/PySide object it represents."""
        return sip.wrapinstance(long(ptr), QtCore.QObject)
