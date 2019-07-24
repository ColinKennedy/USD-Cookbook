#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A basic demonstration of how to traverse the instances of a USD stage."""

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Gf, Sdf, Usd


def create_basic_instance_stage():
    """A USD stage that has instanced Prims on it.

    Reference:
        https://graphics.pixar.com/usd/docs/api/_usd__page__scenegraph_instancing.html#Usd_ScenegraphInstancing_Querying

    Returns:
        `pxr.Usd.Stage`: The generated, in-memory object.

    """
    stage = Usd.Stage.CreateInMemory()

    car = stage.CreateClassPrim("/Car")
    car.CreateAttribute("color", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f([0, 0, 0]))
    body = stage.DefinePrim("/Car/Body")
    body.CreateAttribute("color", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f([0, 0, 0]))
    stage.DefinePrim("/Car/Door")

    paths = ("/ParkingLot/Car_1", "/ParkingLot/Car_2", "/ParkingLot/Car_n")

    for path in paths:
        prim = stage.DefinePrim(path)
        prim.SetInstanceable(True)
        prim.GetReferences().AddReference(assetPath="", primPath=car.GetPath())

    return stage


def traverse_instanced_children(prim):
    """Get every Prim child beneath `prim`, even if `prim` is instanced.

    Important:
        If `prim` is instanced, any child that this function yields will
        be an instance proxy.

    Args:
        prim (`pxr.Usd.Prim`): Some Prim to check for children.

    Yields:
        `pxr.Usd.Prim`: The children of `prim`.

    """
    for child in prim.GetFilteredChildren(Usd.TraverseInstanceProxies()):
        yield child

        for subchild in traverse_instanced_children(child):
            yield subchild


def main():
    """Run the main execution of the current script."""
    stage = create_basic_instance_stage()

    all_uninstanced_prims = list(stage.TraverseAll())
    all_prims_including_instanced_child_prims = sorted(
        traverse_instanced_children(stage.GetPseudoRoot())
    )

    print(
        'The instanced Prims list found "{number}" more Prims than TraverseAll.'.format(
            number=len(all_prims_including_instanced_child_prims)
            - len(all_uninstanced_prims)
        )
    )

    for prim in all_prims_including_instanced_child_prims:
        print(prim)


if __name__ == "__main__":
    main()
