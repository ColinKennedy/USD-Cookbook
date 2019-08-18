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

Skip to [How To Find Where To Look](#How-To-Find-Where-To-Look) to find
out how to search these definitions by yourself.


## Table Of Contents
Here's a quick list of both styles that USD uses to query plugins.

### "By-Name" Plugins
- UsdGeomMetrics - [Set Your Default Scene Up Axis](#Set-Your-Default-Scene-Up-Axis)
- UsdColorConfigFallbacks - [Set Up Color Management](#Set-Up-Color-Management)
- UsdUtilsPipeline - [UsdUtilsPipeline](#UsdUtilsPipeline)
    - MaterialsScopeName - [Set Up A Registered Material Prim](#Set-Up-A-Registered-Material-Prim)
    - PrimaryCameraName - [Set Up A Default Camera Name](#Set-Up-A-Default-Camera)
    - RegisteredVariantSets - [Set Up Variant Selection Export Policies](#Set-Up-Variant-Selection-Export-Policies)
- DefaultMaterialsScopeName - [Set Up A Registered Material Prim](#Set-Up-A-Registered-Material-Prim)
- DefaultPrimaryCameraName - [Set Up A Default Camera Name](#Set-Up-A-Default-Camera)
- UsdVariantFallbacks - [Set Up Variant Selection Fallbacks](#Set-Up-Variant-Selection-Fallbacks)


### Filtered Plugins
- Kinds - [Subclass Your Own Kind](#Subclass-Your-Own-Kind)
- SdfMetadata - [Extend Metadata](#Extend-Metadata)


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
documentation](https://graphics.pixar.com/usd/docs/api/class_plug_registry.html)


### Set Your Default Scene Up Axis
**Summary**: Set a value for the up axis for USD scenes that don't have an authored up-axis value

**Key**: UsdGeomMetrics

**Related Links**:
 - [UsdGeomGetFallbackUpAxis](https://graphics.pixar.com/usd/docs/api/group___usd_geom_up_axis__group.html#gaf16b05f297f696c58a086dacc1e288b5)
 - [Encoding Stage UpAxis](https://graphics.pixar.com/usd/docs/api/group___usd_geom_up_axis__group.html)

**Source Code Link**: [pxr/usd/lib/usdGeom/metrics.cpp](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usd/lib/usdGeom/metrics.cpp#L89-L164)

**Plugin Sample Text**:

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
**Relevant Commands**:
```cpp
SdfSchema::GetInstance().GetFallback(UsdGeomTokens->upAxis)
```

```python
from pxr import Usd, UsdGeom
stage = Usd.Stage.CreateInMemory()
print(UsdGeom.GetStageUpAxis(stage))  # Prints "Y" normally but will print "Z" if the plugin is installed
```


### Set Up Color Management
**Summary**: A way to store and interpret per-attribute color-space values

**Key**: UsdColorConfigFallbacks

**Description**: USD lets you set colorspace information in layers
    and attribute as metadata. If there's nothing authored, the
    color configuration fallback plugin is queried, instead. This
    is very useful because it lets different projects use different
    configurations without changing any USD files.

**Source Code Link**: [pxr/usd/lib/stage.cpp](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usd/lib/usd/stage.cpp#L127-L181)

**Related Links**:
- [Color Configuration API](https://graphics.pixar.com/usd/docs/api/class_usd_stage.html#Usd_ColorConfigurationAPI)
    - Warning: The example plugInfo.json in the documentation has a syntax error ("colorConfiguration" = "https://github.com/imageworks/OpenColorIO-Configs/blob/master/aces_1.0.1/config.ocio"). Refer to the sample text below, instead:

**Plugin Sample Text**:

`plugInfo.json`
```json
{
    "Plugins": [
        {
            "Type": "resource",
            "Name": "color_management_definition",
            "Info": {
                "UsdColorConfigFallbacks": {
                    "colorConfiguration": "https://github.com/imageworks/OpenColorIO-Configs/blob/master/aces_1.0.1/config.ocio",
                    "colorManagementSystem": "OpenColorIO"
                }
            }
        }
    ]
}
```

**Defining Values in USDA, Explicitly**:

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


**Relevant Commands**:

TODO : Add Python commands
```cpp
UsdStage::SetColorConfiguration(const SdfAssetPath &colorConfig) const;
SdfAssetPath UsdStage::GetColorConfiguration() const;
void UsdStage::SetColorManagementSystem(const TfToken &cms) const;
TfToken UsdStage::GetColorManagementSystem() const;
```


### UsdUtilsPipeline
The `UsdUtilsPipeline` plugin key is a plugin that configures some default
USD stage settings.

#### Set Up A Default Camera Name
**Summary**: Store the name of the "primary/preferred camera" of your USD stage.

**Description**: If you define a PrimaryCameraName in UsdUtilsPipeline, that camera name is used. Otherwise, USD falls back to the site-defined DefaultPrimaryCameraName.

**Default**: If no primary camera name is given using this plugin, USD falls back to "main_cam".

**Key**:
 - [[UsdUtilsPipeline][PrimaryCameraName]](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usd/lib/usdUtils/pipeline.cpp#L365)
 - [DefaultPrimaryCameraName](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usd/lib/usdUtils/pipeline.cpp#L366)

**Related Links**:
 - [UsdUtilsGetPrimaryCameraName](https://graphics.pixar.com/usd/docs/api/pipeline_8h.html#a7b291555b813b2fa2665531dd98995a2)

**Source Code Link**:
 - [The main function that discovers all UsdUtilsPipeline-related plugins](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usd/lib/usdUtils/pipeline.cpp#L258-L330)

**Plugin Sample Text**:

`plugInfo.json`
```json
{
    "Plugins": [
        {
            "Name": "Default Camera Name",
            "Type": "resource",
            "Info": {
                "UsdUtilsPipeline": {
                    "PrimaryCameraName": "SomeCameraName"
                },
                "DefaultPrimaryCameraName": "SomeFallbackName"
            }
        }
    ]
}
```

**Relevant Commands**:
TODO : do Python, too
```cpp
TfToken UsdUtilsGetPrimaryCameraName(const bool forceDefault);
```


#### Set Up A Registered Material Prim
**Summary**: Let USD know that Prims given a certain name have materials
as its child Prims.

**Description**: From the USD documentation: "The name of the USD prim
under which materials are expected to be authored"

**Key**:
 - [[UsdUtilsPipeline][MaterialsScopeName]](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usd/lib/usdUtils/pipeline.cpp#L352)
 - [DefaultMaterialsScopeName](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usd/lib/usdUtils/pipeline.cpp#L353)

**Related Links**:
 - [UsdUtilsGetMaterialsScopeName](https://graphics.pixar.com/usd/docs/api/pipeline_8h.html#a589b8a95736d7cd9b0ce9f6ac9fc147c)

**Source Code Link**:
 - [The main function that discovers all UsdUtilsPipeline-related plugins](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usd/lib/usdUtils/pipeline.cpp#L258-L330)

**Plugin Sample Text**:

`plugInfo.json`
```json
{
    "Plugins": [
        {
            "Name": "Default Material Prim Container",
            "Type": "resource",
            "Info": {
                "UsdUtilsPipeline": {
                    "MaterialsScopeName": "SomePrimName"
                },
                "DefaultMaterialsScopeName": "SomeFallbackPrimName"
            }
        }
    ]
}
```

**Relevant Commands**:

TODO : do Python, too
```cpp
TfToken UsdUtilsGetMaterialsScopeName(const bool forceDefault);
```


### Set Up Variant Selection Fallbacks
There's already an example project for this plugin, located at
[concepts/variant_fallbacks](../concepts/variant_fallbacks). But, for
completion, let's also summarize the information here, too.

**Summary**: If a VariantSet has no selection, this plugin can control
which variant gets selected, if needed, by-default.

**Key**: UsdVariantFallbacks

**Related Links**:
 - [GetGlobalVariantFallbacks](https://graphics.pixar.com/usd/docs/api/class_usd_stage.html#a34d1d78fe8e31f0ba439d2265d694af5)
 - [SetGlobalVariantFallbacks](https://graphics.pixar.com/usd/docs/api/class_usd_stage.html#addaffc14d334e5cb1e3a90c02fadcaf6)


**Source Code Link**:
 - [pxr/usr/lib/stage.cpp](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usd/lib/usd/stage.cpp#L183-L222)

**Plugin Sample Text**:
```json
{
    "Plugins": [
        {
			"Name": "Variant Set Fallbacks",
			"Type": "resource",
            "Info": {
				"UsdVariantFallbacks": {
					"some_variant_set_name": ["possible_fallback_1", "possible_fallback_2", "possible_fallback_3", "foo", "bar"]
				}
            }
        }
    ]
}
```

**Relevant Commands**:

TODO : Do C++
```python
# Set variant fallbacks explicitly (this will override any plugInfo.json fallbacks)
Usd.Stage.SetGlobalVariantFallbacks({"some_variant_set_name": ["foo", "bar"]})  # Must be done before creating a stage
Usd.Stage.GetGlobalVariantFallbacks()
```


#### Set Up Variant Selection Export Policies
There's already an example project for this plugin, located at
[guides/registered_variant_selection_export_policies](../guides/registered_variant_selection_export_policies/README.md).
But, for completion, let's also summarize the information here, too.

**Summary**: Decide which USD VariantSet is allowed to be written to disk and under what conditions

**Description**: This plugin doesn't appear to do anything at the API
level. It seems to be more like a reference for tools to use on-export
to decide how to deal with VariantSets. USD uses this plugin in a number
of places, mainly in Katana and Maya's translator plugins.

**Key**: RegisteredVariantSets

**Related Links**:
- [UsdUtilsGetRegisteredVariantSets](https://graphics.pixar.com/usd/docs/api/pipeline_8h.html#af8c5904ce00b476edc137bb4ae0e114d)

**Source Code Link**:
 - [The part of UsdUtilsPipeline that discovers VariantSet selection export policies](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usd/lib/usdUtils/pipeline.cpp#L135-L185)

**Plugin Sample Text**:

`plugInfo.json`
```json
{
    "Plugins": [
        {
            "Name": "Variant Selection Export Policies",
            "Type": "resource",
            "Info": {
                "UsdUtilsPipeline": {
                    "RegisteredVariantSets": {
                        "some_variant_set": {
                            "selectionExportPolicy": "never"
                        },
                        "standin": {
                            "selectionExportPolicy": "never"
                        }
                    }
                }
            }
        }
    ]
}
```

**Relevant Commands**
TODO : Do Python, too
```cpp
const std::set<UsdUtilsRegisteredVariantSet>& UsdUtilsGetRegisteredVariantSets();
```


### Subclass Your Own Kind
**Summary**: Create a custom Kind by using one of USD's existing Kinds
as a base class.

**Key**: Kinds

**Related Links**:
 - [Extending the KindRegistry](https://graphics.pixar.com/usd/docs/api/kind_page_front.html#kind_extensions)

**Source Code Link**:
 - [pxr/usd/lib/kind/registry.cpp](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usd/lib/kind/registry.cpp#L174-L220)

**Plugin Sample Text**:

`plugInfo.json` (This was copy/pasted from [pxr/usd/lib/kind/testenv/testKindRegistry/lib/python/plugInfo.json](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usd/lib/kind/testenv/testKindRegistry/lib/python/plugInfo.json#L1-L19))
```json
{
    "Plugins": [
        {
            "Type": "python",
            "Name": "TestKindModule",
            "Info": {
                "Kinds": {
                    # Add "test_model_kind" as a kind of model.
                    "test_model_kind": {
                        "baseKind": "model"
                    },
                    # Add "test_root_kind" as a root kind.
                    "test_root_kind": {
                    }
                }
            }
        }
    ]
}
```

Important: It's highly recommended to inherit from an existing Kind,
rather than create a new root kind. USD traversals use predicate flags
to quickly get models. Custom root kinds can still be traversed normally
but it will be much slower. It's faster to inherit from a model Kind and
use UsdPrimRange like normal. You can still make a root kind of course,
it's just not recommended.
[Source conversation here](https://groups.google.com/forum/#!searchin/usd-interest/custom$20kind|sort:date/usd-interest/J_tLjVaaePM/HeIp47EzAwAJ).


**Relevant Commands**:
```cpp
UsdPrimRange::Stage(const UsdStagePtr &stage, const Usd_PrimFlagsPredicate &predicate);
UsdPrimRange::UsdPrimRange(Usd_PrimDataConstPtr begin, Usd_PrimDataConstPtr end, const SdfPath& proxyPrimPath, const Usd_PrimFlagsPredicate &predicate = UsdPrimDefaultPredicate);
```


### Extend Metadata
There's already an example project for this plugin, located at
[concepts/plugin_metadata](../concepts/plugin_metadata). But, for
completion, let's also summarize the information here, too.

**Summary**: Registry new metadata types so you can add your own custom metadata onto layers, attributes, prims, and more.

**Key**: SdfMetadata

**Related Links**:
- [A very detailed description of how to extend metadata](https://graphics.pixar.com/usd/docs/api/sdf_page_front.html#sdf_plugin_metadata)
- [Object Model and How the Classes Work Together](https://graphics.pixar.com/usd/docs/api/_usd__page__object_model.html)

**Source Code Link**:
 - [Where metadata is extended](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usd/lib/sdf/schema.cpp#L1570-L1742)

**Plugin Sample Text**:

`plugInfo.json`
```json
{
    "Plugins": [
        {
			"Name": "Plugin double extension",
			"Type": "resource",
            "Info": {
                "SdfMetadata": {
                    "another_metadata": {
                        "type": "double[]",
                        "appliesTo": "layers",
						"default": [5.0, 13.0]
                    },
                    "my_custom_double": {
                        "type": "double",
                        "appliesTo": "prims",
						"default": 12.0
                    }
                }
            }
        }
    ]
}
```

**Relevant Commands**:

TODO : Do Python

```cpp
TfToken SdfSchemaBase::SpecDefinition::GetMetadataFieldDisplayGroup(const TfToken& name) const
TfTokenVector SdfSchemaBase::SpecDefinition::GetMetadataFields() const;
bool SdfSchemaBase::SpecDefinition::IsMetadataField(const TfToken& name) const;
const VtValue& SdfSchemaBase::GetFallback(const TfToken &fieldKey) const;
const VtValue& SdfSpec::GetFallbackForInfo( const TfToken & key ) const
std::vector<TfToken> SdfSpec::GetMetaDataInfoKeys() const;
```


## TODO unsorted
This repository already covers a
hdxPrman
 resources/shaders (path)


RMAN_RIXPLUGINPATH
 - all paths


std::string rmantree = TfGetenv("RMANTREE");
 - lib/plugins/Args



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
