# Quick Reference

This concept copies a Variant Set into a Prim. You can also copy other
types too as long as the type can be referred to as a SdfPath.

In the documentation for SdfPrimSpec, there's a warning that the
destination parent Prim must exist.

Reference: https://graphics.pixar.com/usd/docs/api/copy_utils_8h.html#ad20defdb6654ee0937942116177fd4cc

The documentation suggests calling `SdfCreatePrimInLayer` before copying
anything over.


### C++

```cpp
pxr::SdfCopySpec(
    source,
    pxr::SdfPath {"/SomePrim{SomeVariantSet=SomeVariant}"},
    destination,
    pxr::SdfPath {"/DestinationPrim"}
);
```

```cpp
auto destination_prim = pxr::SdfPath {"/Another/DestinationPrim"};
pxr::SdfCreatePrimInLayer(destination, destination_prim);
pxr::SdfCopySpec(
    source,
    pxr::SdfPath {"/SomePrim{SomeVariantSet=SomeVariant}"},
    destination,
    destination_prim
);
```


### Python

```python
    Sdf.CopySpec(
        source,
        "/SomePrim{SomeVariantSet=SomeVariant}",
        destination,
        "/DestinationPrim",
    )
```

```python
destination_prim = "/Another/DestinationPrim"
Sdf.CreatePrimInLayer(destination, destination_prim)
Sdf.CopySpec(
    source,
    "/SomePrim{SomeVariantSet=SomeVariant}",
    destination,
    destination_prim,
)
```


# See Also
https://graphics.pixar.com/usd/docs/api/sdf_page_front.html

https://groups.google.com/d/msg/usd-interest/kV45vxQ9eNY/3viNsH8QAQAJ
