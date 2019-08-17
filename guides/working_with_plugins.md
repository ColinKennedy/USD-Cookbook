There's 2 ways of extending USD for your pipeline
1. Fork USD and add the features in that you want (and then PR it back so others can use it!)
2. Use Plugins

Option #2 is way easier to do and easier to maintain. But how are
you supposed to know which USD features can be changed by using
plugins? There's no master-list of how USD uses their own [Plugin
Framework](https://graphics.pixar.com/usd/docs/api/plug_page_front.html)
. And there's no way to query that information in code, either. The best
you can do is query what plugins are discoverable (which we'll get to in
a bit).

Rather than write cookbook projects for every USD plugin, it makes more
sense to make a glossary for reference and explain how to find out more
information.

With that said, this guide will teach:

- What plugins USD uses
- The source-code location to find out more about those plugins
- How to find plugins, yourself


## Plugin Summary
USD has two main methods of querying plugins. It either queries plugins
using a reserved plugin key or source code will iterate over every
plugin and filter by some condition, like "X plugin is a subclass of Foo
base plugin".

Skip to [How To Find Where To Look](How-To-Find-Where-To-Look) to find
out how to search these definitions by yourself.


## Usage Table Of Contents
Here's a quick list of both styles that USD uses to query plugins.

### "By-Name" Plugins
- UsdGeomMetrics - [Set Your Default Scene Up Axis](Set-Your-Default-Scene-Up-Axis)
- UsdColorConfigFallbacks - [Set Up Color Management](Set-Up-Color-Management)
- UsdUtilsPipeline
    - MaterialsScopeName
    - PrimaryCameraName
    - RegisteredVariantSets
- DefaultMaterialsScopeName
- DefaultPrimaryCameraName


### Filtered Plugins
TODO: Write here


## How To Query Discovered Plugins
If you're only interested in finding out what plugins are loaded, USD
already has a convenience method for that. That said, if you're using
a default build of USD, the methods won't return very interesting
results. But in a studio pipeline this list is a great opportunity for
"discovering" projects that you may not have been aware of.

```python
from pxr import Plug

for plugin in Plug.Registry().GetAllPlugins():
    print('Plugin: "{plugin.name}" is loaded: "{plugin.isLoaded}".'.format(plugin=plugin))
    print('Path: "{plugin.path}".'.format(plugin=plugin))
```

Example Output on a default build of USD:

```
Plugin: "usd" is loaded: "False".
Path: "/usr/local/USD-19.07/lib/libusd.so".
Plugin: "usdGeom" is loaded: "False".
Path: "/usr/local/USD-19.07/lib/libusdGeom.so".
Plugin: "usdLux" is loaded: "False".
Path: "/usr/local/USD-19.07/lib/libusdLux.so".
Plugin: "usdHydra" is loaded: "False".
Path: "/usr/local/USD-19.07/lib/libusdHydra.so".
...
```

USD uses its own plugin system to register many of its own modules. So
you'll always see its libraries mixed in with any proprietary ones that
a studio has added.


## Plugin Details
This section goes over some simple plugins, what they do, and links to
learn more. If a section contains sample plugin text, assume that the
file needs to be named `plugInfo.json` and its directory should be found
in the PXR_PLUGINPATH_NAME environment variable.

If you don't know what this means, check out
[The Variant Selection Fallback Plugin](../concepts/variant_fallbacks/README.md)
or
[The Plugin Metadata Plugin](../concepts/plugin_metadata/README.md)
or
[The Custom Resolver Plugin](../concepts/custom_resolver/README.md)
projects to find out more information.
Also, there's [the USD PluginRegistry
documentation](https://graphics.pixar.com/usd/docs/api/class_plug_regist
ry.html)


### Set Your Default Scene Up Axis
Summary: Set a value for the up axis for USD scenes that don't have an authored up-axis value
Key: UsdGeomMetrics
Related Links:
 - https://graphics.pixar.com/usd/docs/api/group___usd_geom_up_axis__group.html#gaf16b05f297f696c58a086dacc1e288b5
 - https://graphics.pixar.com/usd/docs/api/group___usd_geom_up_axis__group.html
Source Code Link: [pxr/usd/lib/usdGeom/metrics.cpp](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usd/lib/usdGeom/metrics.cpp#L89-L164)

Plugin Sample Text:

`plugInfo.json`
```json
{
    "Plugins": [
        {
            "Type": "resource",
            "Name": "scene_up_plugin",
            "Info": {
                "UsdGeomMetrics": {
                    "upAxis": "Z"
                }
            }
        }
    ]
}
```

TODO : Add Python and C++ commands
Relevant Commands:
```cpp
SdfSchema::GetInstance().GetFallback(UsdGeomTokens->upAxis)
```

```python
from pxr import Usd, UsdGeom
stage = Usd.Stage.CreateInMemory()
print(UsdGeom.GetStageUpAxis(stage))  # Prints "Y" normally but will print "Z" if the plugin is installed
```


### Set Up Color Management
Summary: A way to store and interpret per-attribute color-space values
Key: "UsdColorConfigFallbacks"
Description: USD lets you set colorspace information in layers
    and attribute as metadata. If there's nothing authored, the color
    configuration fallback plugin is queried, instead. This is very useful
    because it lets different projects use different configurations.
Source Code Link: [pxr/usd/lib/stage.cpp](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usd/lib/usd/stage.cpp#L127-L181)
Related Links:
 - https://graphics.pixar.com/usd/docs/api/class_usd_stage.html#Usd_ColorConfigurationAPI
Plugin Sample Text:

`plugInfo.json`
```json
```

Relevant Source Code:
[Looks.usda](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usd/plugin/usdMtlx/testenv/testUsdMtlxFileFormat.testenv/baseline/Looks.usda#L1-L7)
(This code can be used to explicitly set color management settings, per-layer)
```usda
#usda 1.0
(
    colorManagementSystem = "ocio"
    customLayerData = {
        string colorSpace = "acescg"
    }
)
```

[Looks.usda](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usd/plugin/usdMtlx/testenv/testUsdMtlxFileFormat.testenv/baseline/Looks.usda#L1-L7)
(This code can be used to explicitly set color management settings, per-attribute)
```usda
color3f inputs:otherColor6 = (0.1, 0.1, 0.1) (
    colorSpace = "lin_rec709"
)
```


Relevant Commands:

TODO : Add Python commands
```cpp
UsdStage::SetColorConfiguration(const SdfAssetPath &colorConfig) const;
SdfAssetPath UsdStage::GetColorConfiguration() const;
void UsdStage::SetColorManagementSystem(const TfToken &cms) const;
TfToken UsdStage::GetColorManagementSystem() const;
```



## TODO unsorted
This repository already covers a
hdxPrman
 resources/shaders (path)


RMAN_RIXPLUGINPATH
 - all paths


std::string rmantree = TfGetenv("RMANTREE");
 - lib/plugins/Args


metadata
 -


Kinds
 - dict
  - the key is the name
   - baseKind - str
 - https://graphics.pixar.com/usd/docs/api/kind_page_front.html#kind_extensions
 - pxr/usd/lib/kind/registry.cpp



Check out what GetAllDerivedTypes does
 - pxr/usd/lib/ndr/registry.cpp
 - third_party/houdini/lib/gusd/USD_CustomTraverse.cpp






SdfFileFormats
 - any plugin that derives from SdfFileFormat
All derived SdfFileFormat types

    TfType formatBaseType = TfType::Find<SdfFileFormat>();

    if (TF_VERIFY(!formatBaseType.IsUnknown()))
        PlugRegistry::GetAllDerivedTypes(formatBaseType, &formatTypes);

- formatId - string
- extensions - list of strings. It's the filetype extension
- target - the location it will go in(?)
- primary - if this file format plugin should be the preferred plugin for its extensions
-  pxr/usd/lib/sdf/fileFormatRegistry.cpp
- TODO find a file that registers this. Alembic should be one good example
- https://graphics.pixar.com/usd/docs/api/sdf_page_front.html#sdf_fileFormatPlugin
    - couldn't find a better link


const TfType defaultResolverType = TfType::Find<ArDefaultResolver>();

        PlugRegistry::GetAllDerivedTypes(
            TfType::Find<ArResolver>(), &resolverTypes);
pxr/usd/lib/ar/resolver.cpp

void ArSetPreferredResolver(const std::string& resolverTypeName);
 - used when getting ar plugins



UsdVariantFallbacks
 - already covered this one
 - TODO link to wherever I've got that in the cookbook
 - pxr/usr/lib/stage.cpp
 - https://graphics.pixar.com/usd/docs/api/class_usd_stage.html#a34d1d78fe8e31f0ba439d2265d694af5



```cpp
/* static */
UsdMayaPrimReaderRegistry::ReaderFactoryFn
UsdMayaPrimReaderRegistry::Find(const TfToken& usdTypeName)
```

TODO Check what runs this function to find out what type names Maya allows



TODO Check this too
TfType
UsdSchemaRegistry::GetTypeFromName(const TfToken& typeName){
    return PlugRegistry::GetInstance().FindDerivedTypeByName(
        *_schemaBaseType, typeName.GetString());
}


pxr/usd/lib/ar/resolver.cpp
- TODO wtf are package resolvers?


UsdUtilsPipeline
 - I have an example for this already
 - pxr/usd/lib/usdUtils/pipeline.cpp

UsdUtilsPipeline
    (UsdUtilsPipeline)
        (MaterialsScopeName)
        (PrimaryCameraName)
    GetPrimaryCameraName
 - https://graphics.pixar.com/usd/docs/api/pipeline_8h.html#a589b8a95736d7cd9b0ce9f6ac9fc147c
 - https://graphics.pixar.com/usd/docs/api/pipeline_8h.html#a7b291555b813b2fa2665531dd98995a2

```json
"UsdImagingOpenVDBAssetAdapter": {
    "bases": [
        "UsdImagingFieldAdapter"
    ],
    "isInternal": true,
    "primTypeName": "OpenVDBAsset"
},
"UsdImagingField3DAssetAdapter": {
    "bases": [
        "UsdImagingFieldAdapter"
    ],
    "isInternal": true,
    "primTypeName": "Field3DAsset"
}
```

- isInternal - bool - used by Pixar to allow users to disable plugins that are crashing or executing slowly. Not meant to be used by clients of USD
- primTypeName - string - the name of the Prim that the plugin is meant for
 - Driven by by the USDIMAGING_ENABLE_PLUGINS environment variable.
 - https://graphics.pixar.com/usd/docs/api/class_usd_imaging_adapter_registry.html#a44227db6636d587bcd6500275f9de4f6

pxr/usdImaging/lib/usdImaging/adapterRegistry.cpp


shaderResources -
```json
{
    "Plugins": [
        {
            "Info": {
                "ShaderResources": "shaders"
            },
            "LibraryPath": "@PLUG_INFO_LIBRARY_PATH@",
            "Name": "hdSt",
            "ResourcePath": "@PLUG_INFO_RESOURCE_PATH@",
            "Root": "@PLUG_INFO_ROOT@",
            "Type": "library"
        }
    ]
}
```

- shaderResources - string - A folder to shaders to load into hydra
- pxr/imaging/lib/hio/glslfx.cpp


pxr/imaging/lib/glf/rankedTypeMap.h - Honorable mention (not sure how it's used)

https://github.com/parallax/ar-export/blob/master/libs/USDPython/USD/usd/sdf/resources/plugInfo.json



- implementsComputeExtent
 - It's a type-specific plugin
 - requires a function to be defined in the generated schema's .cpp file
 ```cpp
  TF_REGISTRY_FUNCTION(UsdGeomBoundable)
  {
      UsdGeomRegisterComputeExtentFunction<MyPrim>(MyComputeExtentFunction);
  }

 ```


 - https://graphics.pixar.com/usd/docs/api/boundable_compute_extent_8h.html#a4564996409a8ce82ca1c8c7aa41a16ac
 - pxr/usr/lib/usdGeom/boundableComputeExtent.cpp



## How To Find Where To Look
