#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Gf, Kind, Usd, UsdGeom


def main():
    """Run the main execution of the current script."""
    stage = Usd.Stage.CreateInMemory()
    stage.GetRootLayer().documentation = (
        "This is an example of setting a Model Prim kind"
    )

    sphere1 = UsdGeom.Sphere.Define(stage, "/SomeSphere")
    Usd.ModelAPI(sphere1).SetKind(Kind.Tokens.component)
    sphere2 = UsdGeom.Sphere.Define(stage, "/SomeSphere/SphereChild")
    Usd.ModelAPI(sphere2).SetKind(Kind.Tokens.subcomponent)
    sphere3 = UsdGeom.Sphere.Define(stage, "/SomeSphere/Foo")
    Usd.ModelAPI(sphere3).SetKind("does_not_exist")
    sphere3.GetPrim().SetMetadata(
        "comment",
        "XXX: This kind is made up. But it could be real if we added to the KindRegistry\n"
        "https://graphics.pixar.com/usd/docs/api/class_kind_registry.html",
    )

    print(stage.GetRootLayer().ExportToString())


if __name__ == "__main__":
    main()
