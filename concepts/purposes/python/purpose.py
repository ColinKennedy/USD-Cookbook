#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create a series of Prims with different "purpose" Properties defined."""

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Usd, UsdGeom


def main():
    """Run the main execution of the current script."""
    stage = Usd.Stage.CreateInMemory()
    xform = UsdGeom.Xform(stage.DefinePrim("/Xform", "Xform"))

    cube = UsdGeom.Cube(stage.DefinePrim("/Xform/SomeGuide", "Cube"))
    purpose = cube.CreatePurposeAttr()
    purpose.Set(UsdGeom.Tokens.guide)

    sphere = UsdGeom.Sphere(stage.DefinePrim("/Xform/SomeRender", "Sphere"))
    purpose = sphere.CreatePurposeAttr()
    purpose.Set(UsdGeom.Tokens.render)

    cone = UsdGeom.Cone(stage.DefinePrim("/Xform/SomeProxy", "Cone"))
    purpose = cone.CreatePurposeAttr()
    purpose.Set(UsdGeom.Tokens.proxy)

    cylinder = UsdGeom.Cylinder(stage.DefinePrim("/Xform/SomeDefault", "Cylinder"))
    purpose = cylinder.CreatePurposeAttr()
    purpose.Set(UsdGeom.Tokens.default_)

    print(stage.GetRootLayer().ExportToString())


if __name__ == "__main__":
    main()
