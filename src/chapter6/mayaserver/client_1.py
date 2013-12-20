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

#(1)
MAYAEXE = r'C:\Program Files\Autodesk\Maya 2011 Subscription Advantage Pack\bin\mayabatch.exe'#r'C:\Program Files\Autodesk\Maya2014\bin\maya.exe'

def kill(process): #(2)
    if os.name == 'nt':
        os.system('taskkill /f /pid %s' % process.pid)
    else:
        process.terminate()

if __name__ == '__main__':
    import time
    proc = subprocess.Popen([MAYAEXE]) #(3)
    # proc = subprocess.Popen([MAYAEXE, '-batch'])
    time.sleep(5) #(4)
    kill(proc) #(5)


import atexit

def start_process():
    process = subprocess.Popen([MAYAEXE])
    atexit.register(kill, process)

if __name__ == '__main__':
    import time
    start_process()
    time.sleep(5)
