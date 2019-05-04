#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Gf
from pxr import Usd
from pxr import UsdGeom


def main():
    '''Run the main execution of the current script.'''
    stage = Usd.Stage.CreateInMemory()
    sphere = UsdGeom.Sphere(stage.DefinePrim('/SomeSphere', 'Sphere'))
    sphere.AddTranslateOp().Set(Gf.Vec3d(20, 30, 40))


    # Method #1: Compute at a certain time
    print(UsdGeom.Imageable(sphere).ComputeWorldBound(
        Usd.TimeCode(1),
        purpose1='default',
    ))

    # Method #2: Compute using a cache
    cache = UsdGeom.BBoxCache(Usd.TimeCode.Default(), ['default', 'render'])
    print(cache.ComputeWorldBound(sphere.GetPrim()))


if __name__ == '__main__':
    main()
