#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A demonstration of how to add to variant sets at different levels of pipeline.

There is an asset that gets added to a "sequence" and then the sequence
is further further refined by a shot. This is shown by adding variant
sets at each step.

Important:
    All of the Stages here are created in-memory to avoid writing to
    disk. Because of that, we use identifiers to refer to those Stages.
    In production code, these identifiers should actually be paths to
    files or some kind of URI that USD can resolve into a consumable
    resource.

"""

# IMPORT STANDARD LIBRARIES
import os
import textwrap

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Usd, UsdGeom


def create_asset():
    """Create some asset to add into a sequence of shots."""
    stage = Usd.Stage.CreateInMemory()
    stage.GetRootLayer().documentation = (
        'This file contains the "character" that will be changed in other layers.'
    )

    sphere = UsdGeom.Sphere.Define(stage, "/SomeSphere")

    return stage


def create_sequence(asset):
    """Create a collection that shots will include and add some character to it."""
    stage = Usd.Stage.CreateInMemory()
    root = stage.GetRootLayer()
    root.documentation = "A common set of data for an entire sequence."
    root.subLayerPaths.append(asset)
    stage.SetMetadata(
        "comment",
        "We override the character to make it bigger and add some viewing option.",
    )
    prim = stage.OverridePrim("/SomeSphere")
    variants = prim.GetVariantSets().AddVariantSet("some_variant_set")
    variants.AddVariant("variant_name_1")

    variants.SetVariantSelection("variant_name_1")

    with variants.GetVariantEditContext():
        sphere = UsdGeom.Sphere(prim)
        sphere.GetDisplayColorAttr().Set([(1, 0, 0)])

    return stage


def create_shot(sequence):
    """Get the settings from some `sequence` and modify its assets."""
    stage = Usd.Stage.CreateInMemory()
    stage.GetRootLayer().subLayerPaths.append(sequence)
    prim = stage.OverridePrim("/SomeSphere")
    variants = prim.GetVariantSets().GetVariantSet("some_variant_set")
    variants.AddVariant("variant_name_2")

    prim.SetMetadata(
        "comment",
        textwrap.dedent(
            """\
        SetVariantSelection sets the default variant.

        Also note that our new variant set, "variant_name_2" adds, not
        overrides, the "some_variant_set". So we have "variant_name_2"
        and "variant_name_1" now.

        """
        ),
    )
    variants.SetVariantSelection("variant_name_2")
    with variants.GetVariantEditContext():
        sphere = UsdGeom.Sphere(prim)
        sphere.GetDisplayColorAttr().Set([(0, 1, 0)])

    stage.Save()
    return stage


def main():
    """Run the main execution of the current script."""
    sphere_stage = create_asset()
    sequence_stage = create_sequence(sphere_stage.GetRootLayer().identifier)
    shot_stage = create_shot(sequence_stage.GetRootLayer().identifier)

    print(sphere_stage.GetRootLayer().ExportToString())
    print(sequence_stage.GetRootLayer().ExportToString())
    print(shot_stage.GetRootLayer().ExportToString())


if __name__ == "__main__":
    main()
