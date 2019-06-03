# Quick Reference
### C++
```cpp
auto bounds = pxr::UsdGeomImageable(sphere).ComputeWorldBound(
    pxr::UsdTimeCode(1),
    pxr::TfToken("default")
);
std::cout << bounds << std::endl;

auto cache = pxr::UsdGeomBBoxCache(
    pxr::UsdTimeCode().Default(),
    pxr::UsdGeomImageable::GetOrderedPurposeTokens()
);

std::cout << cache.ComputeWorldBound(sphere.GetPrim()) << std::endl;
```


### Python
```python
# Method #1: Compute at a certain time
print(UsdGeom.Imageable(sphere).ComputeWorldBound(
    Usd.TimeCode(1),
    purpose1='default',
))

# Method #2: Compute using a cache
cache = UsdGeom.BBoxCache(Usd.TimeCode.Default(), ['default', 'render'])
print(cache.ComputeWorldBound(sphere.GetPrim()))
```
