#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""An example of changing any part of a USD Layer's namespace."""

from __future__ import print_function
from pxr import Sdf


def main():
    """Run the main execution of the current script."""
    layer = Sdf.Layer.FindOrOpen("input.usda")

    # Try everything.
    edit = Sdf.BatchNamespaceEdit()
    edit.Add("/C", "/D")  # Prim renames
    edit.Add("/B", "/C")
    edit.Add("/D", "/B")
    edit.Add("/G", "/E/G")  # Prim reparents
    edit.Add("/H", "/E/F/H")
    edit.Add("/I", "/E/H")  # Prim reparent/rename
    edit.Add("/J", "/L/J")  # Prim reparent
    edit.Add("/L/J/K", "/K")  # Prim reparent from under a reparented prim
    edit.Add("/X", Sdf.Path.emptyPath)  # Prim remove
    edit.Add("/E", Sdf.Path.emptyPath)  # Prim with descendants remove

    edit.Add("/P.c", "/P.d")  # Prim property renames
    edit.Add("/P.b", "/P.c")
    edit.Add("/P.d", "/P.b")
    edit.Add("/P.g", "/Q.g")  # Prim property reparents
    edit.Add("/P.h", "/Q/R.h")
    edit.Add("/P.i", "/Q.h")  # Prim property reparent/rename
    edit.Add("/P.x", Sdf.Path.emptyPath)  # Prim property remove

    edit.Add("/S", "/T")  # Rename prim used in targets

    edit.Add("/V{v=one}U", "/V{v=two}W/U")  # Variant prim reparent/rename
    edit.Add("/V{v=two}W", Sdf.Path.emptyPath)  # Variant prim remove
    edit.Add("/V{v=one}.u", "/V{v=two}.u")  # Variant property reparent/rename
    edit.Add("/V{v=two}.w", Sdf.Path.emptyPath)  # Variant property remove

    before = layer.ExportToString()
    print('Will applying this layer fail?', not layer.CanApply(edit))
    assert layer.Apply(edit)
    after = layer.ExportToString()
    print(before == after)


if __name__ == "__main__":
    main()
