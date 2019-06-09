#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create a series of Prims with different "purpose" Properties defined."""

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Usd, UsdGeom


def main():
    """Run the main execution of the current script."""
    stage = Usd.Stage.CreateInMemory()
    xform = UsdGeom.Xform.Define(stage, "/Xform")

    cube = UsdGeom.Cube.Define(stage, "/Xform/SomeGuide")
    purpose = cube.CreatePurposeAttr()
    purpose.Set(UsdGeom.Tokens.guide)

    sphere = UsdGeom.Sphere.Define(stage, "/Xform/SomeRender")
    purpose = sphere.CreatePurposeAttr()
    purpose.Set(UsdGeom.Tokens.render)

    cone = UsdGeom.Cone.Define(stage, "/Xform/SomeProxy")
    purpose = cone.CreatePurposeAttr()
    purpose.Set(UsdGeom.Tokens.proxy)

    cylinder = UsdGeom.Cylinder.Define(stage, "/Xform/SomeDefault")
    purpose = cylinder.CreatePurposeAttr()
    purpose.Set(UsdGeom.Tokens.default_)

    print(stage.GetRootLayer().ExportToString())


if __name__ == "__main__":
    main()
