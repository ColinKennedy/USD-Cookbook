#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import collections
import time

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Sdf, Usd

ITERATIONS = 1000
PATHS = frozenset((
    "/BasePrim",
    "/BasePrim/InnerPrim",
    "/BasePrim/InnerPrim/SiblingPrim",
    "/SomePrim",
    "/SomePrim/AnotherInnerPrim",
    "/SomePrim/ChildPrim",
    "/SomePrim/SiblingPrim"
))


# Reference: https://medium.com/pythonhive/python-decorator-to-measure-the-execution-time-of-methods-fa04cb6bb36d
def _timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print '%r  %2.2f ms' % \
                  (method.__name__, (te - ts) * 1000)
        return result
    return timed


@_timeit
def _prepare_prim_specs_with_sdf(layer, paths):
    """Create PrimSpecs using a Sdf Layer."""
    for path in paths:
        prim_spec = Sdf.CreatePrimInLayer(layer, path)
        prim_spec.specifier = Sdf.SpecifierDef

    parent = layer.GetPrimAtPath("SomePrim/AnotherInnerPrim")
    for index in range(ITERATIONS):
        Sdf.PrimSpec(parent, "IndexedPrim{}".format(index), Sdf.SpecifierDef)


@_timeit
def _prepare_prims_with_stage(stage, paths):
    """Create Prims using a USD Stage."""
    for path in paths:
        stage.DefinePrim(path)

    indexed_template = "/SomePrim/AnotherInnerPrim/IndexedPrim{}"
    for index in range(ITERATIONS):
        stage.DefinePrim(indexed_template.format(index))


def create_using_sdf():
    """Run the main execution of the current script."""
    layer = Sdf.Layer.CreateAnonymous()

    # TODO : Adding / Removing this ChangeBlock doesn't change the time
    # much. Is a change block only useful when authoring opinions?
    #
    with Sdf.ChangeBlock():
       _prepare_prim_specs_with_sdf(layer, PATHS)

    return layer.ExportToString()


def create_using_stage():
    """str: Create Prims using a USD stage."""
    stage = Usd.Stage.CreateInMemory()
    _prepare_prims_with_stage(stage, PATHS)

    return stage.GetRootLayer().ExportToString()


def main():
    stage_export = create_using_stage()
    layer_export = create_using_sdf()

    # The first line of a USD export is a metadata line so we remove it
    # here just so we can compare if the output really is the same.
    #
    stage_export = stage_export.splitlines()[1:]
    layer_export = layer_export.splitlines()[1:]

    print('These exports should be exactly the same', stage_export == layer_export)


if __name__ == "__main__":
    main()
