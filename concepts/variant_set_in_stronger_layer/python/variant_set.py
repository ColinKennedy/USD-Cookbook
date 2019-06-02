#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import tempfile

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Usd, UsdGeom


def create_basic_stage(path):
    stage = Usd.Stage.CreateNew(path)
    sphere = UsdGeom.Sphere(stage.DefinePrim("/SomeSphere", "Sphere"))

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

    stage.Save()


def create_override_stage(path):
    stage = Usd.Stage.CreateInMemory()
    stage.GetPrimAtPath("/SomeSphere")
    root = stage.GetRootLayer()
    root.subLayerPaths.append(path)
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
    with tempfile.NamedTemporaryFile(delete=False, suffix=".usda") as handle:
        create_basic_stage(handle.name)
        stage = create_override_stage(handle.name)
        print(stage.GetRootLayer().ExportToString())


if __name__ == "__main__":
    main()
