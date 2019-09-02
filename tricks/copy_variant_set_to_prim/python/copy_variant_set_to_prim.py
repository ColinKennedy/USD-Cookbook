#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""An example module that shows how to copy SdfPath objects using the SDF API."""

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Sdf


def main():
    """Run the main execution of the current script."""
    source = Sdf.Layer.CreateAnonymous()
    root = source.pseudoRoot

    prim = Sdf.PrimSpec(root, "SomePrim", Sdf.SpecifierDef)
    variant_set = Sdf.VariantSetSpec(prim, "SomeVariantSet")
    variant = Sdf.VariantSpec(variant_set, "SomeVariant")
    Sdf.PrimSpec(variant.primSpec, "InnerPrim", Sdf.SpecifierDef)

    destination = Sdf.Layer.CreateAnonymous()
    Sdf.CopySpec(
        source, "/SomePrim{SomeVariantSet=SomeVariant}", destination, "/DestinationPrim"
    )

    # XXX : Notice that we have to call `CreatePrimInLayer` here but
    # we didn't need to run it in the last example. That's because
    # in this example, the parent Prim path "/Another" doesn't
    # exist yet and has to be created before data can be copied to
    # "/Another/DestinationPrim".
    #
    # In the previous example, "/" is the parent of "/DestinationPrim".
    # And "/" always exists. So we didn't need to call
    # `CreatePrimInLayer`. But generally, you usually should.
    #
    destination_prim = "/Another/DestinationPrim"
    Sdf.CreatePrimInLayer(destination, destination_prim)
    Sdf.CopySpec(
        source,
        "/SomePrim{SomeVariantSet=SomeVariant}",
        destination,
        destination_prim,
    )

    print(destination.ExportToString())


if __name__ == "__main__":
    main()
