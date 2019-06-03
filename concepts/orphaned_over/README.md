# Quick Reference

An orphaned Over is an Over that does not author an Opinion that affects
the composed Stage's result. In short, it's an `over` specifier that
points to nothing. Check out the [usda folder](usda) for a better idea
of what that looks like, if needed.


### C++
```cpp
for (auto const &prim : stage->TraverseAll()) {
    if (!prim.IsDefined()) {
        std::cout << prim.GetPath() << std::endl;
    }
}
```


### Python
```python
print(list(prim for prim in stage.TraverseAll() if not prim.IsDefined()))
```


# See Also
https://graphics.pixar.com/usd/docs/USD-Glossary.html#USDGlossary-Over
