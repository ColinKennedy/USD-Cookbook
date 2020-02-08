# Quick Reference
### C++
```cpp
auto sphere = pxr::UsdGeomSphere::Define(stage, pxr::SdfPath {"/thing/SomethingElse/NestedEvenMore"});
auto prim = stage->DefinePrim(pxr::SdfPath("/thing/SomethingElse/SpecializedChild"));
prim.GetSpecializes().AddSpecialize(sphere.GetPath());
```


### Python
```python
sphere = UsdGeom.Sphere.Define(stage, "/thing/SomethingElse/NestedEvenMore")
prim = stage.DefinePrim("/thing/SomethingElse/SpecializedChild")
prim.GetSpecializes().AddSpecialize(sphere.GetPath())
```


### USD
```usda
#usda 1.0

def "thing"
{
    def "SomethingElse"
    {
        def Sphere "NestedEvenMore"
        {
        }

        def "SpecializedChild" (
            prepend specializes = </thing/SomethingElse/NestedEvenMore>
        )
        {
        }
    }
}
```


# See Also
https://graphics.pixar.com/usd/docs/USD-Glossary.html#USDGlossary-Specializes
