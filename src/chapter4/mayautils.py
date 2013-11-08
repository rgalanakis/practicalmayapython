import contextlib
import maya.cmds as cmds
import pymel.core as pmc


@contextlib.contextmanager
def undo_chunk():
    try:
        pmc.undoInfo(openChunk=True)
        yield
    finally:
        pmc.undoInfo(closeChunk=True)


@contextlib.contextmanager
def undo_on_error():
    pmc.undoInfo(openChunk=True)
    try:
        yield
        pmc.undoInfo(closeChunk=True)
    except:
        pmc.undoInfo(closeChunk=True)
        pmc.undo()
        raise


@contextlib.contextmanager
def set_file_prompt(state):
    oldstate = cmds.file(q=True, prompt=True)
    try:
        cmds.file(prompt=state)
        yield
    finally:
        cmds.file(prompt=oldstate)


@contextlib.contextmanager
def at_time(t):
    oldt = pmc.getCurrentTime()
    try:
        pmc.setCurrentTime(t)
        yield
    finally:
        pmc.setCurrentTime(oldt)


@contextlib.contextmanager
def with_unit(*args, **kwargs):
    oldlin = pmc.currentUnit(q=True, linear=True)
    oldang = pmc.currentUnit(q=True, angle=True)
    oldtim = pmc.currentUnit(q=True, time=True)
    try:
        pmc.currentUnit(*args, **kwargs)
    finally:
        pmc.currentUnit(linear=oldlin)
        pmc.currentUnit(angle=oldang)
        pmc.currentUnit(time=oldtim)


@contextlib.contextmanager
def render_layer_active(render_layer):
    orig_layer = pmc.nodetypes.RenderLayer.currentLayer()
    try:
        render_layer.setCurrent()
    finally:
        orig_layer.setCurrent()


# Version 1

@contextlib.contextmanager
def set_namespace_active(ns):
    old = pmc.namespaceInfo(currentNamespace=True,
                            absoluteName=True)
    try:
        pmc.namespace(setNamespace=ns)
        yield
    finally:
        pmc.namespace(setNamespace=old)


# Version 2

@contextlib.contextmanager
def set_namespace_active(ns):
    if ns == '':
        # This would be too ambiguous, so prohibit it
        raise ValueError('argument cannot be an empty string')
    old = pmc.namespaceInfo(currentNamespace=True,
                            absoluteName=True)
    try:
        pmc.namespace(setNamespace=ns)
        yield
    finally:
        pmc.namespace(setNamespace=old)


@contextlib.contextmanager
def denormalized_skin(skincluster):
    """Turns of skin cluster normalization and maintaining
    max influrnces."""
    max_infl = skincluster.maintainMaxInfluences.get()
    norm = skincluster.setNormalizeWeights(q=True)
    try:
        skincluster.maintainMaxInfluences.set(False)
        skincluster.setNormalizeWeights(0)
        yield
    finally:
        skincluster.maintainMaxInfluences.set(max_infl)
        skincluster.setNormalizeWeights(norm)


def swap_influence(skin_cluster, vert_ind, infl_a, infl_b):
    """For a given vertex,
    swaps the weight between two influences."""
    valA = pmc.skinPercent(skin_cluster, vert_ind, q=True, t=infl_a)
    valB = pmc.skinPercent(skin_cluster, vert_ind, q=True, t=infl_b)
    with denormalized_skin(skin_cluster):
        pmc.skinPercent(skin_cluster, vert_ind, tv=[infl_a, valB])
        pmc.skinPercent(skin_cluster, vert_ind, tv=[infl_b, valA])


mySkin = pmc.skinCluster()
swap_influence(mySkin, 100, 'right_thigh', 'left_thigh')

_denormalized_skins = set()


@contextlib.contextmanager
def denormalized_skin(skinCl):
    """Turns of skin cluster normalization and maintaining
    max influences."""
    if skinCl in _denormalized_skins:
        yield
    else:
        _denormalized_skins.add(skinCl)
        maxInfl = skinCl.maintainMaxInfluences.get()
        norm = skinCl.setNormalizeWeights(q=True)
        try:
            skinCl.maintainMaxInfluences.set(False)
            skinCl.setNormalizeWeights(0)
            yield
        finally:
            skinCl.maintainMaxInfluences.set(maxInfl)
            skinCl.setNormalizeWeights(norm)
            _denormalized_skins.remove(skinCl)


def cached_contextmanager(ctxmgr):
    cache = set()

    @contextlib.contextmanager
    def inner(*args):
        if args in cache:
            yield
        else:
            cache.add(args)
            try:
                yield ctxmgr(*args)
            finally:
                cache.remove(args)

    return inner


@cached_contextmanager
def denormalized_skin(skinCl):
    """Turns of skin cluster normalization and maintaining
    max influences."""
    maxInfl = skinCl.maintainMaxInfluences.get()
    norm = skinCl.setNormalizeWeights(q=True)
    try:
        skinCl.maintainMaxInfluences.set(False)
        skinCl.setNormalizeWeights(0)
        yield
    finally:
        skinCl.maintainMaxInfluences.set(maxInfl)
        skinCl.setNormalizeWeights(norm)


def cached_contextmanager(ctxmgr):
    cache = {}

    @contextlib.contextmanager
    def inner(*args):
        if args in cache:
            yield cache[args]
        else:
            cache[args] = None
            try:
                value = ctxmgr(*args)
                cache[args] = value
                yield value
            finally:
                del cache[args]

    return inner


@contextlib.contextmanager
def simplecache(func):
    def inner(*args, **kwargs):
        if not hasattr(inner, '_cache'):
            inner._cache = func(*args, **kwargs)
        return inner._cache

    return inner


def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


@simplecache
def factorial_1000():
    return factorial(1000)


import profiling

@profiling.record_duration
def export_scene():
    pass


def deco(key):
    def _deco(func):
        def inner(*args, **kwargs):
            print 'Invoking:', key
            return func(*args, **kwargs)
        return inner
    return _deco


class deco(object):
    def __init__(self, key):
        self.key = key

    def __call__(self, func):
        def inner(*args, **kwargs):
            print 'Invoking', self.key
            return func(*args, **kwargs)
        return inner


@deco('foo')
def spam():
    pass
