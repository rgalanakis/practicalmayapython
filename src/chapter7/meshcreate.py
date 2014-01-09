def demo():
    """

# List multiplication

>>> [(0, 1)] * 2
[(0, 1), (0, 1)]

>>> value = [1]
>>> newlist = [value] * 2
>>> newlist
[[1], [1]]
>>> newlist[0].append('a')
>>> newlist
[[1, 'a'], [1, 'a']]

# Zip and unzip

>>> numbers = (1, 2)
>>> letters = ('a', 'b')
>>> zipped = zip(numbers, letters)
>>> print zipped
[(1, 'a'), (2, 'b')]
>>> unzipped = zip(*zipped)
>>> print unzipped
[(1, 2), ('a', 'b')]
>>> unzipped[0] == numbers
True
>>> unzipped[1] == letters
True

# Enumerate

>>> chars = 'ab'
>>> for i in range(len(chars)):
...     c = chars[i]
...     print 'Item %s is %r' % (i, c)
Item 0 is 'a'
Item 1 is 'b'

>>> for i, c in enumerate(chars):
...     print 'Item %s is %r' % (i, c)
Item 0 is 'a'
Item 1 is 'b'

    """

# Part I: Set up data

# meshcreate.py
from maya import OpenMaya
import pymel.core as pmc

vert_positions = [
    (1, 1, 1), (1, -1, 1), (-1, -1, 1), (-1, 1, 1), #front
    (1, 1, 1), (1, -1, 1), (1, -1, -1), (1, 1, -1), #right
    (1, 1, -1), (1, -1, -1), (-1, -1, -1), (-1, 1, -1), #back
    (-1, 1, 1), (-1, -1, 1), (-1, -1, -1), (-1, 1, -1), #left
    (1, 1, 1), (1, 1, -1), (-1, 1, -1), (-1, 1, 1), #top
    (1, -1, 1), (1, -1, -1), (-1, -1, -1), (-1, -1, 1), #bottom
]
# all faces have same UVs
vert_uvs = [(0, 0), (0, 1), (1, 1), (1, 0)] * 6
poly_counts = [4] * 6  #Six quad faces
poly_connections = [
    3, 2, 1, 0,
    4, 5, 6, 7,
    8, 9, 10, 11,
    15, 14, 13, 12,
    16, 17, 18, 19,
    23, 22, 21, 20
]


# Part II: Derive other data

def py_to_array(values, marray_type, projection=None): #(1)
    result = marray_type() #(2)
    for v in values: #(3)
        newv = v
        if projection is not None:
            newv = projection(v)
        result.append(newv) #(4)
    return result #(5)

def tuple_to_mpoint(p): #(6)
    return OpenMaya.MPoint(p[0], p[1], p[2])

#(7)
vert_pos_array = py_to_array(
    vert_positions,
    OpenMaya.MPointArray,
    tuple_to_mpoint)
poly_counts_array = py_to_array(
    poly_counts, OpenMaya.MIntArray)
poly_conns_array = py_to_array(
    poly_connections, OpenMaya.MIntArray)

ulist, vlist = zip(*vert_uvs)
uarray = py_to_array(ulist, OpenMaya.MFloatArray)
varray = py_to_array(vlist, OpenMaya.MFloatArray)

# Part II: Create the cube

def create_cube_1():
    mesh = OpenMaya.MFnMesh() #(1)
    mesh.create( #(2)
        len(vert_positions),
        len(poly_counts ),
        vert_pos_array,
        poly_counts_array,
        poly_conns_array
    )
    mesh.setUVs(uarray, varray) #(3)
    mesh.assignUVs(poly_counts_array, poly_conns_array) #(4)
    mesh.updateSurface() #(5)
    pmc.sets(
        'initialShadingGroup',
        edit=True, forceElement=mesh.name()) #(6)

# Test create_cube in Maya, should create a cube

# Part IV: Set up normal data

def get_normals_data():
    result = {}
    offset = 0
    for i, pcnt in enumerate(poly_counts):
        vertInds = poly_connections[offset:offset + pcnt]
        positions = [vert_positions[vind] for vind in vertInds]
        normals = [OpenMaya.MVector(p[0], p[1], p[2]).normal()
                   for p in positions]
        result[i] = (vertInds, normals)
        offset += pcnt
    return result
face_to_vert_inds_and_normals = get_normals_data()


# Part V: Final creator

def create_cube_2():
    mesh = OpenMaya.MFnMesh()
    mesh.create(
        len(vert_positions),
        len(poly_counts),
        vert_pos_array,
        poly_counts_array,
        poly_conns_array
    )
    mesh.setUVs(uarray, varray)
    mesh.assignUVs(poly_counts_array, poly_conns_array)

    items = face_to_vert_inds_and_normals.items()
    for faceInd, (vertInds, norms) in items:
        for vind, normal in zip(vertInds, norms):
            mesh.setFaceVertexNormal(normal, faceInd, vind)

    mesh.updateSurface()
    pmc.sets(
        'initialShadingGroup',
        edit=True, forceElement=mesh.name())


if __name__ == "__main__":
    import maya.standalone
    maya.standalone.initialize()
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
    create_cube_1()
    create_cube_2()
