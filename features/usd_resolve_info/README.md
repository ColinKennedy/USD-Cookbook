## Quick Explanation

UsdResolveInfo is meant to inspect where an opinion
comes from. It's mainly used in usdview to display
information about properties to the user, covered on the
[usdview_style_documentation](../../references/usdview_style_documentation)
page.


## C++

```cpp
stage->GetPrimAtPath(pxr::SdfPath{"/Foo"}).GetAttribute(pxr::TfToken{"bar"}).GetResolveInfo().GetSource()
```


## Python

```python
stage.GetPrimAtPath("/Foo").GetAttribute("bar").GetResolveInfo().GetSource()
```


## Reference

[UsdResolveInfo](https://graphics.pixar.com/usd/docs/api/class_usd_resolve_info.html)
