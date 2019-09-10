#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""An example module that shows how to "contextualize" a relative path resolve.

Important:
    If you try to load "some_stage.usda", you'll get a resolve warning.

    Warning: in _ReportErrors at line 2782 of /home/selecaoone/Downloads/USD/pxr/usd/lib/usd/stage.cpp -- Could not open asset @some_nested_layer.usda@ for reference on prim @some_stage.usda@,@anon:0x1303750:some_stage-session.usda@</SomePrim3>. (instantiating stage on stage @some_stage.usda@ <0x130b060>)

    The stage couldn't open "some_stage.usda" wrote
    @some_nested_layer.usda@ asset incorrectly. It should instead be
    @nested/some_nested_layer.usda@. This is true whether you call
    `Usd.Stage.Open` inside __or__ outside of the context binder.

    - But, if you try to load "some_nested_layer.usda" using
    `UsdUtils.ComputeAllDependencies` within the `Ar.ResolverContextBinder`,
    that will return back the correct Layer path!

    - If you remove `nested_folder` from
    `Ar.DefaultResolverContext([project_folder, nested_folder])`,
    `UsdUtils.ComputeAllDependencies` will return "some_nested_layer.usda"
    as an unresolved dependency.

"""

# IMPORT FUTURE LIBRARIES
from __future__ import print_function

# IMPORT STANDARD LIBRARIES
import os

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Ar, Usd, UsdGeom, UsdUtils

_CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def main():
    """Run the main execution of the current script."""
    project_folder = os.path.join(_CURRENT_DIR, "project_folder")
    nested_folder = os.path.join(project_folder, "nested")
    context = Ar.DefaultResolverContext([project_folder, nested_folder])

    path = "some_stage.usda"
    print('The path to find: "{path}".'.format(path=path))
    resolver = Ar.GetResolver()
    print(
        'This path should be empty: "{result}".'.format(result=resolver.Resolve(path))
    )

    with Ar.ResolverContextBinder(context):
        print(
            'Now the path will actually resolve, "{result}".'.format(
                result=resolver.Resolve(path)
            )
        )
        print(
            "And we can even get dependency information",
            UsdUtils.ComputeAllDependencies(path),
        )

        print()
        print("XXX: We can resolve any of the below relative paths in this context")
        print("The next 2 paths will resolve because we added `project_folder`")
        print(resolver.Resolve("a_dependent_layer.usda"))
        print(resolver.Resolve("data.json"))
        print("The next path will resolve because we added `nested_folder`")
        print(resolver.Resolve("some_nested_layer.usda"))
        print()

        stage = Usd.Stage.Open("some_stage.usda")

    print()
    print(
        "XXX: But if we try to query information from the paths, that "
        "doesn't work. It's the same whether we're inside or outside "
        "of the context."
    )
    prim = UsdGeom.Sphere(stage.GetPrimAtPath("/SomePrim"))
    print(prim.GetRadiusAttr().Get())
    prim = UsdGeom.Sphere(stage.GetPrimAtPath("/SomePrim2"))
    print(prim.GetRadiusAttr().Get())
    prim = UsdGeom.Sphere(stage.GetPrimAtPath("/SomePrim3"))
    print(
        'This will be None, because @some_nested_layer.usda will not resolve: "{value}"'.format(
            value=prim.GetRadiusAttr().Get()
        )
    )


if __name__ == "__main__":
    main()
