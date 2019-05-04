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
    orphaned_overs = list(Usd.PrimRange.Stage(stage, ~Usd.PrimIsDefined))


if __name__ == '__main__':
    main()
