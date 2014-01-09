
#myset.py
_state = {}
def add(v):
    _state[v] = None
def remove(v):
    del _state[v]
def items():
    return _state.keys()


#myset.py
class MySet(object):
    def __init__(self):
        self._state = {}
    def add(self, v):
        self._state[v] = None
    def remove(self, v):
        del self._state[v]
    def items(self):
        return self._state.keys()
