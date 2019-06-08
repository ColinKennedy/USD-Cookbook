#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
# IMPORT STANDARD LIBRARIES
import time

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Sdf, Usd

ITERATIONS = 1000
PATHS = (
    {
        "BasePrim": {
            "InnerPrim": frozenset((
                "SiblingPrim",
            )),
        },
        "SomePrim": frozenset((
            "AnotherInnerPrim",
            "ChildPrim",
            "SiblingPrim",
        )),
    }
)


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
    create_prim_specs(layer.pseudoRoot, paths)
    parent = layer.GetPrimAtPath("SomePrim/AnotherInnerPrim")
    for index in range(ITERATIONS):
        Sdf.PrimSpec(parent, "IndexedPrim{}".format(index), Sdf.SpecifierDef)


@_timeit
def _prepare_prims_with_stage(stage):
    """Create Prims using a USD Stage."""
    for path in create_prims(PATHS):
        stage.DefinePrim(path)

    indexed_template = "/SomePrim/AnotherInnerPrim/IndexedPrim{}"
    for index in range(ITERATIONS):
        stage.DefinePrim(indexed_template.format(index))


def create_prim_specs(root, names):
    """Create the PrimSpecs for some Sdf Layer."""
    def _create_recursively(parent, names):
        if not isinstance(names, collections.MutableMapping):
            for name in names:
                Sdf.PrimSpec(parent, name, Sdf.SpecifierDef)

            return

        for base, inner_names in names.iteritems():
            base_prim_spec = Sdf.PrimSpec(parent, base, Sdf.SpecifierDef)
            _create_recursively(base_prim_spec, inner_names)

    _create_recursively(root, names)


def create_prims(names):
    """str: Write out the paths to each Prim that must be created."""
    def _create_recursively(names, parent=''):
        if not isinstance(names, collections.MutableMapping):
            for name in names:
                yield parent + '/' + name

            return
            yield

        for base, inner_names in names.iteritems():
            base_prim_spec = parent + '/' + base
            yield base_prim_spec

            for prim in _create_recursively(inner_names, parent=base_prim_spec, ):
                yield prim

    for prim in _create_recursively(names):
        yield prim


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
    _prepare_prims_with_stage(stage)

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
