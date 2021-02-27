#!/usr/bin/env python
# -*- coding: utf-8 -*-

import textwrap

from pxr import Sdf, Usd, UsdGeom


def _run_resolution_test():
    referencee = Usd.Stage.CreateInMemory()
    referencee.GetRootLayer().ImportFromString(
        """\
        #usda 1.0
        (
            defaultPrim = "root"
        )

        def Scope "root"
        {
            def Sphere "sphere"
            {
                double radius = 2
                double radius.timeSamples = {
                    10: 10,
                    40: 40,
                }
            }
        }
        """
    )

    referencer = Usd.Stage.CreateInMemory()
    root = referencer.DefinePrim("/root")
    root.GetReferences().AddReference(
        Sdf.Reference(
            referencee.GetRootLayer().identifier,
            layerOffset=Sdf.LayerOffset(
                offset=5, scale=2
            ),
        )
    )

    sphere = UsdGeom.Sphere(referencer.GetPrimAtPath("/root/sphere"))
    radius = sphere.GetRadiusAttr()

    times = [
        (10, 10.0, Usd.ResolveInfoSourceTimeSamples),
        (20, 10.0, Usd.ResolveInfoSourceTimeSamples),
        (25, 10.0, Usd.ResolveInfoSourceTimeSamples),
        (30, 12.5, Usd.ResolveInfoSourceTimeSamples),
        (55, 25.0, Usd.ResolveInfoSourceTimeSamples),
        (85, 40.0, Usd.ResolveInfoSourceTimeSamples),
    ]

    template = textwrap.dedent(
        """\
        Expected Value: "{expected_value}"
        Actual Value: "{actual_value}"
        Expected Resolve: "{expected_resolve}",
        Actual Resolve: "{actual_resolve}",\
        """
    )

    for time_code, expected_value, expected_resolve in times:
        print('Time Start: "{time_code}"'.format(time_code=time_code))
        print(
            template.format(
                expected_value=expected_value,
                actual_value=radius.Get(time_code),
                expected_resolve=expected_resolve,
                actual_resolve=radius.GetResolveInfo(time_code).GetSource(),
            )
        )
        print('Time End: "{time_code}"'.format(time_code=time_code))


def _run_linear_interpolation_test():
    stage = Usd.Stage.CreateInMemory()
    stage.GetRootLayer().ImportFromString(
        """\
        #usda 1.0

        def Scope "root"
        {
            int foo = 8
            int foo.timeSamples = {
                5: 10,
                20: 40,
            }
        }
        """
    )

    attribute = stage.GetObjectAtPath("/root.foo")

    for time_code in [-5, 3, 5, 10, 15, 20, 25]:
        value = is_interpolated(attribute, time_code)
        print('Time "{time_code}", Value "{value}"'.format(time_code=time_code, value=value))


def is_interpolated(attribute, frame):
    bracketing = attribute.GetBracketingTimeSamples(frame)

    # Note that some attributes return an empty tuple, some None, from
    # GetBracketingTimeSamples(), but all will be fed into this function.
    #
    return bracketing and (len(bracketing) == 2) and (bracketing[0] != frame)


def main():
    """Run the main execution of the current script."""
    stage = Usd.Stage.CreateInMemory()
    sphere = UsdGeom.Sphere.Define(stage, "/sphere")
    radius = sphere.CreateRadiusAttr()

    print('XXX : Starting resolution test')
    _run_resolution_test()
    print('XXX : Ending resolution test')

    print('XXX : Starting interpolation test')
    _run_linear_interpolation_test()
    print('XXX : Ending interpolation test')

    print('Radius will print 1.0 and Usd.ResolveInfoSourceFallback')
    print(radius.Get())
    print(radius.GetResolveInfo().GetSource())
    print('Now the radius will print 5.0 and Usd.ResolveInfoSourceDefault')
    radius.Set(5.0)
    print(radius.Get())
    print(radius.GetResolveInfo().GetSource())


if __name__ == "__main__":
    main()
