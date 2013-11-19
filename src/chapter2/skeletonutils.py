# Version 1

def convert_to_skeleton(rootnode, prefix='skel_', _parent=None):
    """Converts a hierarchy of nodes into joints that have the
    same transform, with their name prefixed with `prefix`.
    Return the newly created root node.
    The new hierarchy will share the same parent as rootnode.

    :param rootnode: The root PyNode.
      Everything under it will be converted.
    :param prefix: String to prefix newly created nodes with.
    """
    # Create a joint from the given node with the new name.
    # Copy the transform and rotation.
    # Set the parent to rootnode's parent if _parent is None,
    # Otherwise set it to _parent.
    # Convert all the children recursively.



# Version 2

def convert_to_skeleton(rootnode, prefix='skel_', _parent=None):
    """Converts a hierarchy of nodes into joints that have the
    same transform, with their name prefixed with `prefix`.
    Return the newly created root node.
    The new hierarchy will share the same parent as rootnode.

    :param rootnode: The root PyNode.
      Everything under it will be converted.
    :param prefix: String to prefix newly created nodes with.
    """
    # Create a joint from the given node with the new name.
    j = pmc.joint(name=prefix + rootnode.name())
    # Copy the transform and rotation.
    j.translation.set(rootnode.translation.get())
    j.rotation.set(rootnode.rotation.get())
    # Set the parent to rootnode's parent if _parent is None,
    # Otherwise set it to _parent.
    if _parent is None:
        _parent = rootnode.getParent()
    j.setParent(_parent)
    # Convert all the children recursively.
    for c in rootnode.children():
        convert_to_skeleton(c, prefix, j)
    return j



# Version 3

def safeSetParent(node, parent):
    """`node.setParent(parent)` if `parent` is
    not the same as `node`'s existing parent.
    """
    if node.getParent() != parent:
        node.setParent(parent)

def convert_to_skeleton(rootnode, prefix='skel_'):
    j = pmc.joint(name=prefix + rootnode.name())
    safeSetParent(j, rootnode.getParent())
    j.translation.set(rootnode.translation.get())
    j.rotation.set(rootnode.rotation.get())
    for c in rootnode.children():
        convert_to_skeleton(c, prefix)
    return j

# Version 4

def _convert_to_joint(node, prefix):
    j = pmc.joint(name=prefix + node.name())
    j.translation.set(node.translation.get())
    j.rotation.set(node.rotation.get())
    return j

def convert_to_skeleton(rootnode, prefix='skel_'):
    j = _convert_to_joint(rootnode, prefix)
    safeSetParent(j, rootnode.getParent())
    for c in rootnode.children():
        convert_to_skeleton(c, prefix)
    return j

# Version 5

GREEN = 1
BLUE = 2
YELLOW = 3

def _convert_to_joint(node, prefix):
    j = pmc.joint(name=prefix + node.name())
    j.translation.set(node.translation.get())
    j.rotation.set(node.rotation.get())
    x = j.translate.x.get()
    if x < 0.001:
        col = GREEN
    elif x > 0.001:
        col = BLUE
    else:
        col = YELLOW
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
            return GREEN
        elif x > 0.001:
            return BLUE
        else:
            return YELLOW
    j.wireColor.set(calc_wirecolor())
    return j

# Verison 7

def _convert_to_joint(node, prefix):
    j = pmc.joint(name=prefix + node.name())
    j.translation.set(node.translation.get())
    j.rotation.set(node.rotation.get())
    def calc_wirecolor():
        x = j.translate.x.get()
        if x < 0.001:
            return GREEN
        elif x > 0.001:
            return BLUE
        else:
            return YELLOW
    j.wireColor.set(calc_wirecolor())
    return j

def convert_to_skeleton(rootnode, prefix='skel_'):
    """Converts a hierarchy of nodes into joints that have the
    same transform, with their name prefixed with `prefix`.
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

def ancestors(node):
    """Return a list of ancestors, starting with the direct parent
    and ending with the top-level (root) parent."""
    result = []
    parent = node.getParent()
    while parent is not None:
        result.append(parent)
        parent = parent.getParent()
    return result


def uniqueroots(nodes): #(1)
    """Returns a list of the nodes in `nodes` that are not
    children of any node in `nodes`."""
    result = []
    def handle_node(n): #(2)
        """If any of the ancestors of n are in realroots,
        just return, otherwise, append n to realroots.
        """
        for ancestor in ancestors(n):
            if ancestor in nodes: #(4)
                return
        result.append(n) #(5)
    for node in nodes: #(3)
        handle_node(node)
    return result

# VERSION

def _convert_to_joint(node, prefix , jnt_size, lcol, rcol, ccol):
    j = pmc.joint(name=prefix + node.name())
    j.translation.set(node.translation.get())
    j.rotation.set(node.rotation.get())
    j.setJointSize(jnt_size)
    def calc_wirecolor():
        x = j.translate.x.get()
        if x < -0.001:
            return rcol
        elif x > 0.001:
            return lcol
        else:
            return ccol
    j.overrideColor.set(calc_wirecolor())
    return j

def convert_to_skeleton(
        rootnode,
        prefix='skel_',
        joint_size=1.0,
        lcol=BLUE,
        rcol=GREEN,
        ccol=YELLOW):
    j = _convert_to_joint(
        rootnode, prefix, joint_size, lcol, rcol, ccol)
    safeSetParent(j, rootnode.getParent())
    for c in rootnode.children():
        convert_to_skeleton(
            c, prefix, joint_size, lcol, rcol, ccol)
    return j
