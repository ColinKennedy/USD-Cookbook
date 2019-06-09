#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module describes how to merge anonymous layers with unsaved edits into a stage."""

# IMPORT STANDARD LIBRARIES
import functools

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Sdf, Usd, UsdGeom, UsdUtils


def _remove_anonymous_asset_paths(layer, path, identifiers):
    """Remove any anonymous identifier that is/will be merged into a USD stage."""
    if path in identifiers:
        # If `path` is one of the anonymous layers, setting to an empty
        # string will force USD to treat the Asset Path as if it were
        # pointing to a namespace located in the current USD layer.
        #
        return ""

    return path


def main():
    """Run the main execution of the current script."""
    # Initialize the stage and layers
    stage = Usd.Stage.CreateInMemory()
    UsdGeom.Xform.Define(stage, "/SomeTransform")
    UsdGeom.Sphere.Define(stage, "/SomeTransform/SomeSphere")
    anonymous1 = Usd.Stage.CreateInMemory()
    anonymous1.DefinePrim("/SomeItemInAnonymous")
    anonymous2 = Usd.Stage.CreateInMemory()
    anonymous2.DefinePrim("/SomethingElseThatIsInAnotherLayer")

    # Add some composition arcs that target the anonymous layers
    prim = stage.GetPrimAtPath("/SomeTransform/SomeSphere")
    prim.GetReferences().AddReference(
        anonymous1.GetRootLayer().identifier, primPath="/SomeItemInAnonymous"
    )
    prim.GetReferences().AddReference(
        anonymous2.GetRootLayer().identifier,
        primPath="/SomethingElseThatIsInAnotherLayer",
    )

    # XXX : Here we are using `FlattenLayerStack` to replace the
    # authored, anonymous assetPath arguments with nothing because we
    # are about to merge the anonymous layer(s) into the stage anyway,
    # so the paths will just refer to the current USD stage.
    #
    roots = set((layer.GetRootLayer() for layer in (anonymous1, anonymous2)))
    layer = UsdUtils.FlattenLayerStack(
        stage,
        resolveAssetPathFn=functools.partial(
            _remove_anonymous_asset_paths,
            identifiers=tuple(root.identifier for root in roots),
        ),
    )

    # XXX : Merge each anonymous layer that was listed in `identifiers`
    # into the current stage. That way, the references that were created
    # will not break.
    #
    for root in roots:
        UsdUtils.StitchLayers(layer, root)

    print(layer.ExportToString())


if __name__ == "__main__":
    main()
