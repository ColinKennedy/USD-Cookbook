#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import tempfile

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Usd, UsdGeom


def create_cube_base_stage(stage):
    def _create_cube_payload():
        path = tempfile.NamedTemporaryFile(suffix=".usda").name
        stage = Usd.Stage.CreateNew(path)
        xform = UsdGeom.Cube(stage.DefinePrim("/PayloadCubeThing", "Cube"))
        cube = UsdGeom.Cube(stage.DefinePrim("/PayloadCubeThing/PayloadCube", "Cube"))
        stage.Save()

        return path

    payload = _create_cube_payload()
    xform = UsdGeom.Xform(stage.DefinePrim("/SomeXformCube", "Xform"))
    xform.GetPrim().GetPayloads().AddPayload(
        assetPath=payload, primPath="/PayloadCubeThing"
    )

    return xform


def create_sphere_base_stage(stage):
    def _create_sphere_payload():
        path = tempfile.NamedTemporaryFile(suffix=".usda").name
        stage = Usd.Stage.CreateNew(path)
        xform = UsdGeom.Sphere(stage.DefinePrim("/PayloadSphereThing", "Sphere"))
        sphere = UsdGeom.Sphere(
            stage.DefinePrim("/PayloadSphereThing/PayloadSphere", "Sphere")
        )
        stage.Save()

        return path

    payload = _create_sphere_payload()
    xform = UsdGeom.Xform(stage.DefinePrim("/SomeXformSphere", "Xform"))
    xform.GetPrim().GetPayloads().AddPayload(
        assetPath=payload, primPath="/PayloadSphereThing"
    )

    return xform


def main():
    """Run the main execution of the current script."""
    stage = Usd.Stage.CreateInMemory()
    cube = create_cube_base_stage(stage)
    sphere = create_sphere_base_stage(stage)
    xform = UsdGeom.Xform(stage.DefinePrim("/SomeTransform", "Xform"))
    xform.GetPrim().GetReferences().AddReference(
        assetPath="", primPath="/SomeXformCube"
    )
    xform.GetPrim().GetReferences().AddReference(
        assetPath="", primPath="/SomeXformSphere"
    )

    print(stage.GetRootLayer().ExportToString())


if __name__ == "__main__":
    main()
