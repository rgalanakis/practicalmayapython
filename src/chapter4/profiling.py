import types

def _getkey(func):
    if isinstance(func, types.FunctionType):
        return '%s.%s' % (func.__module__, func.__name__)
    if isinstance(func, types.MethodType):
        return '%s.%s.%s' % (func.__module__,
                             func.im_class.__name__,
                             func.__name__) 
    raise TypeError('%s must be a function or method' % func)

def ourfunc(): pass
class OurClass(object):
    def ourmeth(self): pass

assert _getkey(ourfunc) == '__main__.ourfunc'
assert _getkey(OurClass.ourmeth) == '__main__.OurClass.ourmeth'
assert _getkey(OurClass().ourmeth) == '__main__.OurClass.ourmeth'


def record_duration_SIMPLE(func):
    def inner(*args, **kwargs):
        return func(*args, **kwargs)
    return inner

def add(a, b):
    return a + b

assert record_duration_SIMPLE(add)(1, 1) == 2

import time

def record_duration_PRINT(func):
    key = _getkey(func)
    def inner(*args, **kwargs):
        starttime = time.clock()
        result = func(*args, **kwargs)
        endtime = time.clock()
        duration = endtime - starttime
        print '%s took %ss' % (key, duration)
        return result
    return inner


def _report_duration_SIMPLE(key, duration):
    with open('durations.txt', 'a') as f:
        f.write('%s: %s\n' % (key, duration))


def record_duration_FINAL(func):
    key = _getkey(func)
    def inner(*args, **kwargs):
        starttime = time.clock()
        result = func(*args, **kwargs)
        endtime = time.clock()
        duration = endtime - starttime
        _report_duration(key, duration)
        return result
    return inner


import errno #(1)
import traceback #(2)

_reporting_enabled = True #(3)

def _report_duration_FULL(key, duration):
    global _reporting_enabled
    if not _reporting_enabled: #(4)
        return
    try:
        with open('durations.txt', 'a') as f:
            f.write('%s: %s\n' % (key, duration))
    except OSError as ex: #(5)
        if ex.errno == errno.EACCES: #(6)
            print 'durations.txt in use, cannot record.'
        else:
            _reporting_enabled = False #(7)
            traceback.print_exc()
            print 'Disabling metrics recording.'


_report_duration = _report_duration_FULL


def foo():
    """
>>> record_duration = record_duration_PRINT

>>> @record_duration
... def expensive_func():
...     time.sleep(.1)
...     return 'whew'
>>> result = expensive_func()
__main__.expensive_func took 0.099...s
>>> result
'whew'

>>> record_duration = record_duration_FINAL

>>> @record_duration
... def expensive_func():
...     time.sleep(.1)
...     return 'whew'
>>> expensive_func()
'whew'
>>> expensive_func()
'whew'
"""

if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)

