#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import os

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Usd


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def main():
    '''Run the main execution of the current script.'''
    stage = Usd.Stage.Open(os.path.join(CURRENT_DIR, 'over.usda'))

    # XXX: Undefined prims are prims that don't resolve into a stage
    # Method 1: Search the opened stage Layer
    print(list(Usd.PrimRange.Stage(stage, ~Usd.PrimIsDefined)))

    # Method 2: Search all Layers in the stage, recursively (follows
    #           payloads and other composition arcs)
    #
    print(list(stage.Traverse(~Usd.PrimIsDefined)))


if __name__ == '__main__':
    main()
