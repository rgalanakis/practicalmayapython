import pymel.core as pmc


def exactType(node, typename):
    return node.type() == typename


def isType(node, typename):
    types = pmc.nodeType(
        typename, inherited=True, isTypeName=True)
    return node.type() in types


class TypeFilter(object):

    def __init__(self, typename, exact=False):
        self.typename = typename
        self.exact = exact
        self.typenames = pmc.nodeType(
            self.typename, inherited=True, isTypeName=True)

    def isType(self, node):
        if self.exact:
            return node.type() == self.typename
        return node.type() in self.typenames
