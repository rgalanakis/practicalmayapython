"""
Provides a common interface between PyQt4 and PySide.
"""

try:
    from PySide import QtCore, QtGui, shiboken
    Signal = QtCore.Signal

    def wrapinstance(ptr):
        """Converts a pointer (int or long) into the concrete
        PyQt/PySide object it represents."""
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

except ImportError:
    from PyQt4 import QtCore, QtGui
    Signal = QtCore.pyqtSignal
    import sip
    def wrapinstance(ptr):
        """Converts a pointer (int or long) into the concrete
        PyQt/PySide object it represents."""
        return sip.wrapinstance(long(ptr), QtCore.QObject)
