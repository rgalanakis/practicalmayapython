
def interactive():
    """
    Code for all the interactive prompts throughout the chapter.

>>> eval('1 + 1')
2
>>> a = eval('1 + 2')
>>> a
3
>>> eval('print 1')
Traceback (most recent call last):
  ...
  File "<string>", line 1
     print 1
         ^
SyntaxError: invalid syntax

>>> exec '1 + 1'
>>> exec 'b = 1 + 2'
>>> b
3
>>> exec 'print 1'
1
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()

  