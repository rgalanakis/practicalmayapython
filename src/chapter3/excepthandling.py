# Version 1

import sys


def excepthook(etype, evalue, tb):
    print 'Hello!'


sys.excepthook = excepthook

# Version 2

def excepthook(etype, evalue, tb):
    sys.__excepthook__(etype, evalue, tb)
    print 'An unhandled exception occurred.'
    print 'Please copy the error info above this message'
    print 'and a copy of this file and email it to'
    print 'mayasupport@robg3d.com. You should get a response'
    print 'in three days or less.'


sys.excepthook = excepthook


# Version 3

import os
import sys


def _normalize(p):
    return os.path.normpath(os.path.abspath(p))


LIB_DIR = _normalize(os.path.dirname(__file__))

_orig_excepthook = sys.excepthook


def _handle_our_exc(etype, evalue, tb):
    sys.__excepthook__(etype, evalue, tb)
    print 'An unhandled exception occurred.'
    print 'Please copy the error info above this message'
    print 'and a copy of this file and email it to'
    print 'mayasupport@robg3d.com. You should get a response'
    print 'in three days or less.'


def _is_important_tb(tb):
    while tb:
        codepath = tb.tb_frame.f_code.co_filename
        if _normalize(codepath).startswith(LIB_DIR):
            return True
        tb = tb.tb_next
    return False


def excepthook(etype, evalue, tb):
    if _is_important_tb(tb):
        _handle_our_exc(etype, evalue, tb)
    else:
        _orig_excepthook(etype, evalue, tb)

# Version 4

import os
import sys

__author__ = 'rob.galanakis@gmail.com'

_orig_excepthook = sys.excepthook


def _handle_our_exc(etype, evalue, tb):
    sys.__excepthook__(etype, evalue, tb)
    print 'An unhandled exception occurred.'
    print 'Please copy the error info above this message'
    print 'and a copy of this file and email it to'
    print 'mayasupport@robg3d.com. You should get a response'
    print 'in three days or less.'


def _is_important_tb(tb):
    while tb:
        auth = tb.tb_frame.f_globals.get('__author__')
        if auth == __author__:
            return True
        tb = tb.tb_next
    return False


def excepthook(etype, evalue, tb):
    if _is_important_tb(tb):
        _handle_our_exc(etype, evalue, tb)
    else:
        _orig_excepthook(etype, evalue, tb)


# Version 5

import os
import platform
import pymel.core as pmc
import sys


def _collect_info():
    lines = []
    lines.append('Scene Info')
    lines.append('  Maya Scene: ' + pmc.sceneName())
    lines.append('Maya/Python Info')
    lines.append('  Maya Version: ' + pmc.about(version=True))
    lines.append('  Qt Version: ' + pmc.about(qtVersion=True))
    lines.append('  Maya64: ' + str(pmc.about(is64=True)))
    lines.append('  PyVersion: ' + sys.version)
    lines.append('  PyExe: ' + sys.executable)
    lines.append('Machine Info')
    lines.append('  OS: ' + pmc.about(os=True))
    lines.append('  Node: ' + platform.node())
    lines.append('  OSRelease: ' + platform.release())
    lines.append('  OSVersion: ' + platform.version())
    lines.append('  Machine: ' + platform.machine())
    lines.append('  Processor: ' + platform.processor())
    lines.append('Environment Info')
    lines.append('  EnvVars')
    for k in sorted(os.environ.keys()):
        lines.append('    %s: %s' % (k, os.environ[k]))
    lines.append('  SysPath')
    for p in sys.path:
        lines.append('    ' + p)


# Version 6

import os
import platform
import pymel.core as pmc
import sys


def _normalize(p):
    return os.path.normpath(os.path.abspath(p))


LIB_DIR = _normalize(os.path.dirname(__file__))

_orig_excepthook = sys.excepthook


def _collect_info():
    lines = []
    lines.append('Scene Info')
    lines.append('  Maya Scene: ' + pmc.sceneName())

    lines.append('Maya/Python Info')
    lines.append('  Maya Version: ' + pmc.about(version=True))
    lines.append('  Qt Version: ' + pmc.about(qtVersion=True))
    lines.append('  Maya64: ' + str(pmc.about(is64=True)))
    lines.append('  PyVersion: ' + sys.version)
    lines.append('  PyExe: ' + sys.executable)

    lines.append('Machine Info')
    lines.append('  OS: ' + pmc.about(os=True))
    lines.append('  Node: ' + platform.node())
    lines.append('  OSRelease: ' + platform.release())
    lines.append('  OSVersion: ' + platform.version())
    lines.append('  Machine: ' + platform.machine())
    lines.append('  Processor: ' + platform.processor())

    lines.append('Environment Info')
    lines.append('  EnvVars')
    for k in sorted(os.environ.keys()):
        lines.append('    %s: %s' % (k, os.environ[k]))
    lines.append('  SysPath')
    for p in sys.path:
        lines.append('    ' + p)

    return '\n'.join(lines)


def _handle_our_exc(etype, evalue, tb):
    sys.__excepthook__(etype, evalue, tb)
    print 'An unhandled exception occurred.'
    print 'Please copy the error info above this message'
    print 'and a copy of this file and email it to'
    print 'mayasupport@robg3d.com. You should get a response'
    print 'in three days or less.'
    print 'Collected Information:'
    print _collect_info()


def _is_important_tb(tb):
    while tb:
        codepath = tb.tb_frame.f_code.co_filename
        if _normalize(codepath).startswith(LIB_DIR):
            return True
        tb = tb.tb_next
    return False


def excepthook(etype, evalue, tb):
    if _is_important_tb(tb):
        _handle_our_exc(etype, evalue, tb)
    else:
        _orig_excepthook(etype, evalue, tb)


sys.excepthook = excepthook


# Version 7

from email.mime.text import MIMEText
import smtplib


def _send_email(body):
    em = MIMEText(body)
    em['To'] = ['mayasupport@robg3d.com']
    em['From'] = 'mayasupport@robg3d.com'
    em['Subject'] = 'Maya Tools Error'

    server = smtplib.SMTP('localhost')  # Your server here
    try:
        server.sendmail(em['From'], em['To'], em.as_string())
    finally:
        server.quit()


def _handle_our_exc(etype, evalue, tb):
    sys.__excepthook__(etype, evalue, tb)
    lines = traceback.format_exception(etype, evalue, tb)
    lines.append('\n')
    lines.append(_collect_info())
    msg = ''.join(lines)


# Version 8

from email.mime.text import MIMEText
import os
import platform
import pymel.core as pmc
import smtplib
import sys
import traceback


def _normalize(p):
    return os.path.normpath(os.path.abspath(p))


LIB_DIR = _normalize(os.path.dirname(__file__))

_orig_excepthook = sys.excepthook


def _collect_info():
    lines = []
    lines.append('Scene Info')
    lines.append('  Maya Scene: ' + pmc.sceneName())

    lines.append('Maya/Python Info')
    lines.append('  Maya Version: ' + pmc.about(version=True))
    lines.append('  Qt Version: ' + pmc.about(qtVersion=True))
    lines.append('  Maya64: ' + str(pmc.about(is64=True)))
    lines.append('  PyVersion: ' + sys.version)
    lines.append('  PyExe: ' + sys.executable)

    lines.append('Machine Info')
    lines.append('  OS: ' + pmc.about(os=True))
    lines.append('  Node: ' + platform.node())
    lines.append('  OSRelease: ' + platform.release())
    lines.append('  OSVersion: ' + platform.version())
    lines.append('  Machine: ' + platform.machine())
    lines.append('  Processor: ' + platform.processor())

    lines.append('Environment Info')
    lines.append('  EnvVars')
    for k in sorted(os.environ.keys()):
        lines.append('    %s: %s' % (k, os.environ[k]))
    lines.append('  SysPath')
    for p in sys.path:
        lines.append('    ' + p)

    return '\n'.join(lines)


def _send_email(body):
    em = MIMEText(body)
    em['To'] = ['mayasupport@robg3d.com']
    em['From'] = 'mayasupport@robg3d.com'
    em['Subject'] = 'Maya Tools Error'

    server = smtplib.SMTP('localhost')  # Your server here
    try:
        server.sendmail(em['From'], em['To'], em.as_string())
    finally:
        server.quit()


def _handle_our_exc(etype, evalue, tb):
    sys.__excepthook__(etype, evalue, tb)
    lines = traceback.format_exception(etype, evalue, tb)
    lines.append('\n')
    lines.append(_collect_info())
    msg = ''.join(lines)
    _send_email(msg)
    print 'Error caught, support email sent.'


def _is_important_tb(tb):
    while tb:
        codepath = tb.tb_frame.f_code.co_filename
        if _normalize(codepath).startswith(LIB_DIR):
            return True
        tb = tb.tb_next
    return False


def excepthook(etype, evalue, tb):
    if _is_important_tb(tb):
        _handle_our_exc(etype, evalue, tb)
    else:
        _orig_excepthook(etype, evalue, tb)


sys.excepthook = excepthook


# Version 9

def _handle_our_exc(etype, evalue, tb):
    # sys.__excepthook__ # Delete this line!
    lines = traceback.format_exception(etype, evalue, tb)
    lines.append('\n')
    lines.append(_collect_info())
    msg = ''.join(lines)
    _send_email(msg)
    print 'Error caught, support email sent.'


def excepthook(etype, evalue, tb):
    if _is_important_tb(tb):
        _handle_our_exc(etype, evalue, tb)
    _orig_excepthook(etype, evalue, tb)


# Version 10

def excepthook(etype, evalue, tb):
    if _is_important_tb(tb):
        _handle_our_exc(etype, evalue, tb)
        if _orig_excepthook != sys.__excepthook__:
            _orig_excepthook(etype, evalue, tb)
    else:
        _orig_excepthook(etype, evalue, tb)
