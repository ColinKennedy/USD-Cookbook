#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT FUTURE LIBRARIES
from __future__ import print_function

# IMPORT STANDARD LIBRARIES
import functools
import time

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Usd, UsdGeom

REPEATS = 1000


def timeit(function, repeats):
    start = time.time()

    for _ in range(repeats):
        result = function()

    end = time.time()
    print(
        'Function "{function}" was called "{repeats}" times and took "{total:.1f}" milliseconds.'.format(
            function=function.__name__, repeats=repeats, total=(end - start) * 1000
        )
    )

    return result


def _create_basic_scene():
    stage = Usd.Stage.CreateInMemory()
    sphere = UsdGeom.Sphere.Define(stage, "/Some/Prim")
    sphere.GetRadiusAttr().Set(10.0)

    another = Usd.Stage.CreateInMemory()
    another.GetRootLayer().subLayerPaths.append(stage.GetRootLayer().identifier)
    override = UsdGeom.Sphere(another.OverridePrim("/Some/Prim"))
    override.GetRadiusAttr().Set(20.0)

    return another


def _create_basic_scene_with_more_values():
    stage = _create_basic_scene()
    override = UsdGeom.Sphere(stage.OverridePrim("/Some/Prim"))

    for sample in range(10000):
        override.GetRadiusAttr().Set(sample + 30, sample)

    return stage


def _get_time_samples(attributes):
    for attribute in attributes:
        attribute.GetTimeSamples()


def main():
    print("Simple Stage:")
    stage = _create_basic_scene()
    sphere = UsdGeom.Sphere(stage.GetPrimAtPath("/Some/Prim"))

    radius = sphere.GetRadiusAttr()
    print("Testing Get(), normally")
    timeit(radius.Get, REPEATS)

    query = Usd.AttributeQuery(radius)
    print(query.Get())
    radius.Set(100)
    print(query.Get())
    print("Testing Get(), using UsdAttributeQuery")
    timeit(query.Get, REPEATS)
    print()

    print("Testing GetTimeSamples(), normally")
    timeit(radius.GetTimeSamples, REPEATS)

    function = functools.partial(query.GetUnionedTimeSamples, [query])
    function.__name__ = "GetUnionedTimeSamples"
    print("Testing GetTimeSamples(), using a union")
    timeit(function, REPEATS)
    print()

    visibility = sphere.GetVisibilityAttr()

    function = functools.partial(_get_time_samples, (radius, visibility))
    function.__name__ = "_get_time_samples - with radius and visibility"
    print("Testing GetTimeSamples() for multiple attributes, normally")
    timeit(function, REPEATS)

    function = functools.partial(
        query.GetUnionedTimeSamples, [query, Usd.AttributeQuery(visibility)]
    )
    function.__name__ = "GetUnionedTimeSamples - with radius and visibility"
    print("Testing GetTimeSamples() for multiple attributes, using a union")
    timeit(function, REPEATS)
    print()

    print("Heavy Stage:")
    heavier_stage = _create_basic_scene_with_more_values()
    sphere = UsdGeom.Sphere(heavier_stage.GetPrimAtPath("/Some/Prim"))
    radius = sphere.GetRadiusAttr()
    visibility = sphere.GetVisibilityAttr()
    query = Usd.AttributeQuery(radius)
    function = functools.partial(_get_time_samples, (radius, visibility))
    function.__name__ = "_get_time_samples - with radius and visibility"
    print("Testing GetTimeSamples() for multiple attributes, normally")
    timeit(function, REPEATS)

    function = functools.partial(
        query.GetUnionedTimeSamples, [query, Usd.AttributeQuery(visibility)]
    )
    function.__name__ = "GetUnionedTimeSamples - with radius and visibility"
    print("Testing GetTimeSamples() for multiple attributes, using a union")
    timeit(function, REPEATS)


if __name__ == "__main__":
    main()
