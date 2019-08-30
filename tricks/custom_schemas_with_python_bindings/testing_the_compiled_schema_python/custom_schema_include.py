#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module is a copy of Pixar's "Generating Custom Schema Classes" tutorial.

Here, the custom schema classes are imported using the Python namespace
that was created (instead of importing from `pxr`).

Reference:
    https://graphics.pixar.com/usd/docs/Generating-New-Schema-Classes.html

"""

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Usd

# IMPORT FIRST-PARTY LIBRARIES
from testout import Testout


def main():
    """Run the main execution of the current script."""
    stage = Usd.Stage.Open("Test.usda")
    cp = stage.GetPrimAtPath("/Complex")
    simple = Testout.Simple(cp)
    target = simple.GetTargetRel()
    intAttr = simple.GetIntAttrAttr()
    complex = Testout.Complex(cp)
    print 'complexString: %s' % complex.GetComplexStringAttr().Get()
    obj = stage.GetPrimAtPath("/Object")
    paramsAPI = Testout.ParamsAPI.Apply(obj);
    # assert obj.HasAPI(Testout.ParamsAPI)
    print 'mass: %s' % paramsAPI.GetMassAttr().Get()
    print 'velocity: %s' % paramsAPI.GetVelocityAttr().Get()
    print 'volume: %s' % paramsAPI.GetVolumeAttr().Get()


if __name__ == "__main__":
    main()
