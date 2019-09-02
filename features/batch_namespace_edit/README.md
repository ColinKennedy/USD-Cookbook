## Quick Explanation
Sdf Layers can use change blocks to prevent notifications from being
sent whenever edits to a layer occur. But for simple namespace changes,
Sdf Layers have another technique that can be used to make many changes
at once, as long as you know every change that you need to make,
up-front. It's called a BatchNamespaceEdit.

Quick note: 
    The code used in this concept was taken straight from USD's unittests.
    So this section is mostly just to make an existing feature more
    visible, since you normally would have to dig to find out this information.


### C++
```cpp
edit.Add(
    pxr::SdfNamespaceEdit{
        pxr::SdfPath{"/C"},
        pxr::SdfPath{"/D"},
    },
);  // Prim renames
edit.Add(
    pxr::SdfNamespaceEdit{
        pxr::SdfPath{"/G"},
        pxr::SdfPath{"/E/G"},
    },
);  // Prim reparents
edit.Add(
    pxr::SdfNamespaceEdit{
        pxr::SdfPath{"/I"},
        pxr::SdfPath{"/E/H"},
    },
);  // Prim reparent/rename
edit.Add(
    pxr::SdfNamespaceEdit{
        pxr::SdfPath{"/L/J/K"},
        pxr::SdfPath{"/K"},
    },
);  // Prim reparent from under a reparented prim
edit.Add(
    pxr::SdfNamespaceEdit{
        pxr::SdfPath{"/X"},
        pxr::SdfPath::EmptyPath(),
    },
);  // Prim remove
edit.Add(
    pxr::SdfNamespaceEdit{
        pxr::SdfPath{"/E"},
        pxr::SdfPath::EmptyPath(),
    },
);  // Prim with descendants remove

edit.Add(
    pxr::SdfNamespaceEdit{
        pxr::SdfPath{"/P.c"},
        pxr::SdfPath{"/P.d"},
    },
);  // Prim property renames
edit.Add(
    pxr::SdfNamespaceEdit{
        pxr::SdfPath{"/P.g"},
        pxr::SdfPath{"/Q.g"},
    },
);  // Prim property reparents

edit.Add(
    pxr::SdfNamespaceEdit{
        pxr::SdfPath{"/S"},
        pxr::SdfPath{"/T"},
    },
);  // Rename prim used in targets


edit.Add(
    pxr::SdfNamespaceEdit{
        pxr::SdfPath{"/V{v=one}U"},
        pxr::SdfPath{"/V{v=two}W/U"},
    },
);  // Variant prim reparent/rename
edit.Add(
    pxr::SdfNamespaceEdit{
        pxr::SdfPath{"/V{v=two}W"},
        pxr::SdfPath::EmptyPath(),
    },
);  // Variant prim remove
edit.Add(
    pxr::SdfNamespaceEdit{
        pxr::SdfPath{"/V{v=one}.u"},
        pxr::SdfPath{"/V{v=two}.u"},
    },
);  // Variant property reparent/rename
edit.Add(
    pxr::SdfNamespaceEdit{
        pxr::SdfPath{"/V{v=two}.w"},
        pxr::SdfPath::EmptyPath(),
    },
);  // Variant property remove
```

#### C++ - Checking if an apply will work
```cpp
    std::cout << std::boolalpha;
    auto result = layer->CanApply(edit);
    std::cout << "Will applying this layer fail? " << (result == pxr::SdfNamespaceEditDetail::Result::Error) << '\n';
    assert(layer->Apply(edit) && "The edit failed");
```

### Python
```python
edit.Add("/C", "/D")  # Prim renames
edit.Add("/G", "/E/G")  # Prim reparents
edit.Add("/I", "/E/H")  # Prim reparent/rename
edit.Add("/L/J/K", "/K")  # Prim reparent from under a reparented prim
edit.Add("/X", Sdf.Path.emptyPath)  # Prim remove
edit.Add("/E", Sdf.Path.emptyPath)  # Prim with descendants remove

edit.Add("/P.c", "/P.d")  # Prim property renames
edit.Add("/P.g", "/Q.g")  # Prim property reparents

edit.Add("/S", "/T")  # Rename prim used in targets

edit.Add("/V{v=one}U", "/V{v=two}W/U")  # Variant prim reparent/rename
edit.Add("/V{v=two}W", Sdf.Path.emptyPath)  # Variant prim remove
edit.Add("/V{v=one}.u", "/V{v=two}.u")  # Variant property reparent/rename
edit.Add("/V{v=two}.w", Sdf.Path.emptyPath)  # Variant property remove
```

#### Python - Checking if an apply will work
```python
print('Will applying this layer fail?', not layer.CanApply(edit))
# or, you can apply and test if the apply failed
assert layer.Apply(edit)
```


## See Also
https://github.com/PixarAnimationStudios/USD/blob/master/pxr/usd/lib/sdf/testenv/testSdfBatchNamespaceEdit.py
https://graphics.pixar.com/usd/docs/api/class_sdf_layer.html#a4c1b4761140c863aa0e6a2ef6fffe243
