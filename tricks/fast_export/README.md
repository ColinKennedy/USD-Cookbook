# Quick Reference
The USD documentation states that defining Prims and reparenting prims
are some of the sloweest operations that USD does.

That said, USD's Sdf API is fast at authoring PrimSpecs so when I ran
across a suggestion the in USD forums to split an export into two passes
(one for the PrimSpecs and one for the Properties/Attributes), I had to
test it out.

On my machine, the SDF version is over 100x faster than authoring the
same Prims in a USD stage!


### C++

```cpp
auto prim_spec = pxr::SdfCreatePrimInLayer(layer, path);
prim_spec->SetSpecifier(pxr::SdfSpecifierDef);
```


### Python

```python
prim_spec = Sdf.CreatePrimInLayer(layer, path)
prim_spec.specifier = Sdf.SpecifierDef
```


# See Also
https://groups.google.com/d/msg/usd-interest/Bh6_sxij-f8/3UYUui3cAQAJ

https://groups.google.com/d/msg/usd-interest/Bh6_sxij-f8/rnGtLK3tAQAJ
