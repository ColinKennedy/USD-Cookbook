# Quick Reference
### C++
```cpp
auto sphere = pxr::UsdGeomSphere(stage->DefinePrim(pxr::SdfPath("/thing/SomethingElse/NestedEvenMore"), pxr::TfToken("Sphere")));
auto prim = stage->DefinePrim(pxr::SdfPath("/thing/SomethingElse/SpecializedChild"));
prim.GetSpecializes().AddSpecialize(sphere.GetPath());
```


### Python
```python
sphere = UsdGeom.Sphere(stage.DefinePrim("/thing/SomethingElse/NestedEvenMore", "Sphere"))
prim = stage.DefinePrim("/thing/SomethingElse/SpecializedChild")
prim.GetSpecializes().AddSpecialize(sphere.GetPath())
```


### USD
```usda
#usda 1.00

def "thing" {
	def "SomethingElse" {
		def "NestedEvenMore" {
		}
	}

	def Sphere "SpecializedChild" (
		specializes = [
			</thing/SomethingElse/NestedEvenMore>
		]
	)
	{
	}
}
```


# See Also
https://graphics.pixar.com/usd/docs/USD-Glossary.html#USDGlossary-Specializes
