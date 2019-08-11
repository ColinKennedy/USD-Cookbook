#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module demonstrates the deprecated way to query material bindings.

In short, don't use this. Check out `material_binding_api.py` for an
updated way to search for bound materials.

"""

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Usd, UsdShade


def main():
    """Run the main execution of the current script."""
    stage = Usd.Stage.Open("../usda/materials.usda")

    # XXX : It looks as though the `GetBindingRel` and
    # `GetBoundMaterial` work but only for the `material:binding`
    # Relationship.
    #
    prim = stage.GetPrimAtPath("/Bob/Geom/Belt")
    print('Found Prim "{}".'.format(UsdShade.Material.GetBoundMaterial(prim).GetPrim()))
    print('Found Relationship "{}".'.format(UsdShade.Material.GetBindingRel(prim)))

    # XXX : If you attempt to use them on a Prim with a material
    # Property with different syntax, like `material:binding:full`,
    # it'll just return back invalid Prim / Relationship information.
    #
    prim = stage.GetPrimAtPath("/Bob/Geom/Body")
    print('Found Prim "{}".'.format(UsdShade.Material.GetBoundMaterial(prim).GetPrim()))
    print('Found Relationship "{}".'.format(UsdShade.Material.GetBindingRel(prim)))


if __name__ == "__main__":
    main()
