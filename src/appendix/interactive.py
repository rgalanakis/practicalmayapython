
def argskwargs():
    r"""

>>> def countargs(*args):
...     print 'Passed in', len(args), 'args.'
>>> countargs('a', 'b', 'c')
Passed in 3 args.
>>> countargs()
Passed in 0 args.

>>> import os
>>> os.path.join('a', 'b', 'c')
'a\\b\\c'
>>> os.path.join('a')
'a'
>>> os.path.join()
Traceback (most recent call last):
TypeError: join() takes at least 1 argument (0 given)

>>> items = ['a', 'b', 'c']
>>> countargs(items)
Passed in 1 args.
>>> countargs(*items)
Passed in 3 args.

>>> def countkwargs(**kwargs):
...     print 'Passed in', len(kwargs), 'kwargs.'
>>> countkwargs(a=1, b=2)
Passed in 2 kwargs.
>>> countkwargs()
Passed in 0 kwargs.

>>> def countkwargs2(strfunc=None, **kwargs):
...     msg = 'Passed in %s kwargs.' % len(kwargs)
...     if strfunc:
...         msg = strfunc(msg)
...     print msg
>>> countkwargs2(strfunc=str.upper, a=1)
PASSED IN 1 KWARGS.
>>> countkwargs2(str.lower, a=1, b=2)
passed in 2 kwargs.

>>> mapping = dict(a=1, b=2, strfunc=str.upper)
>>> countkwargs2(arg=mapping)
Passed in 1 kwargs.
>>> countkwargs2(**mapping)
PASSED IN 2 KWARGS.
"""

def strfmt():
    """
>>> name = 'Jon'
>>> 'Hi, %s!' % name
'Hi, Jon!'
>>> 'Hi, {0}!'.format(name)
'Hi, Jon!'

>>> '%s' % 'hi'
'hi'
>>> '%r' % 'hi'
"'hi'"
>>> str('hi')
'hi'
>>> repr('hi')
"'hi'"

>>> '%d' % 100.0
'100'
>>> '%03d' % 10
'010'
>>> '%f' % 1
'1.000000'
>>> '%.3f' % 1
'1.000'

>>> 'Hi, %s!' % ('Jon',)
'Hi, Jon!'
>>> '%s, %s!' % ('Hi', 'Jon')
'Hi, Jon!'
>>> '%s, %s!' % 'Hi'
Traceback (most recent call last):
TypeError: not enough arguments for format string
>>> '%s' % ('Hi', 'Jon')
Traceback (most recent call last):
TypeError: not all arguments converted during string formatting

>>> mapping = {'value': 1.2345, 'units': 'km', 'ignore': 1}
>>> '%(value).3f%(units)s' % mapping
'1.234km'

>>> value = 1.2345
>>> units = 'km'
>>> '%(value).3f%(units)s' % locals()
'1.234km'
"""

strlit = """
Docstrings are parsed, but cannot be raw,
so causes havoc with demo of raw strings.
So we just have to use a real interpreter and test manually.

>>> print 'hello\nworld'
hello
world

>>> print 'C:\newfolder'
C:
ewfolder
>>> print 'C:\\newfolder'
C:\newfolder

>>> print r'C:\newfolder'
C:\newfolder

"""

def uni():
    """
>>> import pymel.core as pmc
>>> xform = pmc.polyCube()[0]
>>> myname = 'cubexform'
>>> xform.rename(myname)
nt.Transform(u'cubexform')
>>> xform.name()
u'cubexform'

>>> myname == xform.name()
True
>>> type(myname), type(xform.name())
(<type 'str'>, <type 'unicode'>)
>>> str.__mro__
(<type 'str'>, <type 'basestring'>, <type 'object'>)
>>> unicode.__mro__
(<type 'unicode'>, <type 'basestring'>, <type 'object'>)
    """



if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
