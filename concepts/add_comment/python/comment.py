#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Show how to write a comment in USD Python API."""

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Usd, UsdGeom


def main():
    """Run the main execution of the current script."""
    stage = Usd.Stage.CreateInMemory()

    sphere = UsdGeom.Sphere(stage.DefinePrim("/SomeSphere", "Sphere"))
    sphere.GetPrim().SetMetadata("comment", "I am a comment")

    print(stage.GetRootLayer().ExportToString())


if __name__ == "__main__":
    main()
