# Quick Reference

How do you merge changes in anonymous layers onto a stage if the layers
have unsaved edits? There are multiple approaches but this section shows
one way to do it, which is to combine UsdUtilsFlattenLayerStack and
UsdUtilsStitchLayers.

The idea is to remove all references to the anonymous layers's
identifiers and then merge the layers into the stage until all Prims /
Properties are all together on the stage.


### C++

```cpp
std::vector<pxr::SdfLayerHandle> roots;
std::vector<std::string> identifiers;
// ...
pxr::UsdUtilsResolveAssetPathFn anonymous_path_remover =
    [&identifiers](pxr::SdfLayerHandle const &sourceLayer, std::string const &path) {
        if (std::find(std::begin(identifiers), std::end(identifiers), path) != std::end(identifiers)) {
            return std::string {};
        }

        return std::string {path.c_str()};
    };

auto layer = pxr::UsdUtilsFlattenLayerStack(stage, anonymous_path_remover);

for (auto const &root : roots) {
    pxr::UsdUtilsStitchLayers(layer, root);
}
```


### Python

```python
roots = set((layer.GetRootLayer() for layer in (anonymous1, anonymous2)))
layer = UsdUtils.FlattenLayerStack(
    stage,
    resolveAssetPathFn=functools.partial(
        _remove_anonymous_asset_paths,
        identifiers=tuple(root.identifier for root in roots),
    ),
)

for root in roots:
    UsdUtils.StitchLayers(layer, root)
```


# See Also
https://groups.google.com/d/msg/usd-interest/9-AFtWWOgQY/h8jc6vN0AwAJ

https://groups.google.com/d/msg/usd-interest/kV45vxQ9eNY/n8f6lAoSAQAJ
