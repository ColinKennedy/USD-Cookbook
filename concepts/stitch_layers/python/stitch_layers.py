#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Stitch one Sdf Layer onto another Sdf Layer, using UsdUtils."""

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Sdf, UsdUtils


def main():
    """Run the main execution of the current script."""
    weak_layer = Sdf.Layer.CreateAnonymous()
    weak_root = weak_layer.pseudoRoot
    weak_prim = Sdf.PrimSpec(weak_root, "SomePrim", Sdf.SpecifierClass)
    some_attribute = Sdf.AttributeSpec(
        weak_prim, "some_attribute", Sdf.ValueTypeNames.Bool
    )
    weak_layer.SetTimeSample(some_attribute.path, 0, True)
    weak_layer.SetTimeSample(some_attribute.path, 2, False)
    weak_layer.startTimeCode = 4
    weak_layer.endTimeCode = 10

    strong_layer = Sdf.Layer.CreateAnonymous()
    strong_root = strong_layer.pseudoRoot
    strong_prim = Sdf.PrimSpec(strong_root, "SomePrim", Sdf.SpecifierOver)
    some_attribute = Sdf.AttributeSpec(
        strong_prim, "some_attribute", Sdf.ValueTypeNames.Bool
    )
    strong_layer.SetTimeSample(some_attribute.path, 0, False)
    strong_layer.SetTimeSample(some_attribute.path, 1, True)
    strong_layer.startTimeCode = 8
    strong_layer.endTimeCode = 20

    # XXX : Stitching has different rules, depending on what is being stitched.
    #
    # - time samples use the minimum and maximum values of both layers
    # - dict keys in the strong layer are always preferred and missing
    # keys fall back to the weaker layer
    # - Same with time samples
    #
    # - Interestingly though, the specifier for the PrimSpec does weird things
    # e.g.
    # Scenario 1:
    #  `weak_layer` = Over
    #  `strong_layer` = Def
    #  Result: Def (strong_layer was preferred)
    #
    # Scenario 2:
    #  `weak_layer` = Def
    #  `strong_layer` = Over
    #  Result: Def (weak_layer was preferred)
    #
    # Scenario 3:
    #  `weak_layer` = Class
    #  `strong_layer` = Over
    #  Result: Class (weak_layer was preferred)
    #
    # Scenario 4:
    #  `weak_layer` = Class
    #  `strong_layer` = Def
    #  Result: Def (strong_layer was preferred)
    #
    # Most likely, specifiers have a strength order that StitchLayers
    # is using to merge it. It probably doesn't matter which layer is
    # strong or weak.
    #
    UsdUtils.StitchLayers(strong_layer, weak_layer)
    print(strong_layer.ExportToString())


if __name__ == "__main__":
    main()
