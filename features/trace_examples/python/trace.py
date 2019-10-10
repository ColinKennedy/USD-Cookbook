#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module tests the Trace.TraceFunction and TraceScope context.

The code that this tests runs has been re-used from the
`sdf_change_block` feature project with some minor changes.

"""

from pxr import Trace, Sdf, Usd, UsdGeom


def create_sdf_primspecs_normally():
    """Create Sdf Primspecs."""
    layer = Sdf.Layer.CreateAnonymous()

    paths = {
        Sdf.Path("/AndMore"),
        Sdf.Path("/AnotherOne"),
        Sdf.Path("/AnotherOne/AndAnother"),
        Sdf.Path("/More"),
        Sdf.Path("/OkayNoMore"),
        Sdf.Path("/SomeSphere"),
        Sdf.Path("/SomeSphere/InnerPrim"),
        Sdf.Path("/SomeSphere/InnerPrim/LastOne"),
    }

    prefixes = set(prefix for path in paths for prefix in path.GetPrefixes())

    for path in prefixes:
        prim_spec = Sdf.CreatePrimInLayer(layer, path)
        prim_spec.specifier = Sdf.SpecifierDef
        prim_spec.typeName = UsdGeom.Xform.__name__

    with Trace.TraceScope("Inner Scope"):
        Sdf.Path("/SomeSphere/Prim/Created/In/Inner/Scope")
        prim_spec = Sdf.CreatePrimInLayer(layer, path)
        prim_spec.specifier = Sdf.SpecifierDef
        prim_spec.typeName = UsdGeom.Xform.__name__


def create_sdf_primspecs_using_change_block():
    """Create Sdf Primspecs in a single block of changes."""
    layer = Sdf.Layer.CreateAnonymous()

    paths = {
        Sdf.Path("/AndMore"),
        Sdf.Path("/AnotherOne"),
        Sdf.Path("/AnotherOne/AndAnother"),
        Sdf.Path("/More"),
        Sdf.Path("/OkayNoMore"),
        Sdf.Path("/SomeSphere"),
        Sdf.Path("/SomeSphere/InnerPrim"),
        Sdf.Path("/SomeSphere/InnerPrim/LastOne"),
    }

    prefixes = set(prefix for path in paths for prefix in path.GetPrefixes())

    with Sdf.ChangeBlock():
        for path in prefixes:
            prim_spec = Sdf.CreatePrimInLayer(layer, path)
            prim_spec.specifier = Sdf.SpecifierDef
            prim_spec.typeName = UsdGeom.Xform.__name__

    with Trace.TraceScope("Inner Scope"):
        Sdf.Path("/SomeSphere/Prim/Created/In/Inner/Scope")
        prim_spec = Sdf.CreatePrimInLayer(layer, path)
        prim_spec.specifier = Sdf.SpecifierDef
        prim_spec.typeName = UsdGeom.Xform.__name__


def main():
    """Run the main execution of the current script."""
    print("It's not enough to just add a Trace.TraceFunction decorator / scope.")
    print("You must also enable a collector")
    create_sdf_primspecs_normally()
    create_sdf_primspecs_using_change_block()

    print("This next report will be empty")
    reporter = Trace.Reporter.globalReporter
    reporter.Report()

    print("This next report will have contents, because the collector is recorded")
    collector = Trace.Collector()
    collector.enabled = True
    create_sdf_primspecs_normally()
    collector.enabled = False

    reporter = Trace.Reporter.globalReporter  # This is a singleton object
    reporter.Report()
    # reporter.ReportTimes()  # XXX : A more concise ms timing view

    print("This final report uses an SdfChangeBlock - it should be much faster")
    # XXX: On my machine, using the SdfChangeBlock was consistently 60-100 ms faster
    collector.Clear()  # XXX : This clears pending events
    reporter.ClearTree()  # XXX : Use `ClearTree` to reset the reporter back to 0 before reporting again
    collector.enabled = True
    create_sdf_primspecs_using_change_block()
    collector.enabled = False

    reporter.Report()
    # reporter.ReportTimes()  # XXX : A more concise ms timing view


if __name__ == "__main__":
    main()
