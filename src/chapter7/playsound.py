# noinspection PyUnresolvedReferences
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'chapter5'))

import os
from qtshim import QtGui

GOBBLE = os.path.join(os.path.dirname(__file__), 'gobble.wav')
GORILLA = os.path.join(os.path.dirname(__file__), 'gorilla.wav')

def play_sound(wav=GOBBLE):
    QtGui.QSound.play(wav)


def testPlay():
    """
>>> import playsound, time
>>> playsound.play_sound(GOBBLE)
>>> time.sleep(2)
>>> playsound.play_sound(GORILLA)
>>> time.sleep(2)
"""

if __name__ == '__main__':
    import doctest
    doctest.testmod()
