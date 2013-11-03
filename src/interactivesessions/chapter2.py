"""
>>> import maya.cmds as cmds
>>> mynode = cmds.transform()
>>> cmds.listConnections(mynode, type='transform')

"""

if __name__ == "__main__":
    import doctest
    doctest.testmod()
