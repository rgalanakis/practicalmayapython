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
        return fnattr.create(longname, shortname,
                             OpenMaya.MFnData.kString)
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

class _TransformNode(NodeSpec):
    xform_typeid = OpenMaya.MTypeId(0x60080)
    class TransformMatrix(OpenMayaMPx.MPxTransformationMatrix):
        pass
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
    transformer=None, fields=()): #(1)

    if not attrspec.allow_fields() and fields: #(2)
        raise RuntimeError(
            'Fields not allowed for %s.' % attrspec)

    def createattr(nodeclass):
        fnattr = attrspec.createfnattr()
        attrobj = attrspec.create(fnattr, ln, sn)

        for name, value in fields: #(3)
            fnattr.addField(name, value)

        if default is not None:
            attrspec.setdefault(fnattr, default)

        isinput = not bool(affectors)
        fnattr.setWritable(isinput)
        fnattr.setStorable(isinput)
        if not isinput and transformer is None:
            raise RuntimeError('Must specify transformer.')

        nodeclass.addAttribute(attrobj)
        setattr(nodeclass, ln, attrobj)

        for affectedby in affectors:
            inputplug = getattr(nodeclass, affectedby)
            nodeclass.attributeAffects(inputplug, attrobj)
        return ln, attrspec, transformer, affectors
    return createattr


def float_input(ln, sn, **kwargs):
    return create_attrmaker(A_FLOAT, ln, sn, **kwargs)

def float_output(ln, sn, **kwargs):
    return create_attrmaker(A_FLOAT, ln, sn, **kwargs)


def create_node(nodespec, name, typeid, attrmakers):
    attr_to_spec = {} #(1)
    outattr_to_xformdata = {}
    def compute(mnode, plug, datablock):
        attrname = plug.name().split('.')[-1]
        xformdata = outattr_to_xformdata.get(attrname) #(2)
        if xformdata is None:
            return OpenMaya.MStatus.kUnknownParameter
        xformer, affectors = xformdata
        invals = []
        for inname in affectors: #(3)
            inplug = getattr(nodetype, inname)
            indata = datablock.inputValue(inplug)
            inval = attr_to_spec[inname].getvalue(indata)
            invals.append(inval)
        outval = xformer(*invals) #(4)
        outhandle = datablock.outputValue(plug) #(5)
        attr_to_spec[attrname].setvalue(outhandle, outval)
        datablock.setClean(plug)
    methods = {'compute': compute}
    nodetype = type(name, nodespec.nodebase(), methods)

    mtypeid = OpenMaya.MTypeId(typeid)
    def creator():
        return OpenMayaMPx.asMPxPtr(nodetype())
    def init():
        for makeattr in attrmakers: #(6)
            ln, attrspec, xformer, affectors = makeattr(nodetype)
            attr_to_spec[ln] = attrspec
            if xformer is not None:
                outattr_to_xformdata[ln] = xformer, affectors

    def register(plugin):
        nodespec.register(plugin, name, mtypeid, creator, init)
    def deregister(plugin):
        nodespec.deregister(plugin, mtypeid)
    return register, deregister
