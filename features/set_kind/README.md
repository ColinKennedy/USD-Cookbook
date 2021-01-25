# Quick Reference
### C++
```cpp
auto sphere = pxr::UsdGeomSphere::Define(stage, pxr::SdfPath("/SomeSphere"));
pxr::UsdModelAPI(sphere).SetKind(pxr::KindTokens->assembly);
pxr::UsdModelAPI(sphere).SetKind(pxr::KindTokens->component);
pxr::UsdModelAPI(sphere).SetKind(pxr::KindTokens->group);
pxr::UsdModelAPI(sphere).SetKind(pxr::KindTokens->subcomponent);
pxr::UsdModelAPI(sphere).SetKind(pxr::TfToken("does_not_exist"));
```


### Python
```python
sphere = UsdGeom.Sphere.Define(stage, "/SomeSphere")
Usd.ModelAPI(sphere).SetKind(Kind.Tokens.assembly)
Usd.ModelAPI(sphere).SetKind(Kind.Tokens.component)
Usd.ModelAPI(sphere).SetKind(Kind.Tokens.group)
Usd.ModelAPI(sphere).SetKind(Kind.Tokens.subcomponent)
Usd.ModelAPI(sphere).SetKind("does_not_exist")
```


### USD
```usda
#usda 1.0
(
    doc = "This is an example of setting a Model Prim kind"
)

def Sphere "Sphere1" (
    kind = "assembly"
) {
}

def Sphere "Sphere2" (
    kind = "component"
) {
}

def Sphere "Sphere3" (
    kind = "group"
) {
}

def Sphere "Sphere4" (
    kind = "subcomponent"
) {
}
```


# See Also

[Valid Model Hierarchies](../../concepts/valid_model_hierarchies)

https://graphics.pixar.com/usd/docs/USD-Glossary.html#USDGlossary-Kind

https://graphics.pixar.com/usd/docs/api/class_kind_registry.html
