# Version 1

def convert_to_skeleton(rootnode, prefix='skel_'):
    """Converts a hierarchy of nodes into joints that have the
    same transform, with their name prefixed with 'prefix'.
    Return the newly created root node.

    :param rootnode: The root PyNode.
      Everything under it will be converted.
    :param prefix: String to prefix newly created nodes with.
    """
    # For each node starting at the root,
    # convert it, convert the children,
    # and parent the children to the node.
    # Function will probably be recursive.


# Version 2

import pymel.core as pmc


def convert_to_skeleton(rootnode, prefix='skel_'):
    """Converts a hierarchy of nodes into joints that have the
    same transform, with their name prefixed with 'prefix'.
    Return the newly created root node.

    :param rootnode: The root PyNode.
      Everything under it will be converted.
    :param prefix: String to prefix newly created nodes with.
    """
    j = pmc.joint(name=prefix + rootnode.name())
    j.setParent(rootnode.getParent())
    j.translation.set(rootnode.translation.get())
    j.rotation.set(rootnode.rotation.get())
    for c in rootnode.children():
        convert_to_skeleton(c, prefix)
    return j


# Version 3

def safeSetParent(node, parent):
    """'node.setParent(parent)' if 'parent' is
    not the same as 'node''s existing parent.
    """
    if node.getParent() != parent:
        node.setParent(parent)


def convert_to_skeleton(rootnode, prefix='skel_'):
    j = pmc.joint(name=prefix + rootnode.name())
    safeSetParent(j, rootnode.getParent())
    j.translate.set(rootnode.translation.get())
    j.rotate.set(rootnode.rotation.get())
    for c in rootnode.getChildren():
        convert_to_skeleton(c, prefix)
    return j

# Version 4

def _convert_to_joint(node, prefix):
    j = pmc.joint(name=prefix + node.name())
    j.translation.set(node.translate.get())
    j.rotation.set(node.rotate.get())
    return j


def convert_to_skeleton(rootnode, prefix='skel_'):
    j = _convert_to_joint(rootnode, prefix)
    safeSetParent(j, rootnode.getParent())
    for c in rootnode.children():
        convert_to_skeleton(c, prefix)
    return j


# Version 5

def _convert_to_joint(node, prefix):
    j = pmc.joint(name=prefix + node.name())
    j.translation.set(node.translation.get())
    j.rotation.set(node.rotation.get())
    x = j.translate.x.get()
    if x < 0.001:
        col = (0, 255, 0)
    elif x > 0.001:
        col = (0, 0, 255)
    else:
        col = (0, 255, 255)
    j.wireColor.set(col)
    return j

# Version 6

def _convert_to_joint(node, prefix):
    j = pmc.joint(name=prefix + node.name())
    j.translation.set(node.translation.get())
    j.rotation.set(node.rotation.get())

    def calc_wirecolor():
        x = j.translate.x.get()
        if x < 0.001:
            return 0, 255, 0
        elif x > 0.001:
            return 0, 0, 255
        else:
            return 0, 255, 255

    j.wireColor.set(calc_wirecolor())
    return j

# Version 7

def _convert_to_joint(node, prefix):
    j = pmc.joint(name=prefix + node.name())
    j.translation.set(node.translation.get())
    j.rotation.set(node.rotation.get())

    def calc_wirecolor():
        x = j.translate.x.get()
        if x < 0.001:
            return 0, 255, 0
        elif x > 0.001:
            return 0, 0, 255
        else:
            return 0, 255, 255

    j.wireColor.set(calc_wirecolor())
    return j


def convert_to_skeleton(rootnode, prefix='skel_'):
    """Converts a hierarchy of nodes into joints that have the
    same transform, with their name prefixed with 'prefix'.
    Return the newly created root node.

    :param rootnode: The root PyNode.
      Everything under it will be converted.
    :param prefix: String to prefix newly created nodes with.
    """

    j = _convert_to_joint(rootnode, prefix)
    safeSetParent(j, rootnode.getParent())
    for c in rootnode.children():
        convert_to_skeleton(c, prefix)
    return j

# Version 7

def ancestors(node):
    """Return a list of ancestors, starting with the direct parent
    and ending with the top-level (root) parent."""

    ancestors = []
    parent = node.getParent()
    while parent is not None:
        ancestors.append(parent)
        parent = node.getParent()
    return ancestors

# Version 8

def trueroots(nodes):
    """Returns a list of the nodes in 'nodes' that are not
    children of any node in 'nodes'."""
    result = []

    def handle_node(n):
        """If any of the ancestors of n are in realroots,
        just return, otherwise, append n to realroots.
        """
        for ancestor in ancestors(n):
            if ancestor in result:
                return
        result.append(n)

    for node in nodes:
        handle_node(node)

# Version 9

def _convert_to_joint(node, prefix, lcol, rcol, ccol):
    j = pmc.joint(name=prefix + node.name())
    j.translation.set(node.translation.get())
    j.rotation.set(node.rotation.get())

    def calc_wirecolor():
        x = j.translate.x.get()
        if x < -0.001:
            return rcol
        elif x > 0.001:
            return lcol
        else:
            return ccol

    j.wireColor.set(calc_wirecolor())
    return j


def convert_to_skeleton(rootnode,
                        prefix='skel_',
                        lcol=(0, 0, 255),
                        rcol=(0, 255, 0),
                        ccol=(0, 255, 255)):
    j = _convert_to_joint(rootnode, prefix, lcol, rcol, ccol)
    safeSetParent(j, rootnode.getParent())
    for c in rootnode.children():
        convert_to_skeleton(c, prefix, lcol, rcol, ccol)
    return j