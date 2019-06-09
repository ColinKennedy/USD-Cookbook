#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module shows how to load 2+ Payloads on a single Prim.

The short answer is - add a Payload to 2+ Prims and then Reference
those Prims onto a single Prim. Then that container Prim with all the
references will get each Payload.

Also note: This module isn't going to run directly in usdview because
we're using anonymous layers. So see an actual example, look at the
nearby "usda" folder.

"""

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Usd, UsdGeom


def create_cube_base_stage(stage):
    def _create_cube_payload():
        stage = Usd.Stage.CreateInMemory()
        UsdGeom.Xform.Define(stage, "/PayloadCubeThing")
        UsdGeom.Cube.Define(stage, "/PayloadCubeThing/PayloadCube")

        return stage.GetRootLayer().identifier

    payload = _create_cube_payload()
    xform = UsdGeom.Xform.Define(stage, "/SomeXformCube")
    xform.GetPrim().GetPayloads().AddPayload(
        assetPath=payload, primPath="/PayloadCubeThing"
    )

    return xform


def create_sphere_base_stage(stage):
    def _create_sphere_payload():
        stage = Usd.Stage.CreateInMemory()
        UsdGeom.Xform.Define(stage, "/PayloadSphereThing")
        UsdGeom.Sphere.Define(stage, "/PayloadSphereThing/PayloadSphere")

        return stage.GetRootLayer().identifier

    payload = _create_sphere_payload()
    xform = UsdGeom.Xform.Define(stage, "/SomeXformSphere")
    xform.GetPrim().GetPayloads().AddPayload(
        assetPath=payload, primPath="/PayloadSphereThing"
    )

    return xform


def main():
    """Run the main execution of the current script."""
    stage = Usd.Stage.CreateInMemory()
    cube = create_cube_base_stage(stage)
    sphere = create_sphere_base_stage(stage)
    xform = UsdGeom.Xform.Define(stage, "/SomeTransform")
    xform.GetPrim().GetReferences().AddReference(
        assetPath="", primPath="/SomeXformCube"
    )
    xform.GetPrim().GetReferences().AddReference(
        assetPath="", primPath="/SomeXformSphere"
    )

    print(stage.GetRootLayer().ExportToString())


if __name__ == "__main__":
    main()
