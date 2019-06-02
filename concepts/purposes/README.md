# Quick Reference

```cpp
purpose = sphere.CreatePurposeAttr();
purpose.Set(pxr::UsdGeomTokens->proxy);
purpose.Set(pxr::UsdGeomTokens->default_);
purpose.Set(pxr::UsdGeomTokens->render);
purpose.Set(pxr::UsdGeomTokens->guide);
```

```python
purpose = sphere.CreatePurposeAttr()
purpose.Set(UsdGeom.Tokens.default_)
purpose.Set(UsdGeom.Tokens.guide)
purpose.Set(UsdGeom.Tokens.proxy)
purpose.Set(UsdGeom.Tokens.render)
```

```usda
#usda 1.0

def Xform "Xform"
{
    def Cube "SomeGuide"
    {
        uniform token purpose = "guide"
    }

    def Sphere "SomeRender"
    {
        uniform token purpose = "render"
    }

    def Cone "SomeProxy"
    {
        uniform token purpose = "proxy"
    }

    def Cylinder "SomeDefault"
    {
        uniform token purpose = "default"
    }
}
```

# See Also
https://graphics.pixar.com/usd/docs/USD-Glossary.html#USDGlossary-Purpose
