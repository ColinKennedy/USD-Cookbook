#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A module that checks if the VariantSet fallback plugin works."""

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Pcp, Usd


def main():
    """Run the main execution of the current script."""
    Usd.Stage.SetGlobalVariantFallbacks({"some_variant_set_name": ["foo", "bar"]})

    stage = Usd.Stage.Open("../example_file/variant_set_with_no_authored_selection.usda")
    prim = stage.DefinePrim("/SomePrim")
    variant_set = prim.GetVariantSets().AddVariantSet("some_variant_set_name")

    variant_set.AddVariant("foo")
    variant_set.AddVariant("bar")

    print(
        'The currently-selected variant: "{}"'.format(variant_set.GetVariantSelection())
    )


# def main():
#     """Run the main execution of the current script.
#
#     Important:
#         As mentioned in the `variant_fallbacks/README.md` file, variant
#         fallbacks are determined per-stage exactly when the stage is
#         first created.
#
#         Most projects in this repository use stages that only exist in
#         memory but, in this case, it's easier to provide Prims up-front
#         by reading and existing USD file instead of creating one, from
#         scratch.
#
#     """
#     stage = Usd.Stage.Open(
#         "../example_file/variant_set_with_no_authored_selection.usda"
#     )
#     prim = stage.DefinePrim("/SomePrim")
#     variant_set = prim.GetVariantSets().GetVariantSet("some_variant_set_name")
#
#     print(
#         'The currently-selected variant (which should be "foo"): "{}"'.format(
#             variant_set.GetVariantSelection()
#         )
#     )
#
#
if __name__ == "__main__":
    main()
