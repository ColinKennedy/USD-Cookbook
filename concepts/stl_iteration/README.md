# Quick Reference
### C++
Example: Modifying objects
```cpp
std::for_each(std::begin(range), std::end(range), [](pxr::UsdPrim const &prim){
    pxr::UsdModelAPI(prim).SetKind(pxr::KindTokens->component);
});
```

Example: Printing / Reporting
```cpp
auto range = pxr::UsdPrimRange::Stage(stage);

// Get every prim using accumulate
auto text = std::accumulate(
    std::begin(range),
    std::end(range),
    std::string {"Prims:"},
    [](std::string text, pxr::UsdPrim const &prim) {
        return std::move(text) + "\n" + pxr::TfStringify(prim.GetPath());
    }
);
```
