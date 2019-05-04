#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import os
import operator
import collections

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Sdf
from pxr import Usd


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def collect_all_traverse_data(layer, key=None):
    def _key(primspec):
        return primspec

    if not key:
        key = _key

    specifiers = collections.defaultdict(set)

    # Collect the layer's information
    for specifier, primspecs in collect_traverse_data(layer).iteritems():
        specifiers[specifier].update([key(primspec) for primspec in primspecs])

    # Collect every layer that this layer uses
    for path in layer.subLayerPaths:
        sublayer = Sdf.Layer.FindOrOpen(path)
        for specifier, primspecs in collect_all_traverse_data(sublayer).iteritems():
            specifiers[specifier].update([key(primspec) for primspec in primspecs])

    return specifiers


def collect_traverse_data(layer):
    specifiers = collections.defaultdict(set)
    for primspec in traverse(layer, allow=Sdf.PrimSpec):
        if isinstance(primspec, Sdf.PrimSpec):
            specifiers[primspec.specifier].add(primspec)

    return dict(specifiers)


def traverse(layer, allow=(Sdf.Layer, Sdf.PrimSpec)):
    def _traverse(layer):
        if isinstance(layer, Sdf.Layer):
            for primspec in layer.rootPrims.values():
                for subprim in traverse(primspec):
                    yield subprim
        elif isinstance(layer, Sdf.PrimSpec):
            for child in layer.nameChildren:
                for grandchild in traverse(child):
                    yield grandchild

        yield layer

    for item in _traverse(layer):
        if isinstance(item, allow):
            yield item


def main():
    '''Run the main execution of the current script.'''
    layer = Sdf.Layer.FindOrOpen(os.path.join(CURRENT_DIR, 'over.usda'))
    data = collect_all_traverse_data(layer, key=operator.attrgetter('path'))
    orphaned_overs = data.get(Sdf.SpecifierOver, set()) - data.get(Sdf.SpecifierDef, set())
    print('These overs do not refer to any concrete USD def', orphaned_overs)


if __name__ == '__main__':
    main()
