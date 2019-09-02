#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Show how to print variant selection export policies."""

# IMPORT FUTURE LIBRARIES
from __future__ import print_function

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Usd, UsdUtils


def main():
    """Run the main execution of the current script."""
    print('Printing the export policies')

    for variant in UsdUtils.GetRegisteredVariantSets():
        print(variant.name, variant.selectionExportPolicy)

    print('Done')

    stage = Usd.Stage.CreateInMemory()

    prim = stage.DefinePrim("/Foo")

    variant_set = prim.GetVariantSets().AddVariantSet("some_variant_set")

    variant_set.AddVariant("foo")
    variant_set.SetVariantSelection("foo")

    print('Notice that, unless we actually check the variant selections ourselves, they still get written to-disk.')
    print(stage.GetRootLayer().ExportToString())


if __name__ == "__main__":
    main()
