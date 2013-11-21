import pymel.core as pmc
import skeletonutils

def convert_hierarchies_main():
    """`convert_hierarchies(pmc.selection())`.
    Prints and provides user feedback so only call from UI.
    """
    nodes = pmc.selected(type='transform') #(1)
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
    result = [convert_hierarchy(r) for r in roots]
    return result


def convert_hierarchy(node):
    """Converts the hierarchy under and included `rootnode`
    into joints in the same namespace as `rootnode`.
    Deletes `rootnode` and its hierarchy.
    Connections to nodes are not preserved on the newly
    created joints.
    """
    result = skeletonutils.convert_to_skeleton(node)
    pmc.delete(node)
    return result


# (1)
GREEN = 14
BLUE = 6
YELLOW = 17
PURPLE = 8
AQUA = 28

SETTINGS_DEFAULT = {
    'joint_size': 1.0,
    'right_color': BLUE,
    'left_color': GREEN,
    'center_color': YELLOW,
    'prefix': 'char_',
}
SETTINGS_GAME2 = {
    'joint_size': 25.0,
    'right_color': PURPLE,
    'left_color': AQUA,
    'center_color': GREEN,
    'prefix': 'game2char_',
}

#(2)
def convert_hierarchies_main(settings=SETTINGS_DEFAULT):
    nodes = pmc.selected(type='transform')
    if not nodes:
        pmc.warning('No transforms selected.')
        return
    new_roots = convert_hierarchies(nodes, settings)
    print 'Created:', ','.join([r.name() for r in new_roots])

#(2)
def convert_hierarchies(rootnodes, settings=SETTINGS_DEFAULT):
    roots = skeletonutils.uniqueroots(rootnodes)
    result = [convert_hierarchy(r, settings) for r in roots]
    return result

# (2)
def convert_hierarchy(rootnode,  settings=SETTINGS_DEFAULT):
    result = skeletonutils.convert_to_skeleton( #(3)
        rootnode,
        joint_size=settings['joint_size'],
        prefix=settings['prefix'],
        rcol=settings['right_color'],
        lcol=settings['left_color'],
        ccol=settings['center_color'])
    pmc.delete(rootnode)
    return result
