
def adder(a, b):
    """
    Return a added to b.

    >>> adder(1, 3)
    3
    >>> adder('a', 'b')
    'ab'
    >>> adder(1, 'b')
    Traceback (most recent call last):
    TypeError: unsupported operand type(s) for +: 'int' and 'str'
    """
    return a + b
