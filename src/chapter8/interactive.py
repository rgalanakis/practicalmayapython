
def interactive():
    # noinspection PySingleQuotedDocstring
    '''
>>> s = '+'.join([str(i) for i in range(1, 6)])
>>> s
'1+2+3+4+5'
>>> eval(s)
15

>>> sum(range(1, 6))
15

>>> def _make_sort(reverse):
...     def dosort(items):
...         return sorted(items, reverse=reverse)
...     return dosort
>>> sort_ascending = _make_sort(False)
>>> sort_descending = _make_sort(True)
>>> sort_ascending([1, 3, 2])
[1, 2, 3]
>>> sort_descending([1, 3, 2])
[3, 2, 1]

>>> class Dog(object):
...     def make_sound(self):
...         print 'Woof!'
>>> class Cat(object):
...     def make_sound(self):
...         print 'Meow!'
>>> Dog().make_sound()
Woof!
>>> Cat().make_sound()
Meow!

>>> template = """class %s(object):
...     def make_sound(self):
...         print '%s'"""
>>> exec template % ('Bird', 'Tweet')
>>> Bird().make_sound()
Tweet
>>> exec template % ('Mouse', 'Squeek')
>>> Mouse().make_sound()
Squeek

>>> class Cow(object):
...     def make_sound(self):
...         print 'Moo'

>>> c = Cow()
>>> c
<__main__.Cow object at 0x0...>
>>> type(c)
<class '__main__.Cow'>

>>> def make_animal(name, sound): #(1)
...     def mksound(self): #(2)
...         print sound
...     return type(name, (object,), {'make_sound': mksound}) #(3)
>>> Fish = make_animal('Fish', 'Blub') #(4)
>>> Fish
<class '__main__.Fish'>
>>> make_animal('Seal', 'Ow ow ow')() #(5)
<__main__.Seal object at 0x0...>
>>> make_animal('Fox', '?')().make_sound() #(6)
?

>>> values = [-7, 2, -1]
>>> decorated = [(abs(v), v) for v in values]
>>> decorated.sort()
>>> [v for (absval, v) in decorated]
[-1, 2, -7]
>>> sorted(values, key=abs) # You should actually sort this way
[-1, 2, -7]

>>> def add(a, b): # Our 'full' function
...     return a + b
>>> def partial_add(a):
...     def add2(b): # Create a closure
...         return add(a, b)
...     return add2
>>> adder = partial_add(1) # Create the partial function.
>>> adder(2) # Call the partial function
3


'''
import math

def sin_xformer(input, scale, frames):
    angle = 6.2831853 * (input / frames)
    return math.sin(angle) * scale


sin = sin_xformer(3.0, 4.0, 12.0)
assert 4.0 == sin, sin

if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
