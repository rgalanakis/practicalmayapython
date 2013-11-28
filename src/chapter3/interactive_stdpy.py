"""excepthook doesn't work in doctest, since it catches the error.
The interactive code is here, as well as a demo to show how excepthook
works.
Running this script will print 'Hello!' and print an error.
"""

def interactive():
    """

>>> 1 + '1'
Traceback (most recent call last):
TypeError: unsupported operand type(s) for +: 'int' and 'str'

>>> import sys
>>> def ehook(etype, evalue, tb):
...     print 'Hello!'
>>> sys.excepthook = ehook
>>> 1 + '1'
Hello!

    """


if __name__ == "__main__":
    import sys
    def excepthook(etype, evalue, tb):
        print 'Hello!'
    sys.excepthook = excepthook
    1 + '1'
