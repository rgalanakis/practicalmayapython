def is_exact_type(node, typename):
    """node.type() == typename"""
    return node.type() == typename


def is_type(node, typename):
    """Return True if node.type() is typename or
    any subclass of typename."""
    return typename in node.nodeType(inherited=True)
