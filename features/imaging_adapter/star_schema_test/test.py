#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pxr import Usd
from pxr import UsdGeom
from star import Star


def main():
    """Run the main execution of the current script."""
    stage = Usd.Stage.CreateInMemory()
    Star.Star.Define(stage, "/star")

    # XXX : This should print ...
    # #usda 1.0

    # def Star "star"
    # {
    # }
    #
    print(stage.GetRootLayer().ExportToString())


if __name__ == "__main__":
    main()
