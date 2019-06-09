# Quick Reference
### C++
```cpp
auto variants = sphere.GetPrim().GetVariantSets();
auto variant = variants.AddVariantSet("some_variant");

variant.AddVariant("variant_name_1");

auto radius = sphere.GetRadiusAttr();

{
    variant.SetVariantSelection("variant_name_1");
    pxr::UsdEditContext context {variant.GetVariantEditContext()};
    radius.Set(1.0);
}
```


### Python
```python
variants = sphere.GetPrim().GetVariantSets().AddVariantSet('some_variant_set')
variants.AddVariant('variant_name_1')

variants.SetVariantSelection('variant_name_1')
with variants.GetVariantEditContext():
    sphere.GetRadiusAttr().Set(1)
```


### USD
base.usda
```usda
#usda 1.0

def Sphere "SomeSphere"
(
     variants = {
        string some_variant = "variant_name_2"
     }
     prepend variantSets = "some_variant"
)
{
    variantSet "some_variant" = {
        "variant_name_1" {
            double radius = 1.0
        }
        "variant_name_2" {
            double radius = 2.0
        }
        "variant_name_3" {
            double radius = 3.0
        }
    }
}
```

```usda
#usda 1.0
(
    subLayers = [
        @./base.usda@
    ]
)

over "SomeSphere" (
    variants = {
        string some_variant_set = "foo"
    }
    prepend variantSets = ["another", "some_variant_set"]
)
{
    variantSet "some_variant_set" = {
        "foo" {
            double radius = 100

        }
    }
}
```

# See Also
https://graphics.pixar.com/usd/docs/USD-Glossary.html#USDGlossary-VariantSet

https://graphics.pixar.com/usd/docs/USD-Glossary.html#USDGlossary-Variant
