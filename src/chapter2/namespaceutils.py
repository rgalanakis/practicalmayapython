import contextlib  # Helps make context managers
import pymel.core as pmc

@contextlib.contextmanager
def as_current(ns):
    old = pmc.namespaceInfo(currentNamespace=True)
    pmc.namespace(ns, set=True)
    try:
        yield
    finally:
        pmc.namespace(old, set=True)

