#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Batch-creating PrimSpecs, using SdfChangeBlock."""

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Sdf, UsdGeom


def main():
    """Run the main execution of the current script."""
    layer = Sdf.Layer.CreateAnonymous()

    paths = {
        Sdf.Path("/AndMore"),
        Sdf.Path("/AnotherOne"),
        Sdf.Path("/AnotherOne/AndAnother"),
        Sdf.Path("/More"),
        Sdf.Path("/OkayNoMore"),
        Sdf.Path("/SomeSphere"),
        Sdf.Path("/SomeSphere/InnerPrim"),
        Sdf.Path("/SomeSphere/InnerPrim/LastOne"),
    }

    prefixes = set(prefix for path in paths for prefix in path.GetPrefixes())
    with Sdf.ChangeBlock():
        for path in prefixes:
            prim_spec = Sdf.CreatePrimInLayer(layer, path)
            prim_spec.specifier = Sdf.SpecifierDef
            prim_spec.typeName = UsdGeom.Xform.__name__

    print(layer.ExportToString())


if __name__ == "__main__":
    main()
