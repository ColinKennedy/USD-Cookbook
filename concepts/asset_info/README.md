# Quick Reference
### C++
```cpp
prim.SetAssetInfoByKey(
    pxr::UsdModelAPIAssetInfoKeys->version,
    pxr::VtValue("v1")
);
prim.SetAssetInfoByKey(
    pxr::UsdModelAPIAssetInfoKeys->name,
    pxr::VtValue("some_asset")
);
prim.SetAssetInfoByKey(
    pxr::UsdModelAPIAssetInfoKeys->identifier,
    pxr::VtValue("some/path/to/file.usda")
);
prim.SetAssetInfoByKey(
    pxr::UsdModelAPIAssetInfoKeys->payloadAssetDependencies,
    pxr::VtValue{pxr::VtArray<pxr::SdfAssetPath> {
        pxr::SdfAssetPath("something.usd"),
        pxr::SdfAssetPath("another/thing.usd"),
    }}
);
```


### Python
```python
prim.SetAssetInfoByKey('version', 'v1')
prim.SetAssetInfoByKey('name', 'some_asset')
prim.SetAssetInfoByKey('identifier', 'some/path/to/file.usda')
prim.SetAssetInfoByKey(
    'payloadAssetDependencies',
    Sdf.AssetPathArray([
        Sdf.AssetPath('something.usd'),
        Sdf.AssetPath('another/thing.usd'),
    ]),
)
```


### USD
```usda
#usda 1.0

def Sphere "AnotherSphere" (
    assetInfo = {
        string identifier = "some/path/to/file.usda"
        string name = "some_asset"
        asset[] payloadAssetDependencies = [@something.usd@, @another/thing.usd@]
        string version = "v1"
    }
)
{
}
```

# See Also
https://graphics.pixar.com/usd/docs/USD-Glossary.html#USDGlossary-AssetInfo
