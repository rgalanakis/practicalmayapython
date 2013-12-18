"""
Shows how to launch Maya from Python,
including environment setup.
No server yet.
"""
import os
import subprocess

def create_client():
    exe = r'C:\Program Files\Autodesk\Maya 2011 Subscription Advantage Pack\bin\mayabatch.exe'#r'C:\Program Files\Autodesk\Maya2014\bin\maya.exe'
    mayalib = r'C:\pydev\practicalmayapython\src\chapter6'#r'C:\mayapybook\pylib'
    environ = dict(os.environ)
    pypath = environ.get('PYTHONPATH', '')
    environ['PYTHONPATH'] = os.pathsep.join([pypath, mayalib])
    p = subprocess.Popen([exe], env=environ)
    p.kill()

if __name__ == '__main__':
    create_client()
