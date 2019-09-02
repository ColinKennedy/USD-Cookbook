#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Sdf, Usd, UsdGeom


def main():
    stage = Usd.Stage.CreateInMemory()

    # Method A: Set using methods
    some_sphere = UsdGeom.Sphere.Define(stage, "/SomeSphere")
    model = Usd.ModelAPI(some_sphere.GetPrim())
    model.SetAssetName("some_asset")
    model.SetAssetVersion("v1")
    model.SetAssetIdentifier("some/path/to/file.usda")
    model.SetPayloadAssetDependencies(
        Sdf.AssetPathArray(
            [Sdf.AssetPath("something.usd"), Sdf.AssetPath("another/thing.usd")]
        )
    )

    # Method B: Set-by-key
    another_sphere = UsdGeom.Sphere.Define(stage, "/AnotherSphere")
    another_prim = another_sphere.GetPrim()
    another_prim.SetAssetInfoByKey("version", "v1")
    another_prim.SetAssetInfoByKey("name", "some_asset")
    another_prim.SetAssetInfoByKey("identifier", "some/path/to/file.usda")
    another_prim.SetAssetInfoByKey(
        "payloadAssetDependencies",
        Sdf.AssetPathArray(
            [Sdf.AssetPath("something.usd"), Sdf.AssetPath("another/thing.usd")]
        ),
    )

    # Method C: Set-by-dict
    last_sphere = UsdGeom.Sphere.Define(stage, "/LastSphere")
    last_sphere.GetPrim().SetAssetInfo(
        {
            "identifier": "some/path/to/file.usda",
            "name": "some_asset",
            "version": "v1",
            "payloadAssetDependencies": Sdf.AssetPathArray(
                [Sdf.AssetPath("something.usd"), Sdf.AssetPath("another/thing.usd")]
            ),
        }
    )

    print(stage.GetRootLayer().ExportToString())


if __name__ == "__main__":
    main()
