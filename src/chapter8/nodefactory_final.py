from maya import OpenMaya, OpenMayaMPx

A_FLOAT = dict(
    attr=OpenMaya.MFnNumericAttribute,
    getvalue=lambda dh: dh.asFloat(),
    setvalue=lambda dh, v: dh.setFloat(v),
    create=lambda attrfn, ln, sn: attrfn.create(
        ln, sn, OpenMaya.MFnNumericData.kFloat),
    setdefault=lambda attrfn, d: attrfn.setDefault(d)
)

A_STRING = dict(
    attr=OpenMaya.MFnTypedAttribute,
    getvalue=lambda dh: dh.asString(),
    setvalue=lambda dh, v: dh.setString(v),
    create=lambda attrfn, ln, sn: attrfn.create(
        ln, sn, OpenMaya.MFnData.kString),
    setdefault=lambda attrfn, d: attrfn.setDefault(
        OpenMaya.MFnStringData().create(d))
)


A_ENUM = dict(
    attr=OpenMaya.MFnEnumAttribute,
    getvalue=lambda dh: dh.asInt(),
    setvalue=lambda dh, v: dh.setInt(v),
    create=lambda attrfn, ln, sn: attrfn.create(ln, sn),
    setdefault=lambda attrfn, d: attrfn.setDefault(d)
)

A_COLOR = dict(
    attr=OpenMaya.MFnNumericAttribute,
    getvalue=lambda dh: dh.asFloatVector(),
    setvalue=lambda dh, v: dh.setMFloatVector(OpenMaya.MFloatVector(*v)),
    create=lambda attrfn, ln, sn: attrfn.createColor(ln, sn),
    setdefault=lambda attrfn, d: attrfn.setDefault(*d)
)


NT_DEPENDSNODE = dict(
    nodetype=OpenMayaMPx.MPxNode.kDependNode,
    nodebase=(OpenMayaMPx.MPxNode,),
    register=lambda mp, *args: mp.registerNode(*args),
    deregister=lambda mp, tid: mp.deregisterNode(tid)
)

class TransformMatrix(OpenMayaMPx.MPxTransformationMatrix):
    pass

xformTypeID = OpenMaya.MTypeId(0x00000901)

def makeNodeMatrix():
    return OpenMayaMPx.asMPxPtr(TransformMatrix())

def _registerTransform(mp, typename, typeid, create, init, _):
    mp.registerTransform(
        typename, typeid, create, init,
        makeNodeMatrix, xformTypeID)

NT_TRANSFORMNODE = dict(
    nodetype=OpenMayaMPx.MPxNode.kTransformNode,
    nodebase=(OpenMayaMPx.MPxTransform,),
    register=_registerTransform,
    deregister=lambda mp, tid: mp.deregisterNode(tid)
)


def create_attrmaker(
    descr, ln, sn, affectors=(), default=None,
    transformer=None, fields=()):

    if descr is not A_ENUM and fields:
        raise RuntimeError('Only enum attrs can have fields.')

    def inner(nodetype):
        attr = descr['attr']()
        plug = descr['create'](attr, ln, sn)

        for name, value in fields:
            attr.addField(name, value)

        if default is not None:
            descr['setdefault'](attr, default)

        isoutput = bool(affectors)
        isinput = not isoutput
        attr.setWritable(isinput)
        attr.setStorable(isinput)
        if isoutput:
            assert transformer, 'Must specify transformer.'
            nodetype.transformerdata[ln] = (
                affectors, transformer)

        nodetype.attr_descriptors[ln] = descr

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


def create_node(descr, name, typeid, attrmakers, node_methods=None):
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
            inval = attr_descriptors[inname]['getvalue'](indata)
            invals.append(inval)
        outval = xformer(*invals)
        outplug = getattr(nodetype, attrname)
        outhandle = datablock.outputValue(outplug)
        attr_descriptors[attrname]['setvalue'](outhandle, outval)
        datablock.setClean(plug)

    typedict = {'compute': compute,
                'transformerdata': transformerdata,
                'attr_descriptors': attr_descriptors}
    typedict.update(node_methods)

    nodetype = type(name, descr['nodebase'], typedict)
    mtypeid = OpenMaya.MTypeId(typeid)
    def creator():
        return OpenMayaMPx.asMPxPtr(nodetype())
    def init():
        for makeattr in attrmakers:
            makeattr(nodetype)
    def register(plugin):
        descr['register'](plugin, name, mtypeid,
            creator, init, descr['nodetype'])
    def deregister(plugin):
        descr['deregister'](plugin, mtypeid)
    return register, deregister
