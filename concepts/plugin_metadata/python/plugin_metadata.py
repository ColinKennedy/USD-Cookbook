#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A simple module that checks if the Plugin Metadata file was sourced correctly."""
# IMPORT THIRD-PARTY LIBRARIES
from pxr import Sdf, Vt


def main():
    """Run the main execution of the current script."""
    layer = Sdf.Layer.CreateAnonymous()

    message = "Plugin Metadata was not sourced correctly"
    primspec = Sdf.CreatePrimInLayer(layer, "/SomePrim")

    assert (
        "my_custom_double" in primspec.GetMetaDataInfoKeys()
    ), message

    assert layer.pseudoRoot.GetFallbackForInfo("another_metadata") == Vt.DoubleArray(
        [5, 13]
    ), message


if __name__ == "__main__":
    main()
