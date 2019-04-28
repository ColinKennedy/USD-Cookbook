#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Usd
from pxr import UsdGeom


def main():
    '''Run the main execution of the current script.'''
    stage = Usd.Stage.CreateInMemory()

    sphere = UsdGeom.Sphere(stage.DefinePrim("/SomeSphere", "Sphere"))
    sphere.GetPrim().SetMetadata('comment', 'I am a comment')

    print(stage.GetRootLayer().ExportToString())


if __name__ == '__main__':
    main()
