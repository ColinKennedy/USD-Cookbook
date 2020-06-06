#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A module used to get any Prim in a USD stage."""

from pxr import Sdf, Usd, UsdGeom


def _iter_all_parents(path):
    """Get every Sdf namespace on-and-above `path`.

    This function is inclusive - which means it returns `path` as part of its output.

    Args:
        path (:class:`pxr.Sdf.Path`):
            A Sdf namespace to some Prim. e.g. "/foo/bar", "/some{variant_set=selection}here", etc.

    Yields:
        :class:`pxr.Sdf.Path`: The given `path` and any found parents.

    """
    parent = path

    while not parent.IsRootPrimPath():
        yield parent
        parent = parent.GetParentPath()

    # Yield the root Prim path, too
    yield parent


def _gather_variant_selections(path):
    """Parse `path` into all of its variant set / selection details.

    Args:
        path (:class:`pxr.Sdf.Path`):
            A Sdf namespace to some Prim. e.g. "/foo/bar", "/some{variant_set=selection}here", etc.

    Returns:
        list[tuple[str, str, str]]:
            This output describes the variants `path` contains. Starting
            from `path`'s top-most parent down to the bottom, it
            returns a variant-less path + its variant data. e.g.
            "/some{variant_set=selection}here" returns. [("/some",
            "variant_set", "selection")].

    """
    output = []

    for path_ in reversed(list(_iter_all_parents(path))):
        variant_set, selection = path_.GetVariantSelection()

        if not variant_set or not selection:
            continue

        output.append((path_.StripAllVariantSelections(), variant_set, selection))

    return output


def get_prim_at_path(stage, path):
    """Get the Prim at `path`, using some `stage`.

    Warning:
        This function will modify the current state of `stage` to
        forcibly get the Prim at `path`. If you don't want this, you're
        better of using :func:`pxr.Usd.Stage.GetPrimAtPath`.

    Args:
        stage (:class:`pxr.Usd.Stage`):
            Some layer that contains Prims. Presumably, it also contains a Prim at `path`.
        path (:class:`pxr.Sdf.Path`):
            Some absolute path to a Prim which is assumed to live in
            `stage`. If the Prim lies inside of variant sets, make sure to include
            those details. e.g. `Sdf.Path("/foo{variant_set=selection}prim1")`.

    Raises:
        ValueError: If `path` is a valid Sdf Path but cannot be used by this function.

    Returns:
        :class:`pxr.Usd.Prim`: The found Prim at `path`.

    """
    if not path.ContainsPrimVariantSelection():
        return stage.GetPrimAtPath(path)

    root = path.GetPrimOrPrimVariantSelectionPath()

    if str(root).endswith("}"):
        raise ValueError(
            'Path "{root}" is not allowed. You cannot select a variant set directly.'.format(
                root=root
            )
        )

    for selector, variant_set, selection in _gather_variant_selections(root):
        prim = stage.GetPrimAtPath(selector)
        selector = prim.GetVariantSets().GetVariantSet(variant_set)
        selector.SetVariantSelection(selection)

    # Now that `stage` is in the correct state and every variant set
    # has been applied, we can finally select the Prim that `path` describes.
    #
    composed_path = path.StripAllVariantSelections()

    return stage.GetPrimAtPath(composed_path.GetPrimPath())


def main():
    """Run the main execution of the current script."""
    stage = Usd.Stage.CreateInMemory()
    stage.GetRootLayer().ImportFromString(
        """\
        #usda 1.0

        def Scope "root" (
            variantSets = ["foo"]
        )
        {
            variantSet "foo" = {
                "base" {
                    def Scope "prim1"
                    {
                        def Sphere "a_sphere"
                        {
                            double radius = 3
                        }
                    }
                }
                "another" {
                    def Scope "prim2" (
                        variantSets = ["bar"]
                    )
                    {
                        variantSet "bar" = {
                            "one" {
                                def Sphere "sphere"
                                {
                                    double radius = 2
                                }
                            }
                        }
                    }
                }
            }
        }
        """
    )

    variant_sphere = UsdGeom.Sphere(get_prim_at_path(stage, Sdf.Path("/root{foo=base}prim1/a_sphere")))
    print('This value should be 3.0: "{}"'.format(variant_sphere.GetRadiusAttr().Get()))

    nested_variant_sphere = UsdGeom.Sphere(get_prim_at_path(stage, Sdf.Path("/root{foo=another}prim2{bar=one}sphere")))
    print('This value should be 2.0: "{}"'.format(nested_variant_sphere.GetRadiusAttr().Get()))


if __name__ == "__main__":
    main()
