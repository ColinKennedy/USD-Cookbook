# Quick Reference
USD Edit targets and Edit contexts directly modify USD Layers, according
to some stage.

Every USD stage has a USD Layer where, by default, all your
opinions go. It's called the "root" Layer and is accessed using
`stage.GetRootLayer()` / `stage->GetRootLayer()`.

All an Edit Target / Edit Context does is it tells USD "from here on,
any opinions will go in this other Layer instead of the root Layer".

## Important
Only USD Layers in the USD's LayerStack are able to be edit targets. In
other words, the layers must be available using the Sublayer composition
arc. You can't apply an edit target to a referenced Layer, for example.

## cpp
### Edit context
```cpp
{
    pxr::UsdEditContext context {main_stage, inner_stage->GetRootLayer()};
    auto sphere = pxr::UsdGeomSphere(main_stage->GetPrimAtPath(pxr::SdfPath{"/root/sphere"}));
    sphere.GetRadiusAttr().Set(10.0);
}
```

### Edit target
```cpp
main_stage->SetEditTarget(pxr::UsdEditTarget(inner_stage->GetRootLayer()));
auto sphere = pxr::UsdGeomSphere(main_stage->GetPrimAtPath(pxr::SdfPath{"/root/sphere"}));
sphere.GetRadiusAttr().Set(5.0);
```

## python
### Edit context
```python
with Usd.EditContext(main_stage, inner_stage.GetRootLayer()):
    sphere = UsdGeom.Sphere(main_stage.GetPrimAtPath("/root/sphere"))
    sphere.GetRadiusAttr().Set(10)
```

### Edit target
```python
main_stage.SetEditTarget(Usd.EditTarget(inner_stage.GetRootLayer()))
sphere = UsdGeom.Sphere(main_stage.GetPrimAtPath("/root/sphere"))
sphere.GetRadiusAttr().Set(5)
```


# References
[Edit Target Glossary Definition](https://graphics.pixar.com/usd/docs/USD-Glossary.html#USDGlossary-EditTarget)

[UsdEditTarget Documentation](https://graphics.pixar.com/usd/docs/api/class_usd_edit_target.html)

[UsdEditContext Documentation](https://graphics.pixar.com/usd/docs/api/class_usd_edit_context.html)
