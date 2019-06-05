# Quick Reference

Note: You can also give the UsdUtilsStitchLayers function a predicate
and control how stitching is handled. That isn't explored here but, if
you want to learn more, check out See Also

### C++

```cpp
auto strong_layer = pxr::SdfLayer::CreateAnonymous();
auto weak_layer = pxr::SdfLayer::CreateAnonymous();
pxr::UsdUtilsStitchLayers(strong_layer, weak_layer);
```

### Python

```python
weak_layer = Sdf.Layer.CreateAnonymous()
strong_layer = Sdf.Layer.CreateAnonymous()
UsdUtils.StitchLayers(strong_layer, weak_layer)
```

# See Also
https://graphics.pixar.com/usd/docs/api/stitch_8h.html#a9c953272f0b69e5b57e02cfe8a6cd2f8

https://github.com/PixarAnimationStudios/USD/blob/38c70fb869c01228f82fd844a8c420860b5131c1/pxr/usd/lib/usdUtils/testenv/testUsdUtilsStitch.cpp#L56-L95
