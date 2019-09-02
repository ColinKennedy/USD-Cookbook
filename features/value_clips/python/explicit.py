#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Use the Value Clip API's explicit syntax to author Value Clips."""

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Sdf, Usd


def main():
    """Run the main execution of this module."""
    stage = Usd.Stage.CreateInMemory()
    stage.SetStartTimeCode(0)
    stage.SetEndTimeCode(12)

    prim = stage.DefinePrim("/Prim")
    model = Usd.ClipsAPI(prim)
    model.SetClipActive([(0, 0), (2, 1)])
    model.SetClipAssetPaths(
        [Sdf.AssetPath("./clip_1.usda"), Sdf.AssetPath("./clip_2.usda")]
    )
    model.SetClipPrimPath("/Clip")
    model.SetClipTimes([(0, 0), (1, 1), (2, 0), (3, 1)])
    model.SetClipManifestAssetPath("./clip_manifest.usda")

    prim.GetReferences().AddReference(assetPath="./ref.usda", primPath="/Ref")
    print(stage.GetRootLayer().ExportToString())


if __name__ == "__main__":
    main()
