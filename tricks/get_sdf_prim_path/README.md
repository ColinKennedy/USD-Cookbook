# Quick Reference
Sometimes, you just need to select a Prim. If you have no variant
sets, you can normally just do `stage.GetPrimAtPath("/foo/bar")` and
you're done. But what if "bar" is defined behind a variant set and that
variant set isn't selected in the current stage? Then GetPrimAtPath
returns an invalid Prim.

The basic steps goes like this
- Have a description of the entire path (including variants + their selections)
- Iterate overy every variant set and forcibly set the selections, one by one
- Then you can get your path


# See Also
[Variants Tutorial](https://graphics.pixar.com/usd/docs/Authoring-Variants.html)

[pxr::SdfPath::StripAllVariantSelections](https://graphics.pixar.com/usd/docs/api/class_sdf_path.html#af66d081e4ec164f04c3fb1805cfcfa4f)

[pxr::UsdObject::IsValid](https://graphics.pixar.com/usd/docs/api/class_usd_object.html#afa8720abaf6972d6dac22a8cd1a67225)
