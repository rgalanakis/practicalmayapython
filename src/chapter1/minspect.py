import pymel.core as pmc
import sys
import types


def syspath():
    print 'sys.path:'
    for p in sys.path:
        print '  ' + p


def info(obj):
    """Prints information about the object."""

    lines = ['Info for %s' % obj.name(),
             'Attributes:']
    # Get the name of all attributes
    for a in obj.listAttr():
        lines.append('  ' + a.name())
    lines.append('MEL type: %s' % obj.type())
    lines.append('MRO:')
    lines.extend(['  ' + t.__name__ for t in type(obj).__mro__])
    result = '\n'.join(lines)
    print result


def _is_pymel(obj):
    try: # (1)
        module = obj.__module__ # (2)
    except AttributeError: # (3)
        try:
            module = obj.__name__ # (4)
        except AttributeError:
            return None # (5)
    return module.startswith('pymel') # (6)


def _py_to_helpstr(obj):
    if isinstance(obj, basestring):
        return 'search.html?q=%s' % (obj.replace(' ', '+'))
    if not _is_pymel(obj):
        return None
    if isinstance(obj, types.ModuleType):
        return 'generated/{0}.html#module-{0}'.format(obj.__name__)
    if isinstance(obj, types.MethodType):
        return 'generated/classes/{module}/{module}.{typename}.html#{module}.{typename}.{methname}'.format(
            module=obj.__module__,
            typename=obj.im_class.__name__,
            methname=obj.__name__)
    if isinstance(obj, types.FunctionType):
        return 'generated/functions/{module}/{module}.{funcname}.html#{module}.{funcname}'.format(
            module=obj.__module__,
            funcname=obj.__name__)
    if not isinstance(obj, type):
        obj = type(obj)
    return 'generated/classes/{module}/{module}.{typename}.html#{module}.{typename}'.format(
        module=obj.__module__,
        typename=obj.__name__)


def test_py_to_helpstr():
    def dotest(obj, ideal):
        result = _py_to_helpstr(obj)
        assert result == ideal, '%s != %s' % (result, ideal)
    dotest('maya rocks', 'search.html?q=maya+rocks')
    dotest(pmc.nodetypes, 'generated/pymel.core.nodetypes.html#module-pymel.core.nodetypes')
    dotest(pmc.nodetypes.Joint, 'generated/classes/pymel.core.nodetypes/pymel.core.nodetypes.Joint.html#pymel.core.nodetypes.Joint')
    dotest(pmc.nodetypes.Joint(), 'generated/classes/pymel.core.nodetypes/pymel.core.nodetypes.Joint.html#pymel.core.nodetypes.Joint')
    dotest(pmc.nodetypes.Joint().getTranslation, 'generated/classes/pymel.core.nodetypes/pymel.core.nodetypes.Joint.html#pymel.core.nodetypes.Joint.getTranslation')
    dotest(pmc.joint, 'generated/functions/pymel.core.animation/pymel.core.animation.joint.html#pymel.core.animation.joint')
    dotest(object(), None)
    dotest(10, None)
    dotest([], None)
    dotest(sys, None)


def test_py_to_helpstrFAIL():
    assert 1 == 2, '1 != 2'


import webbrowser # (1)
HELP_ROOT_URL = 'http://autodesk.com/us/maya/2011help/PyMel/'# (2)

def pmhelp(obj): # (3)
    """Gives help for a pymel or python object.

    If obj is not a PyMEL object, use Python's built-in
    `help` function.
    If obj is a string, open a web browser to a search in the
    PyMEL help for the string.
    Otherwise, open a web browser to the page for the object.
    """
    tail = _py_to_helpstr(obj)
    if tail is None:
        help(obj) # (4)
    else:
        webbrowser.open(HELP_ROOT_URL + tail) # (5)

# Version 2
#
#import inspect
#import pymel.core as pmc
#import sys  # Was already present
#
#
#def info(obj):
#    """Prints information about the object."""
#
#    lines = ['Info for %s' % obj.name()]
#    # Get the value of all attributes in our object
#    allattrs = [getattr(obj, a) for a in dir(obj)]
#    lines.append('Methods:')
#    # Get the name of any attributes that are methods
#    lines.extend([a.func_name for a in allattrs if
#                  inspect.ismethod(a)])
#    lines.append('Attributes:')
#    # Get the name of any attributes
#    # that are PyMEL Attribute instances
#    lines.extend([a.name() for a in allattrs if isinstance(a, pmc.Attr)])
#    result = '\n'.join(lines)
#    print result
#
## Version 3
#
#def info(obj):
#    """Prints information about the object."""
#
#    lines = ['Info for %s' % obj.name()]
#    # Get the value of all attributes in our object
#    allattrs = [getattr(obj, a) for a in dir(obj)]
#    lines.append('Methods:')
#    # Get the name of any attributes that are methods
#    lines.extend([a.func_name for a in allattrs if inspect.ismethod(a)])
#    lines.append('Attributes:')
#    # Get the name of any attributes
#    # that are PyMEL Attribute instances
#    lines.extend([a.name() for a in allattrs if isinstance(a, pmc.Attr)])
#    lines.append('MEL type: %s' % obj.type())
#    lines.append('MRO:')
#    lines.extend([t.__name__ for t in type(obj).__mro__])
#    result = '\n'.join(lines)
#    print result
#
#
## Function converts a python object to a PyMEL help query url.
## If the object is a string,
##   return a query string for a help search.
## If the object is a PyMEL object,
##   return the appropriate url tail.
## PyMEL functions, modules, types, instances,
##   and methods are all valid.
## Non-PyMEL objects return None.
## Function takes a python object and returns a full help url.
## Calls the first function.
## If first function returns None,
##   just usebuiltin `help` function.
## Otherwise, open a web browser to the help page.
#
#
#def _pyToHelpStr(obj): # (1)
#    return None
#
#
#def test_pyToHelpStr(): # (2)
#    def dotest(obj, ideal): #(3)
#        result = _pyToHelpStr(obj)
#        assert result == ideal, '%s != %s' % (result, ideal) #(4)
#
#    dotest('maya rocks', 'search.html?q=maya+rocks') #(5)
#
#
#def _pyToHelpStr(obj):
#    if isinstance(obj, basestring):
#        return 'search.html?q=%s' % (obj.replace(' ', '+'))
#    return None
#
#
#def test_pyToHelpStr():
#    def dotest(obj, ideal):
#        result = _pyToHelpStr(obj)
#        assert result == ideal, '%s != %s' % (result, ideal)
#
#    dotest('maya rocks', 'search.html?q=maya+rocks')
#    dotest(pmc.nodetypes, 'generated/pymel.core.nodetypes.html#module-pymel.core.nodetypes')
#    dotest(pmc.nodetypes.Joint,
#           'generated/classes/pymel.core.nodetypes/pymel.core.nodetypes.Joint.html#pymel.core.nodetypes.Joint')
#    dotest(pmc.nodetypes.Joint(),
#           'generated/classes/pymel.core.nodetypes/pymel.core.nodetypes.Joint.html#pymel.core.nodetypes.Joint')
#    dotest(pmc.nodetypes.Joint().children,
#           'generated/classes/pymel.core.nodetypes/pymel.core.nodetypes.Joint.html#pymel.core.nodetypes.Joint.children')
#    dotest(pmc.joint,
#           'generated/functions/pymel.core.animation/pymel.core.animation.joint.html?highlight=joint#pymel.core.animation.joint')
#    dotest(10, None)
#    dotest(object(), None)
#
#
#import types
#
#
#def _pyToHelpStr(obj):
#    if isinstance(obj, basestring):
#        return 'search.html?q=%s' % (obj.replace(' ', '+'))
#    if isinstance(obj, types.ModuleType):
#        return 'generated/{0}.html#module-{0}'.format(obj.__name__)
#    return None
#
#
#def _pyToHelpStr(obj):
#    if isinstance(obj, basestring):
#        return 'search.html?q=%s' % (obj.replace(' ', '+'))
#    if isinstance(obj, types.ModuleType):
#        return 'generated/{0}.html#module-{0}'.format(obj.__name__)
#    if isinstance(obj, type):
#        return 'generated/classes/{module}/{module}.{typename}.html#{module}.{typename}'.format(
#            module=obj.__module__, typename=obj.__name__)
#    return None
#
#
#def _pyToHelpStr(obj):
#    if isinstance(obj, types.InstanceType):
#        obj = type(obj)
#    if isinstance(obj, basestring):
#        return 'search.html?q=%s' % (obj.replace(' ', '+'))
#    if isinstance(obj, types.ModuleType):
#        return 'generated/{0}.html#module-{0}'.format(obj.__name__)
#    if isinstance(obj, type):
#        return 'generated/classes/{module}/{module}.{typename}.html#{module}.{typename}'.format(
#            module=obj.__module__, typename=obj.__name__)
#    return None
#
#
#def _pyToHelpStr(obj):
#    if isinstance(obj, types.InstanceType):
#        obj = type(obj)
#    if isinstance(obj, basestring):
#        return 'search.html?q=%s' % (obj.replace(' ', '+'))
#    if isinstance(obj, types.ModuleType):
#        return 'generated/{0}.html#module-{0}'.format(obj.__name__)
#    if isinstance(obj, type):
#        return 'generated/classes/{module}/{module}.{typename}.html#{module}.{typename}'.format(
#            module=obj.__module__,
#            typename=obj.__name__)
#    if isinstance(obj, types.MethodType):
#        return 'generated/classes/{module}/{module}.{typename}.html#{module}.{typename}.{methname}'.format(
#            module=obj.__module__,
#            typename=obj.im_class.__name__,
#            methname=obj.__name__)
#    return None
#
#
#def _pyToHelpStr(obj):
#    if isinstance(obj, types.InstanceType):
#        obj = type(obj)
#    if isinstance(obj, basestring):
#        return 'search.html?q=%s' % (obj.replace(' ', '+'))
#    if isinstance(obj, types.ModuleType):
#        return 'generated/{0}.html#module-{0}'.format(obj.__name__)
#    if isinstance(obj, type):
#        return 'generated/classes/{module}/{module}.{typename}.html#{module}.{typename}'.format(
#            module=obj.__module__,
#            typename=obj.__name__)
#    if isinstance(obj, types.MethodType):
#        return 'generated/classes/{module}/{module}.{typename}.html#{module}.{typename}.{methname}'.format(
#            module=obj.__module__,
#            typename=obj.im_class.__name__,
#            methname=obj.__name__)
#    if isinstance(obj, types.FunctionType):
#        return 'generated/functions/{module}/{module}.{funcname}.html#{module}.{funcname}'.format(
#            module=obj.__module__,
#            funcname=obj.__name__)
#    return None
#
#
#def _isPymel(obj):
#    try:
#        module = obj.__module__
#    except AttributeError:
#        module = obj.__name__
#    return module.startswith('pymel')
#
#
#def test_pyToHelpStr():
#    def dotest(obj, ideal):
#        result = _pyToHelpStr(obj)
#        assert result == ideal, '%s != %s' % (result, ideal)
#
#    dotest('maya rocks', 'search.html?q=maya+rocks')
#    dotest(pmc.nodetypes, 'generated/pymel.core.nodetypes.html#module-pymel.core.nodetypes')
#    dotest(pmc.nodetypes.Joint,
#           'generated/classes/pymel.core.nodetypes/pymel.core.nodetypes.Joint.html#pymel.core.nodetypes.Joint')
#    dotest(pmc.nodetypes.Joint(),
#           'generated/classes/pymel.core.nodetypes/pymel.core.nodetypes.Joint.html#pymel.core.nodetypes.Joint')
#    dotest(pmc.nodetypes.Joint().children,
#           'generated/classes/pymel.core.nodetypes/pymel.core.nodetypes.Joint.html#pymel.core.nodetypes.Joint.children')
#    dotest(pmc.joint,
#           'generated/functions/pymel.core.animation/pymel.core.animation.joint.html?highlight=joint#pymel.core.animation.joint')
#    dotest(10, None)
#    dotest(object(), None)
#    dotest(10, None)
#    dotest([], None)
#    dotest(sys, None)
#
#
#def _pyToHelpStr(obj):
#    if isinstance(obj, types.InstanceType):
#        obj = type(obj)
#    if isinstance(obj, basestring):
#        return 'search.html?q=%s' % (obj.replace(' ', '+'))
#    if not _isPymel(obj):
#        return None
#    if isinstance(obj, types.ModuleType):
#        return 'generated/{0}.html#module-{0}'.format(obj.__name__)
#    if isinstance(obj, type):
#        return 'generated/classes/{module}/{module}.{typename}.html#{module}.{typename}'.format(
#            module=obj.__module__,
#            typename=obj.__name__)
#    if isinstance(obj, types.MethodType):
#        return 'generated/classes/{module}/{module}.{typename}.html#{module}.{typename}.{methname}'.format(
#            module=obj.__module__,
#            typename=obj.im_class.__name__,
#            methname=obj.__name__)
#    if isinstance(obj, types.FunctionType):
#        return 'generated/functions/{module}/{module}.{funcname}.html#{module}.{funcname}'.format(
#            module=obj.__module__,
#            funcname=obj.__name__)
#    return None
#
#
#import webbrowser
#
#HELP_ROOT_URL = 'http://autodesk.com/us/maya/2011help/PyMel/'
#
#
#def pmhelp(obj):
#    tail = _pyToHelpStr(obj)
#    if tail is None:
#        help(obj)
#    else:
#        webbrowser.open(HELP_ROOT_URL + tail)
#
#
#def pmhelp(obj):
#    """Gives help for a pymel or python object.
#
#    If obj is not a PyMEL object, use Python's built-in `help` function.
#    If obj is a string, open a web browser to a search in the PyMEL help for the string.
#    Otherwise, open a web browser to the page for the object.
#    """
#    tail = _pyToHelpStr(obj)
#    if tail is None:
#        help(obj)
#    else:
#        webbrowser.open(HELP_ROOT_URL + tail)
#
