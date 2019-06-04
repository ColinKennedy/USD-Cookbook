# Quick Reference
### C++
Example: Using boost to do custom traverals
```cpp
auto range = pxr::UsdPrimRange::Stage(stage);

for (auto const &prim : range | boost::adaptors::filtered([](pxr::UsdPrim const &prim) {
    return prim.GetPath().GetName() == "AnotherSphere";
})) {
    pxr::UsdModelAPI(prim).SetKind(pxr::KindTokens->component);
}
```

# See Also
https://groups.google.com/forum/#!topic/usd-interest/J_tLjVaaePM
