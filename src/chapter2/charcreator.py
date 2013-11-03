# Version 1

import pymel.core as pmc
import skeletonutils


def convert_hierarchy(rootnode):
    """Converts the hierarchy under and included 'rootnode'
    into joints in the same namespace as 'rootnode'.
    Deletes 'rootnode' and its hierarchy.
    Connections to nodes are not preserved on the newly
    created joints.
    """


def convert_hierarchies(rootnodes):
    """Calls 'convert_hierarchy' for each root node in 'rootnodes'
    (so passing in '[parent, child]' would convert the 'parent'
    hierarchy assuming 'child' lives under it).
    """


def convert_hierarchies_main():
    """'convert_hierarchies(pmc.selection())'.
    Prints and provides user feedback so only call from UI.
    """


# Version 2

def convert_hierarchies_main():
    nodes = pmc.selection(type='transform')
    if not nodes:
        pmc.warning('No transforms selected.')
        return
    new_roots = convert_hierarchies(nodes)
    print 'Created:', ','.join([r.name() for r in new_roots])

# Version 3

def convert_hierarchies(rootnodes):
    roots = skeletonutils.trueroots(rootnodes)
    for r in roots:
        convert_hierarchy(r)


# Version 4
import namespaceutils


def convert_hierarchy(node):
    with namespaceutils.as_current(node.parentNamespace()):
        skeletonutils.convert_to_skeleton(node)
    pmc.delete(node)


# Version 5

import pymel.core as pmc
import namespaceutils
import skeletonutils

SETTINGS_DEFAULT = {
    'joint_size': 1.0,
    'right_color': (0, 255, 0),
    'left_color': (0, 0, 255),
    'center_color': (0, 255, 255),
    'prefix': 'char_',
}
SETTINGS_GAME2 = {
    'joint_size': 25.0,
    'right_color': (255, 0, 0),
    'left_color': (0, 0, 0),
    'center_color': (255, 255, 0),
    'prefix': 'gamechar_',
}


def convert_hierarchy(rootnode, settings=SETTINGS_DEFAULT):
    with namespaceutils.as_current(rootnode.parentNamespace()):
        skeletonutils.convert_to_skeleton(
            rootnode,
            jointsize=settings['joint_size'],
            prefix=settings['prefix'],
            rcol=settings['right_color'],
            lcol=settings['left_color'],
            ccol=settings['center_color'])
        pmc.delete(rootnode)


def convert_hierarchies(rootnodes, settings=SETTINGS_DEFAULT):
    roots = skeletonutils.trueroots(rootnodes)
    for r in roots:
        convert_hierarchy(r, settings)


def convert_hierarchies_main(settings=SETTINGS_DEFAULT):
    nodes = pmc.selection(type='transform')
    if not nodes:
        pmc.warning('No transforms selected.')
        return
    new_roots = convert_hierarchies(nodes, settings)
    print 'Created:', ','.join([r.name() for r in new_roots])
