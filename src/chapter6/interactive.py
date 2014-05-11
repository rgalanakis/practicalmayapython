
def interactive():
    """
    Code for all the interactive prompts throughout the chapter.

>>> eval('1 + 1')
2
>>> exec '1 + 1'


>>> exec 'print 1'
1
>>> eval('print 1')
Traceback (most recent call last):
  ...
  File "<string>", line 1
     print 1
         ^
SyntaxError: invalid syntax

>>> exec 'b = 1 + 1'
>>> eval('b')
2

>>> def exec2(s):
...     exec s
>>> exec2('c = 2 + 2')
>>> eval('c')
Traceback (most recent call last):
NameError: name 'c' is not defined

>>> def exec3(s):
...     exec s in globals(), globals()
>>> exec3('d = 3 + 3')
>>> eval('d', globals(), globals())
6

>>> 'e' in globals()
False
>>> e = 1
>>> 'e' in globals() # Normal assignment puts e in globals
True
>>> 'f' in globals()
False
>>> exec 'f = 1'
>>> 'f' in globals() # Assignment in exec puts f in globals
True
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()

  