from maya import OpenMaya, OpenMayaMPx

class AttrSpec(object): #(1)
    def createfnattr(self):
        raise NotImplementedError()
    def getvalue(self, datahandle):
        raise NotImplementedError()
    def setvalue(self, datahandle, value):
        raise NotImplementedError()
    def create(self, fnattr, longname, shortname):
        raise NotImplementedError()
    def setdefault(self, fnattr, value):
        raise NotImplementedError()
    def allow_fields(self):
        return False

class _FloatAttr(AttrSpec): #(2)
    def createfnattr(self):
        return OpenMaya.MFnNumericAttribute()
    def getvalue(self, datahandle):
        return datahandle.asFloat()
    def setvalue(self, datahandle, value):
        datahandle.setFloat(value)
    def create(self, fnattr, longname, shortname):
        return fnattr.create(
            longname, shortname, OpenMaya.MFnNumericData.kFloat)
    def setdefault(self, fnattr, value):
        fnattr.setDefault(value)
A_FLOAT = _FloatAttr() #(3)

class _StringAttr(AttrSpec):
    def createfnattr(self):
        return OpenMaya.MFnTypedAttribute()
    def getvalue(self, datahandle):
        return datahandle.asString()
    def setvalue(self, datahandle, value):
        datahandle.setString(value)
    def create(self, fnattr, longname, shortname):
        return fnattr.create(longname, shortname, OpenMaya.MFnData.kString)
    def setdefault(self, fnattr, value):
        fnattr.setDefault(OpenMaya.MFnStringData().create(value))
A_STRING = _StringAttr()

class _EnumAttr(AttrSpec):
    def createfnattr(self):
        return OpenMaya.MFnEnumAttribute()
    def getvalue(self, datahandle):
        return datahandle.asInt()
    def setvalue(self, datahandle, value):
        datahandle.setInt(value)
    def create(self, fnattr, longname, shortname):
        return fnattr.create(longname, shortname)
    def setdefault(self, fnattr, value):
        fnattr.setDefault(value)
    def allow_fields(self):
        return True
A_ENUM = _EnumAttr()

class _ColorAttr(AttrSpec):
    def createfnattr(self):
        return OpenMaya.MFnNumericAttribute()
    def getvalue(self, datahandle):
        return datahandle.asFloatVector()
    def setvalue(self, datahandle, value):
        datahandle.setMFloatVector(OpenMaya.MFloatVector(*value))
    def create(self, fnattr, longname, shortname):
        return fnattr.createColor(longname, shortname)
    def setdefault(self, fnattr, value):
        fnattr.setDefault(*value)
A_COLOR = _ColorAttr()


class NodeSpec(object): #(1)
    def nodebase(self):
        raise NotImplementedError()
    def register(self, fnplugin, typename, typeid, create, init):
        raise NotImplementedError()
    def deregister(self, fnplugin, typeid):
        raise NotImplementedError()

class _DependsNode(NodeSpec): #(2)
    def nodebase(self):
        return (OpenMayaMPx.MPxNode,) #(3)
    def register(self, fnplugin, typename, typeid, create, init):
        fnplugin.registerNode( #(4)
            typename, typeid, create, init,
            OpenMayaMPx.MPxNode.kDependNode)
    def deregister(self, fnplugin, typeid): #(5)
        fnplugin.deregisterNode(typeid)
NT_DEPENDSNODE = _DependsNode() #(6)

class TransformMatrix(OpenMayaMPx.MPxTransformationMatrix):
    pass

class _TransformNode(NodeSpec):
    xform_typeid = OpenMaya.MTypeId(0x00000901)
    def nodebase(self):
        return (OpenMayaMPx.MPxTransform,)
    def _make_node_matrix(self):
        return OpenMayaMPx.asMPxPtr(TransformMatrix())
    def register(self, fnplugin, typename, typeid, create, init):
        fnplugin.registerTransform(
            typename, typeid, create, init,
            self._make_node_matrix, self.xform_typeid)
    def deregister(self, fnplugin, typeid):
        fnplugin.deregisterNode(typeid)
NT_TRANSFORMNODE = _TransformNode()

def create_attrmaker(
    attrspec, ln, sn, affectors=(), default=None,
    transformer=None, fields=()):

    if not attrspec.allow_fields() and fields:
        raise RuntimeError('%s is not configured to allow fields.' % attrspec)

    def inner(nodetype):
        attr = attrspec.createfnattr()
        plug = attrspec.create(attr, ln, sn)

        for name, value in fields:
            attr.addField(name, value)

        if default is not None:
            attrspec.setdefault(attr, default)

        isoutput = bool(affectors)
        isinput = not isoutput
        attr.setWritable(isinput)
        attr.setStorable(isinput)
        if isoutput:
            assert transformer, 'Must specify transformer.'
            nodetype.transformerdata[ln] = (
                affectors, transformer)

        nodetype.attr_descriptors[ln] = attrspec

        nodetype.addAttribute(plug)
        setattr(nodetype, ln, plug)

        for affectedby in affectors:
            inputplug = getattr(nodetype, affectedby)
            nodetype.attributeAffects(inputplug, plug)
    return inner


def float_input(ln, sn, **kwargs):
    return create_attrmaker(A_FLOAT, ln, sn, **kwargs)

def float_output(ln, sn, **kwargs):
    return create_attrmaker(A_FLOAT, ln, sn, **kwargs)


def create_node(nodespec, name, typeid, attrmakers, node_methods=None):
    if node_methods is None:
        node_methods = {}

    if 'compute' in node_methods:
        raise ValueError('Cannot override compute method.')

    transformerdata = {}
    attr_descriptors = {}
    def compute(mnode, plug, datablock):
        nodename, attrname = plug.name().split('.')
        if attrname not in transformerdata:
            return OpenMaya.MStatus.kUnknownParameter
        affectors, xformer = transformerdata[attrname]
        invals = []
        for inname in affectors:
            inplug = getattr(nodetype, inname)
            indata = datablock.inputValue(inplug)
            inval = attr_descriptors[inname].getvalue(indata)
            invals.append(inval)
        outval = xformer(*invals)
        outplug = getattr(nodetype, attrname)
        outhandle = datablock.outputValue(outplug)
        attr_descriptors[attrname].setvalue(outhandle, outval)
        datablock.setClean(plug)

    typedict = {'compute': compute,
                'transformerdata': transformerdata,
                'attr_descriptors': attr_descriptors}
    typedict.update(node_methods)

    nodetype = type(name, nodespec.nodebase(), typedict)
    mtypeid = OpenMaya.MTypeId(typeid)
    def creator():
        return OpenMayaMPx.asMPxPtr(nodetype())
    def init():
        for makeattr in attrmakers:
            makeattr(nodetype)
    def register(plugin):
        nodespec.register(plugin, name, mtypeid, creator, init)
    def deregister(plugin):
        nodespec.deregister(plugin, mtypeid)
    return register, deregister
