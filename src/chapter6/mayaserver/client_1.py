"""
Shows how to launch Maya from Python, including:

- launching process
- process handle inheritance

No server yet.
"""

import subprocess
import time

# (1)
MAYAEXE = r'C:\Program Files\Autodesk\Maya 2011 Subscription Advantage Pack\bin\mayabatch.exe'#r'C:\Program Files\Autodesk\Maya2014\bin\maya.exe'
MAYAPYLIB = r'C:\pydev\practicalmayapython\src\chapter6'#r'C:\mayapybook\pylib'


def start_process():
    process = subprocess.Popen([MAYAEXE]) # (3)
    return process


if __name__ == '__main__':
    start_process()
    time.sleep(5) # (4)
