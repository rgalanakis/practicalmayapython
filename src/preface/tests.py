
def tests():
    """
>>> def spam():
...     return 'spam!'
>>> spam()
'spam!'

>>> def more_spam():
...     spams = ' '.join([spam()] * 5)
...     return spams
>>> more_spam()
'spam! spam! spam! spam! spam!'


>>> 'This is input'.replace('in', 'out')
'This is output'
>>> if True:
...     print 'Hello!'
Hello!
"""

if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
