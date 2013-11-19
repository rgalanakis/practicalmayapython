import pymel.core as pmc
import skeletonutils

def convert_hierarchies_main():
    """`convert_hierarchies(pmc.selection())`.
    Prints and provides user feedback so only call from UI.
    """
    nodes = pmc.selection(type='transform') #(1)
    if not nodes:
        pmc.warning('No transforms selected.') #(2)
        return
    new_roots = convert_hierarchies(nodes) #(3)
    print 'Created:', ','.join([r.name() for r in new_roots]) #(4)


def convert_hierarchies(rootnodes):
    """Calls `convert_hierarchy` for each root node in `rootnodes`
    (so passing in `[parent, child]` would convert the `parent`
    hierarchy assuming `child` lives under it).
    """
    roots = skeletonutils.uniqueroots(rootnodes)
    for r in roots:
        convert_hierarchy(r)


def convert_hierarchy(node):
    """Converts the hierarchy under and included `rootnode`
    into joints in the same namespace as `rootnode`.
    Deletes `rootnode` and its hierarchy.
    Connections to nodes are not preserved on the newly
    created joints.
    """
    skeletonutils.convert_to_skeleton(node)
    pmc.delete(node)


import pymel.core as pmc
import skeletonutils

# (1)
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

# (2)
def convert_hierarchy(rootnode,  settings=SETTINGS_DEFAULT):
    skeletonutils.convert_to_skeleton( #(3)
        node,
         jointsize=settings['joint_size'],
        prefix=settings['prefix'],
        rcol=settings['right_color'],
        lcol=settings['left_color'],
        ccol=settings['center_color'])
    pmc.delete(node)

#(2)
def convert_hierarchies(rootnodes, settings=SETTINGS_DEFAULT):
    roots = skeletonutils.trueroots(rootnodes)
    for r in roots:
        convert_hierarchy(r, settings)

#(2)
def convert_hierarchies_main(settings=SETTINGS_DEFAULT):
    nodes = pmc.selection(type='transform')
    if not nodes:
        pmc.warning('No transforms selected.')
        return
    new_roots = convert_hierarchies(nodes, settings)
    print 'Created:', ','.join([r.name() for r in new_roots])
