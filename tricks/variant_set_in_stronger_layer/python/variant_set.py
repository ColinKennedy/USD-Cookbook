#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A module that shows how to author Variant Sets from stronger USD Layers.

Important:
    All of the Stages here are created in-memory to avoid writing to
    disk. Because of that, we use identifiers to refer to those Stages.
    In production code, these identifiers should actually be paths to
    files or some kind of URI that USD can resolve into a consumable
    resource.

"""

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Usd, UsdGeom


def create_basic_stage():
    stage = Usd.Stage.CreateInMemory()
    sphere = UsdGeom.Sphere.Define(stage, "/SomeSphere")

    stage.GetRootLayer().documentation = "A layer that authors some variant set"

    variants = sphere.GetPrim().GetVariantSets().AddVariantSet("some_variant_set")
    variants.AddVariant("variant_name_1")
    variants.AddVariant("variant_name_2")
    variants.AddVariant("variant_name_3")

    variants.SetVariantSelection("variant_name_1")
    with variants.GetVariantEditContext():
        sphere.GetRadiusAttr().Set(1)

    variants.SetVariantSelection("variant_name_2")
    with variants.GetVariantEditContext():
        sphere.GetRadiusAttr().Set(2)

    variants.SetVariantSelection("variant_name_3")
    with variants.GetVariantEditContext():
        sphere.GetRadiusAttr().Set(3)

    return stage


def create_override_stage(identifier):
    stage = Usd.Stage.CreateInMemory()
    stage.GetPrimAtPath("/SomeSphere")
    root = stage.GetRootLayer()
    root.subLayerPaths.append(identifier)
    sphere = UsdGeom.Sphere(stage.GetPrimAtPath("/SomeSphere"))

    # Here's an example of adding a completely new variant set
    sphere.GetPrim().GetVariantSets().AddVariantSet("another")

    variants = sphere.GetPrim().GetVariantSets().GetVariantSet("some_variant_set")
    variants.AddVariant("foo")

    variants.SetVariantSelection("foo")
    with variants.GetVariantEditContext():
        sphere.GetRadiusAttr().Set(100)

    return stage


def main():
    basic_stage = create_basic_stage()
    stage = create_override_stage(basic_stage.GetRootLayer().identifier)
    print(stage.GetRootLayer().ExportToString())


if __name__ == "__main__":
    main()
