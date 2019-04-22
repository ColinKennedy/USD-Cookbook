#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import tempfile

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Usd
from pxr import UsdGeom


def create_basic_scene(path):
    stage = Usd.Stage.CreateNew(path)
    sphere = UsdGeom.Sphere(stage.DefinePrim('/SomeSphere', 'Sphere'))

    sets = sphere.GetPrim().GetVariantSets().AddVariantSet('some_variant_set')
    sets.AddVariant('name_1')
    sets.AddVariant('name_2')
    sets.AddVariant('name_3')

    sets.SetVariantSelection('name_1')
    with sets.GetVariantEditContext():
        sphere.GetRadiusAttr().Set(1)

    sets.SetVariantSelection('name_2')
    with sets.GetVariantEditContext():
        sphere.GetRadiusAttr().Set(2)

    sets.SetVariantSelection('name_3')
    with sets.GetVariantEditContext():
        sphere.GetRadiusAttr().Set(3)

    stage.Save()


def create_override_stage(path):
    stage = Usd.Stage.Open(path)
    stage.GetPrimAtPath('/SomeSphere')
    sphere = UsdGeom.Sphere(stage.GetPrimAtPath('/SomeSphere'))
    sphere.GetPrim().GetVariantSets().AddVariantSet('another')

    return stage


def main():
    with tempfile.NamedTemporaryFile(suffix='.usda') as handle:
        create_basic_scene(handle.name)
        stage = create_override_stage(handle.name)
        print(stage.GetRootLayer().ExportToString())


if __name__ == '__main__':
    main()
