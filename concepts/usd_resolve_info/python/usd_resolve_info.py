#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Usd


def main():
    """Run the main execution of the current script."""
    stage = Usd.Stage.Open("usd_resolve_info.usda")
    prim = stage.GetPrimAtPath("/SomePrim")

    print(
        'time_samples_property - Is time samples "{}".'.format(
            prim.GetAttribute("time_samples_property").GetResolveInfo().GetSource()
            == Usd.ResolveInfoSourceTimeSamples
        )
    )
    print(
        'default_property - Is a default value "{}".'.format(
            prim.GetAttribute("default_property").GetResolveInfo().GetSource()
            == Usd.ResolveInfoSourceDefault
        )
    )

    sphere = stage.GetPrimAtPath("/SomeSphere")

    print(
        'radius - Is a type fallback value "{}".'.format(
            sphere.GetAttribute("radius").GetResolveInfo().GetSource()
            == Usd.ResolveInfoSourceFallback
        )
    )
    print(
        'xformOpOrder - Is empty value "{}".'.format(
            prim.GetAttribute("xformOpOrder").GetResolveInfo().GetSource()
            == Usd.ResolveInfoSourceNone
        )
    )
    print('value_clipped_property - Is value clip "{}".'.format(
        stage.GetPrimAtPath("/PrimWithValueClips").GetAttribute("inManifestAndInClip").GetResolveInfo(1).GetSource()
    ))


if __name__ == "__main__":
    main()
