## Quick Explanation
The USD documentation does a good job of explaining this concept.
Essentially, plugin metadata is a way to add custom metadata information onto
prims, attributes, layers, etc. that you wouldn't normally be able to
add to. It's also easy to set up. The steps can be boiled down to:

1. Create a `plugInfo.json` file that describes the metadata that you want to add
2. Include the `plugInfo.json` parent directory into the `PXR_PLUGINPATH_NAME` environment variable so that it is discoverable by USD
3. Work as you normally do. Get/Set the metadata.

This folder shows how to query the metadata, get information about it
it in USD's schema registry, and how to author the plugin metadata
`plugInfo.json` file.


## How To Check If Plugin Metadata Loaded
### C++
This gets you fallback information for metadata that is meant to be
authored onto a SdfPrimSpec.
```cpp
auto fallback = pxr::SdfSchema::GetInstance().GetFallback(pxr::TfToken {"my_custom_double"});
assert(fallback == 12.0 && "Plugin Metadata was not sourced correctly");
```

This gets you fallback information for metadata that is meant to be
authored onto a SdfLayer.
```python
assert layer.pseudoRoot.GetFallbackForInfo("another_metadata") == Vt.DoubleArray(
	[5, 13]
), message
```


## See Also
https://graphics.pixar.com/usd/docs/api/sdf_page_front.html#sdf_plugin_metadata
