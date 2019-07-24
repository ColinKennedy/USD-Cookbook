## Quick Reference

If you have instanced Prims, traversals in USD can be a bit of a
pain. The typical traversal function that people normally use,
`pxr::UsdStage::TraverseAll`, stops at the root of an instance and
doesn't get back any child Prim information. But what it you need it?

Well, thankfully it's not too bad to do. But there is some manual
work involved. USD has something called an "instance proxy" which is
essentially an object that looks and acts like a regular Prim but
represents data that is shared from the instance's master.


### C++

```cpp
std::vector<pxr::UsdPrim> traverse_instanced_children(pxr::UsdPrim const &prim) {
    std::vector<pxr::UsdPrim> prims;

    auto range = prim.GetFilteredChildren(pxr::UsdTraverseInstanceProxies());
    prims.insert(std::end(prims), std::begin(range), std::end(range));

    for (auto const &child : range) {
        auto subchild_range = traverse_instanced_children(child);
        prims.reserve(subchild_range.size());
        prims.insert(std::end(prims), std::begin(subchild_range), std::end(subchild_range));
    }

    return prims;
}
```

### Python

```python
def traverse_instanced_children(prim):
    """Get every Prim child beneath `prim`, even if `prim` is instanced.

    Important:
        If `prim` is instanced, any child that this function yields will
        be an instance proxy.

    Args:
        prim (`pxr.Usd.Prim`): Some Prim to check for children.

    Yields:
        `pxr.Usd.Prim`: The children of `prim`.

    """
    for child in prim.GetFilteredChildren(Usd.TraverseInstanceProxies()):
        yield child

        for subchild in traverse_instanced_children(child):
            yield subchild
```


## See Also
https://graphics.pixar.com/usd/docs/api/_usd__page__scenegraph_instancing.html#Usd_ScenegraphInstancing_InstanceProxies
https://graphics.pixar.com/usd/docs/api/class_usd_prim.html#a33abfdbdc10aae66f611553867f6634a
