#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Usd


def main():
    """Run the main execution of the current script."""
    stage = Usd.Stage.Open('override.usda')
    prim = stage.GetPrimAtPath('/AnotherPrim/InnerPrim1')
    print(prim.IsInstanceable(), prim.IsInstance())
    prim = stage.GetPrimAtPath('/MyPrim/SomeSphere')
    print(prim.IsInstanceable(), prim.IsInstance())


if __name__ == "__main__":
    main()
