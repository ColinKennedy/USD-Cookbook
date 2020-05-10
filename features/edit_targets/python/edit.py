#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pxr import Usd, UsdGeom


def _make_target():
    stage = Usd.Stage.CreateInMemory()
    root = UsdGeom.Scope.Define(stage, "/root")
    UsdGeom.Sphere.Define(stage, root.GetPath().AppendChild("sphere"))
    stage.SetDefaultPrim(root.GetPrim())

    return stage


def main():
    """Run the main execution of the current script."""
    inner_stage = _make_target()
    main_stage = Usd.Stage.CreateInMemory()

    # XXX : In order to use `inner_stage` in an EditContext, it must be
    # in `main_stage`'s local LayerStack (e.g. it must be a sublayer)
    #
    main_stage.GetRootLayer().subLayerPaths.append(inner_stage.GetRootLayer().identifier)

    print(main_stage.GetRootLayer().ExportToString())
    print('Inner stage before context')
    print(inner_stage.GetRootLayer().ExportToString())

    with Usd.EditContext(main_stage, inner_stage.GetRootLayer()):
        sphere = UsdGeom.Sphere(main_stage.GetPrimAtPath("/root/sphere"))
        sphere.GetRadiusAttr().Set(10)

    print('Inner stage after context')
    print(inner_stage.GetRootLayer().ExportToString())

    main_stage.SetEditTarget(Usd.EditTarget(inner_stage.GetRootLayer()))
    sphere = UsdGeom.Sphere(main_stage.GetPrimAtPath("/root/sphere"))
    sphere.GetRadiusAttr().Set(5)

    print('Inner stage after setting')
    print(inner_stage.GetRootLayer().ExportToString())


if __name__ == "__main__":
    main()
