#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Usd, UsdGeom


def main():
    """Run the main execution of the current script."""
    stage = Usd.Stage.CreateInMemory()
    # from inspection import dirgrep; dirgrep(stage, 'prim', sort=True)
    sphere = UsdGeom.Sphere.Define(stage, "/thing/SomethingElse/NestedEvenMore")
    sphere.GetRadiusAttr().Set(4)

    prim = stage.DefinePrim("/thing/SomethingElse/SpecializedChild")
    prim.GetSpecializes().AddSpecialize(sphere.GetPath())

    print(stage.GetRootLayer().ExportToString())


if __name__ == "__main__":
    main()
