#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Sdf, Usd


def main():
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
