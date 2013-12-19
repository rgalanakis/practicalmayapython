"""
Shows how to launch Maya from Python, including:

- launching process
- process handle inheritance
- kill a proc
- use atexit

No server yet.
"""
import os
import subprocess

# (1)
MAYAEXE = r'C:\Program Files\Autodesk\Maya 2011 Subscription Advantage Pack\bin\mayabatch.exe'#r'C:\Program Files\Autodesk\Maya2014\bin\maya.exe'
MAYAPYLIB = r'C:\pydev\practicalmayapython\src\chapter6'#r'C:\mayapybook\pylib'


def start_process():
    process = subprocess.Popen([MAYAEXE]) # (3)
    return process

def kill(pid):
    if os.name == 'nt':
        os.system('taskkill /f /pid %s' % pid)
    else:
        os.system('kill -SIGKILL %s' % pid)

if __name__ == '__main__':
    import time
    proc = start_process()
    time.sleep(5) # (4)
    kill(proc.pid)

import atexit

def start_process():
    process = subprocess.Popen([MAYAEXE]) # (3)
    atexit.register(kill, process.pid)


if __name__ == '__main__':
    import time
    start_process()
