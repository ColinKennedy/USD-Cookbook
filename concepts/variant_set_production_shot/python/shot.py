#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A demonstration of how to add to variant sets at different levels of pipeline.

There is an asset that gets added to a "sequence" and then the sequence
is further further refined by a shot. This is shown by adding variant
sets at each step.

"""

# IMPORT STANDARD LIBRARIES
import os
import tempfile
import textwrap

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Usd, UsdGeom


def create_asset():
    """Create some asset to add into a sequence of shots."""
    path = tempfile.NamedTemporaryFile(suffix=".usda").name
    stage = Usd.Stage.CreateNew(path)
    stage.GetRootLayer().documentation = (
        'This file contains the "character" that will be changed in other layers.'
    )

    sphere = UsdGeom.Sphere(stage.DefinePrim("/SomeSphere", "Sphere"))

    stage.Save()  # XXX: This is needed. Otherwise `create_sequence` will fail
    return path, stage


def create_sequence(asset):
    """Create a collection that shots will include and add some character to it."""
    path = tempfile.NamedTemporaryFile(suffix=".usda").name
    stage = Usd.Stage.CreateNew(path)
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

    # XXX: This is kind of random and cool BUT if you comment
    # out `stage.Save()` in `create_asset`, the `Set` function
    # below fail with a "Empty typeName" error. But if you add
    # `prim.SetTypeName('Sphere')` then it will work even without saving
    # the stage in `create_asset`. The consequence of doing this though
    # is that "over" will be forced to a specific type, which isn't that
    # flexible.
    #
    # Moral of the story is: Save your work!
    #
    with variants.GetVariantEditContext():
        sphere = UsdGeom.Sphere(prim)
        sphere.GetDisplayColorAttr().Set([(1, 0, 0)])

    stage.Save()
    return path, stage


def create_shot(sequence):
    """Get the settings from some `sequence` and modify its assets."""
    path = tempfile.NamedTemporaryFile(suffix=".usda").name
    stage = Usd.Stage.CreateNew(path)
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
    return path, stage


def main():
    """Run the main execution of the current script."""
    sphere, sphere_stage = create_asset()
    sequence, sequence_stage = create_sequence(sphere)
    shot, shot_stage = create_shot(sequence)

    print(sphere_stage.GetRootLayer().ExportToString())
    print(sequence_stage.GetRootLayer().ExportToString())
    print(shot_stage.GetRootLayer().ExportToString())

    for path in [sphere, sequence, shot]:
        os.remove(path)


if __name__ == "__main__":
    main()
