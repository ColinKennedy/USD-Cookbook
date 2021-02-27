#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pxr import Sdf, Usd


def as_sdf():
    """Run the main execution of the current script."""
    layer = Sdf.Layer.CreateAnonymous()
    prim_spec = Sdf.CreatePrimInLayer(layer, "/root")
    prim_spec.specifier = Sdf.SpecifierDef
    attribute_spec = Sdf.AttributeSpec(prim_spec, "some_name", Sdf.ValueTypeNames.Int)
    attribute_spec.custom = True
    attribute_spec.default = 8

    layer.SetTimeSample(attribute_spec.path, 10.5, 9)

    print(layer.ExportToString())


def as_usd():
    stage = Usd.Stage.CreateInMemory()
    prim = stage.DefinePrim("/root")
    attribute = prim.CreateAttribute("some_name", Sdf.ValueTypeNames.Int)
    attribute.Set(8)

    layer = stage.GetEditTarget().GetLayer()  # By default, this is `stage.GetRootLayer`
    layer.SetTimeSample(attribute.GetPath(), 10.5, 9)

    print(layer.ExportToString())


if __name__ == "__main__":
    as_sdf()
    as_usd()
