#!/usr/bin/env python
#

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Usd, UsdShade


def main():
    """Run the main execution of the current script."""
    stage = Usd.Stage.Open("./materials.usda")

    # XXX : It looks as though the `GetBindingRel` and `GetBoundMaterial` work but
    #       only for the `material:binding` Relationship.
    #
    # If you attempt to use them on a Prim that uses a slightly
    # different syntax, like `material:binding:full`, it'll contain
    # missing information.
    #
    prim = stage.GetPrimAtPath("/Bob/Geom/Belt")
    print('Found Prim "{}".'.format(UsdShade.Material.GetBoundMaterial(prim).GetPrim()))
    print('Found Relationship "{}".'.format(UsdShade.Material.GetBindingRel(prim)))

    prim = stage.GetPrimAtPath("/Bob/Geom/Body")
    print('Found Prim "{}".'.format(UsdShade.Material.GetBoundMaterial(prim).GetPrim()))
    print('Found Relationship "{}".'.format(UsdShade.Material.GetBindingRel(prim)))


    import sys
    sys.path.append('/home/selecaoone/env/config/rez_packages/utils/python')
    from inspection import dirgrep
    dirgrep(UsdShade.MaterialBindingAPI, '', sort=True)


if __name__ == "__main__":
    main()
