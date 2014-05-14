class MySet(object):
    def __init__(self):
        self._state = {}
    def add(self, v):
        self._state[v] = None
    def remove(self, v):
        del self._state[v]
    def items(self):
        return self._state.keys()
