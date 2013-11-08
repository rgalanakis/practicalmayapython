import threading
import time
import types

# Version 1

def _getkey(func):
    return


def record_duration(func):
    def inner(*args, **kwargs):
        return func(*args, **kwargs)
    return inner


# Version 2

def _getkey(func):
    if isinstance(func, types.FunctionType):
        return '%s.%s' % (func.__module__, func.__name__)
    if isinstance(func, types.MethodType):
        return '%s.%s.%s' % (func.__module__,
                             func.im_class.__name__,
                             func.__name__)
    raise TypeError('%s must be a function or method' % func)


def record_duration(func):
    key = _getkey(func)

    def inner(*args, **kwargs):
        return func(*args, **kwargs)

    return inner

# Version 3

def record_duration(func):
    key = _getkey(func)

    def inner(*args, **kwargs):
        start = time.clock()
        result = func(*args, **kwargs)
        duration = time.clock() - start
        return result

    return inner


def _report_duration(key, duration):
    with open(r'\\myshare\mayapymetrics\durations.txt', 'a') as f:
        f.write('%s %s: %s\n' % (
            datetime.datetime.now().isoformat(), key, duration))


# Version 4

PROFILEPATH = r'\\myshare\mayapymetrics\durations.txt'


def _report_duration(key, duration):
    try:
        with open(PROFILEPATH, 'a') as f:
            f.write('%s %s: %s\n' % (
                datetime.datetime.now().isoformat(),
                key,
                duration))
    except (IOError, OSError):
        traceback.print_exc()


# Version 5

def _report_duration(key, duration):
    if getattr(_report_duration, '_disabled', False):
        return
    try:
        with open(PROFILEPATH, 'a') as f:
            f.write('%s %s: %s\n' % (
                datetime.datetime.now().isoformat(),
                key,
                duration))
    except (IOError, OSError) as ex:
        if ex.errno == errno.ENOENT:
            _report_duration._disabled = True
        traceback.print_exc()


# Version 6

import datetime
import errno
import time
import traceback


def record_duration(func):
    """Records how long a function took to run.
    Can only be used on functions and methods.
    """
    key = _getkey(func)

    def inner(*args, **kwargs):
        start = time.clock()
        result = func(*args, **kwargs)
        duration = time.clock() - start
        _report_duration(key, duration)
        return result

    return inner


def _report_duration(key, duration):
    if getattr(_report_duration, '_disabled', False):
        return
    try:
        with open(PROFILEPATH, 'a') as f:
            f.write('%s %s: %s\n' % (
                datetime.datetime.now().isoformat(),
                key,
                duration))
    except (IOError, OSError) as ex:
        if ex.errno == errno.ENOENT:
            _report_duration._disabled = True
        traceback.print_exc()


def _getkey(func):
    if isinstance(func, types.FunctionType):
        return '%s.%s' % (func.__module__, func.__name__)
    if isinstance(func, types.MethodType):
        return '%s.%s.%s' % (func.__module__,
                             func.im_class.__name__,
                             func.__name__)
    raise TypeError('%s must be a function or method' % func)
