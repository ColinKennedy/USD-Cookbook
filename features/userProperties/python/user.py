#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""An example of how to set a custom Property, using userProperties."""

# IMPORT FUTURE LIBRARIES
from __future__ import print_function

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Sdf, Usd, UsdGeom


def main():
    """Run the main execution of the current script."""
    def is_user_property(node):
        return node.startswith("userProperties:")

    stage = Usd.Stage.CreateInMemory()
    sphere = UsdGeom.Sphere.Define(stage, "/SomeSphere")
    attribute = sphere.GetPrim().CreateAttribute(
        "userProperties:some_attribute", Sdf.ValueTypeNames.Bool, True
    )
    attribute.Set(False)
    some_attribute_that_will_not_be_printed = sphere.GetPrim().CreateAttribute(
        "another", Sdf.ValueTypeNames.Bool, True
    )

    print('user properties', sphere.GetPrim().GetAuthoredProperties(is_user_property))


if __name__ == "__main__":
    main()
