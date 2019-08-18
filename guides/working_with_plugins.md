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
USD has two main methods of querying plugins. USD either iterates over
all plugins and searches for a specific key or it searches for plugins
that inherit from a known USD type. We'll call these "By-Name" Plugins
and "By-Type" Plugins, respectively.

Skip to [How To Find Where To Look](#How-To-Find-Where-To-Look) to find
out how to search these definitions by yourself.


## Table Of Contents
Here's a quick list of both styles that USD uses to query plugins.


### "By-Name" Plugins
- UsdGeomMetrics - [Set Your Default Scene Up Axis](#Set-Your-Default-Scene-Up-Axis)
- UsdColorConfigFallbacks - [Set Up Color Management](#Set-Up-Color-Management)
- UsdUtilsPipeline - [UsdUtilsPipeline](#UsdUtilsPipeline)
    - MaterialsScopeName - [Set Up A Registered Material Prim](#Set-Up-A-Registered-Material-Prim)
    - PrimaryCameraName - [Set Up A Default Camera Name](#Set-Up-A-Default-Camera-Name)
    - RegisteredVariantSets - [Set Up Variant Selection Export Policies](#Set-Up-Variant-Selection-Export-Policies)
- DefaultMaterialsScopeName - [Set Up A Registered Material Prim](#Set-Up-A-Registered-Material-Prim)
- DefaultPrimaryCameraName - [Set Up A Default Camera Name](#Set-Up-A-Default-Camera-Name)
- UsdVariantFallbacks - [Set Up Variant Selection Fallbacks](#Set-Up-Variant-Selection-Fallbacks)


### "By-Type" Plugins
- Kinds - [Subclass Your Own Kind](#Subclass-Your-Own-Kind)
- SdfMetadata - [Extend Metadata](#Extend-Metadata)
- SdfFileFormat - [Register A File Format](#Register-A-File-Format)
- ArResolver - [Adding A Custom Resolver](#Adding-A-Custom-Resolver)
- ArPackageResolver - [Adding a Package Resolver](#Adding-A-Package-Resolver)
- UsdImagingPrimAdapter - [Pair A usdImaging Adapter Class With A Usd Prim Type](#Pair-A-usdImaging-Adapter-Class-With-A-Usd-Prim-Type)
- ShaderResources - [Add Shader Resources To Hydra](#Add-Shader-Resources-To-Hydra)
- UsdSchemaBase - [Create A Custom Schema](#Create-A-Custom-Schema)
- NdrParserPlugin - [Encode Shaders As USD Prims](#Encode-Shaders-As-USD-Prims)
- GlfImage - [OpenGL USD Types](#OpenGL-USD-Types)


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

**Relevant Commands**:
```cpp
SdfSchema::GetInstance().GetFallback(UsdGeomTokens->upAxis)
TfToken UsdGeomGetFallbackUpAxis();
```

```python
from pxr import Usd, UsdGeom
UsdGeom.GetFallbackUpAxis()

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

```cpp
SdfAssetPath UsdStage::GetColorConfiguration() const;
TfToken UsdStage::GetColorManagementSystem() const;
UsdStage::SetColorConfiguration(const SdfAssetPath &colorConfig) const;
void UsdStage::SetColorManagementSystem(const TfToken &cms) const;
```

```python
Usd.Stage.GetColorConfiguration()
Usd.Stage.GetColorManagementSystem()
Usd.Stage.SetColorConfiguration()
Usd.Stage.SetColorManagementSystem()
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
```cpp
TfToken UsdUtilsGetPrimaryCameraName(const bool forceDefault);
```

```python
UsdUtils.GetPrimaryCameraName()
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

```cpp
TfToken UsdUtilsGetMaterialsScopeName(const bool forceDefault);
```

```python
UsdUtils.GetMaterialsScopeName()
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

```cpp
static PcpVariantFallbackMap GetGlobalVariantFallbacks();
static void SetGlobalVariantFallbacks(const PcpVariantFallbackMap &fallbacks);
```

```python
Usd.Stage.GetGlobalVariantFallbacks()
# Set variant fallbacks explicitly (this will override any plugInfo.json fallbacks)
Usd.Stage.SetGlobalVariantFallbacks({"some_variant_set_name": ["foo", "bar"]})  # Must be done before creating a stage
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
```cpp
const std::set<UsdUtilsRegisteredVariantSet>& UsdUtilsGetRegisteredVariantSets();
```

```python
UsdUtils.GetRegisteredVariantSets()
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

```cpp
TfToken SdfSchemaBase::SpecDefinition::GetMetadataFieldDisplayGroup(const TfToken& name) const
TfTokenVector SdfSchemaBase::SpecDefinition::GetMetadataFields() const;
bool SdfSchemaBase::SpecDefinition::IsMetadataField(const TfToken& name) const;
const VtValue& SdfSchemaBase::GetFallback(const TfToken &fieldKey) const;
const VtValue& SdfSpec::GetFallbackForInfo( const TfToken & key ) const
std::vector<TfToken> SdfSpec::GetMetaDataInfoKeys() const;
TfToken GetMetaDataDisplayGroup(TfToken const &key) const;
```

```python
Sdf.Spec.GetFallbackForInfo()
Sdf.Spec.GetMetadataInfoKeys()
Sdf.Spec.GetMetadataDisplayGroup()
```

### Register A File Format
**Summary**: Add a file format so that it can be natively converted to
and from USD.

**Key**: SdfFileFormat

**Description**:
This plugin takes a dictionary with a number of allowed keys:

- _bases_ - The registered File Format name that this plugin inherits. It
must inherit from a type that inherits from SdfFileFormat or it must
inherit SdfFileFormat, directly.
- extensions - list of strings. It's the filetype extensions that can be
processed by this formatter
- _formatId_ - string - A unique ID that is used to find this file format
plugin. Usually this value matches the extension of the file format. But
it's not a requirement.
- _primary_ - If this file format plugin should be the preferred plugin
for its extensions
- _target_ - To be honest, I'm not really sure what this is for. Maybe
it's the file format that this registered file format is meant to be
converted into? All of the examples online that I see convert to either
"usd" or "sdf", which seems to support that idea.

**Related Links**:
 - [A brief mention about custom file formats](https://graphics.pixar.com/usd/docs/api/sdf_page_front.html#sdf_fileFormatPlugin)

**Source Code Link**:
 - [pxr/usd/lib/sdf/fileFormatRegistry.cpp](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usd/lib/sdf/fileFormatRegistry.cpp#L169-L428)
 - [plugin tokens definition](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usd/lib/sdf/fileFormatRegistry.cpp#L43-L48)

**Plugin Sample Text**:

`plugInfo.json` (This was copied from [USD's usd module](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usd/lib/usd/plugInfo.json#L144-L155))
```json
{
    "Plugins": [
        {
            "Info": {
                "Types": {
                    # ...

                    "UsdUsdcFileFormat": {
                        "bases": [
                            "SdfFileFormat"
                        ],
                        "displayName": "USD Crate File Format",
                        "extensions": [
                            "usdc"
                        ],
                        "formatId": "usdc",
                        "primary": true,
                        "target": "usd"
                    }

                    # ...
                }
            }
        }
    ]
}
```

**Relevant Commands**:

[Everything from the FileFormatRegistry class](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usd/lib/sdf/fileFormatRegistry.h#L56-L75)


### Adding A Custom Resolver
This plugin has been covered by the
[custom_resolver](../concepts/custom_resolver) project in this
repository. But, for completion, let's also summarize the information
here, too.

**Summary**: A resolver plugin is used to convert any string to a
path on-disk. For example, USD Asset paths may be a totally arbitrary
string syntax, such as: "[foo][bar[bazz]??usda|v=001]". A custom
resolver's job is to convert that string into a path on-disk like
"/tmp/foo_folder/bar_bazz_v001.usda".

**Key**: ArResolver (any plugin that inherits this class)

**Related Links**:
 - [Implementing a Custom Resolver](https://graphics.pixar.com/usd/docs/api/ar_page_front.html#ar_implementing_resolver)
 - [ArDefaultResolver class reference](https://graphics.pixar.com/usd/docs/api/class_ar_default_resolver.html)

**Source Code Link**:
 - [pxr/usd/lib/ar/resolver.cpp](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usd/lib/ar/resolver.cpp#L104-L147)
 - [The code that sets USD's default resolver](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usd/lib/ar/resolver.cpp#L560-L593)

**Plugin Sample Text**:

`plugInfo.json` (Copied file from the generated results of [this custom resolver project](../concepts/custom_resolver))
```json
{
    "Plugins": [
        {
            "Info": {
                "Types": {
                    "URIResolver" : {
                        "bases": ["ArResolver"]
                    }
                }
            },
            "LibraryPath": "../libURIResolver.so",
            "Name": "URIResolver",
            "Type": "library"
        }
    ]
}
```
**Relevant Commands**:

```cpp
void ArSetPreferredResolver(const std::string& resolverTypeName);
ArResolver& ArGetResolver();
std::vector<TfType> ArGetAvailableResolvers();
```

```python
Ar.SetPreferredResolver()
Ar.GetResolver()
```


### Adding A Package Resolver
**Summary**: Like "Adding A Custom Resolver" but for USD package resolvers.

**Description**: There's not that much documentation about package resolvers. That
said, USD package resolvers are similar in concept to an asset
resolver but with the following differences:

 - You aren't supposed to instantiate package resolvers yourself. USD
 does this internally, for you. Always prefer ArGetResolver
 - The ArResolver class [converts a logical path (a string or URI) into a physical path](https://graphics.pixar.com/usd/docs/api/class_ar_resolver.html).
 - The ArPackageResolver class specifically handles "package"
 file formats like files with ".pack" extension. It is responsible
 for [resolving information about assets stored within that
 package](https://graphics.pixar.com/usd/docs/api/class_ar_package_resolv
 er.html)
 - In other words, ArPackageResolver resolves a subset of a file on
 disk (an asset within a package file) and ArResolver resolves a whole
 file, instead.

So the question is, how do you define a package resolver?
You do it the same way as an asset resolver, just with a different key.

**Key**: ArPackageResolver

**Related Links**:
 - [A required macro to registry a package resolver, AR_DEFINE_PACKAGE_RESOLVER](https://graphics.pixar.com/usd/docs/api/define_package_resolver_8h.html)
 - [ArPackageResolver - Read the Detailed Description Section](https://graphics.pixar.com/usd/docs/api/class_ar_package_resolver.html)
 - [ArResolver - Read the Detailed Description Section](https://graphics.pixar.com/usd/docs/api/class_ar_resolver.html)

**Source Code Link**:
 - [pxr/usd/lib/ar/resolver.cpp](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usd/lib/ar/resolver.cpp#L629-L695)

**Plugin Sample Text**:

`plugInfo.json` (Copied from [The ArPackageResolver documentation](https://graphics.pixar.com/usd/docs/api/class_ar_package_resolver.html))
```json
{
    "Plugins": [
        {
            "Info": {
                "Types" : {
                    "CustomPackageResolver" : {
                        "bases": [ "ArPackageResolver" ],
                        "extensions": [ "pack" ]
                    }
                }
            },
            ...
        },
        ...
    ]

}
```


### Pair A usdImaging Adapter Class With A Usd Prim Type
**Summary**: Add a usdImaging Adapter Type for a given USD Prim type.

**Description**: This plugin has 3 main keys:
- _bases_ - list of strings - The USD adapter class that this adapter is based off of.
- _isInternal_ - bool - External adapters can be turned on and off
depending on if the `USDIMAGING_ENABLE_PLUGINS` environment variable
is enabled. This environment variable is mainly used for debugging
purposes. Internal adapters stay on.
- _primTypeName_ - string - The USD Prim type that the adapter is for

**Key**: UsdImagingPrimAdapter (must be derived from this class)

**Related Links**:
 - [Explanation for "isInternal"](https://graphics.pixar.com/usd/docs/api/class_usd_imaging_adapter_registry.html#a44227db6636d587bcd6500275f9de4f6)

**Source Code Link**:
 - [pxr/usdImaging/lib/usdImaging/adapterRegistry.cpp](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usdImaging/lib/usdImaging/adapterRegistry.cpp#L62-L128)

**Plugin Sample Text**

`plugInfo.json` (Copied from [pxr/usdImaging/lib/usdVolImaging/plugInfo.json](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usdImaging/lib/usdVolImaging/plugInfo.json))
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

**Relevant Commands**:

[Everything in the UsdImagingAdapterRegistry class](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usdImaging/lib/usdImaging/adapterRegistry.h#L53-L93)


### Add Shader Resources To Hydra
**Summary**: A way to add additional shader definitions to Hydra.

**Key**: [[Info][ShaderResources]](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/imaging/lib/hdx/plugInfo.json#L4-L6)

**Source Code Link**:
 - [pxr/imaging/lib/hio/glslfx.cpp](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/imaging/lib/hio/glslfx.cpp#L101-L120)

**Plugin Sample Text**:

`plugInfo.json` (Copied from [pxr/imaging/lib/hdx/plugInfo.json](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/imaging/lib/hdx/plugInfo.json))
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

**Relevant Commands**:

[Anything in the ShaderResourceRegistry class](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/imaging/lib/hio/glslfx.cpp#L88-L94)


### Create A Custom Schema
**Summary**: Define a USD type to use in your C++ / Python projects.
This system is the same as the one that USD itself uses for most of its
class types.

**Key**: UsdSchemaBase

**Related Links**:
 - [UsdSchemaBase](https://graphics.pixar.com/usd/docs/api/class_usd_schema_base.html)
 - [UsdSchemaRegistry](https://graphics.pixar.com/usd/docs/api/class_usd_schema_registry.html)
 - [API Schema](https://graphics.pixar.com/usd/docs/USD-Glossary.html#USDGlossary-APISchema)
 - [IsA Schema](https://graphics.pixar.com/usd/docs/USD-Glossary.html#USDGlossary-IsASchema)
 - [UsdGeomComputeExtentFunction](https://graphics.pixar.com/usd/docs/api/boundable_compute_extent_8h.html#a4564996409a8ce82ca1c8c7aa41a16ac)
 - [UsdGeomRegisterComputeExtentFunction. A function that must be defined to compute extents of USD types](https://graphics.pixar.com/usd/docs/api/boundable_compute_extent_8h.html#aba77ec2a17618b2a25980f0b644afc26)
 - [Working With Schema Classes](https://graphics.pixar.com/usd/docs/api/_usd__page__common_idioms.html#Usd_WorkingWithSchemas)

**Source Code Link**:
 - [The function that discovers all registered schemas](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usd/lib/usd/schemaRegistry.cpp#L169-L270)
 - [pxr/usd/lib/usdGeom/boundableComputeExtent.cpp](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usd/lib/usdGeom/boundableComputeExtent.cpp#L87-L134)

**Plugin Sample Text**:

```json
{
    "Plugins": [
        {
            "Info": {
                "Types": {
                    # ...

                    "UsdGeomCube": {
                        "alias": {
                            "UsdSchemaBase": "Cube"
                        },
                        "autoGenerated": true,
                        "bases": [
                            "UsdGeomGprim"
                        ],
                        "implementsComputeExtent": true
                    }

                    # ...
                }
            }
        }
    ]
}
```

**Relevant Commands**:

[Everything in the UsdSchemaRegistry class](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usd/lib/usd/schemaRegistry.h#L42-L267)


### Encode Shaders As USD Prims
The USD documentation is fairly extensive about this plugin so, instead
of re-iterating its points, links will be provided, below:

- [UsdShade Based Shader Definition](https://graphics.pixar.com/usd/docs/api/usd_shade_page_front.html#UsdShadeShaderDefinition)
- [NdfParserPlugin](https://graphics.pixar.com/usd/docs/api/class_ndr_parser_plugin.html)
- [UsdShadeShaderDefUtils::GetNodeDiscoveryResults](https://graphics.pixar.com/usd/docs/api/class_usd_shade_shader_def_utils.html#a769e7fcf038cb078b2419735759630be)
- [UsdShadeShaderDefParserPlugin](https://graphics.pixar.com/usd/docs/api/class_usd_shade_shader_def_parser_plugin.html)



### OpenGL USD Types
**Summary**: To be honest, I'm not read up enough on OpenGL and how it
is consumed by USD to discuss this particular plugin. Maybe this section
can be filled in once someone with experience sees this.

Judging from the `plugInfo.json` file, it looks like this plugin is
used to define classes to consume texture file types for viewport
rendering. It has some kind of a ranked ordering, using "precedence" as
the ordering key. But this is all just a guess.

**Key**: GlfImage

**Related Links**:
 - [GlfRankedTypeMap](https://graphics.pixar.com/usd/docs/api/class_glf_ranked_type_map.html)
 
**Source Code Link**:
 - [pxr/imaging/lib/glf/rankedTypeMap.h](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/imaging/lib/glf/rankedTypeMap.h#L94-L179)

**Plugin Sample Text**:

`plugInfo.json` (Copied from [plugInfo.json](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/imaging/lib/glf/plugInfo.json))
```json
{
    "Plugins": [
        {
            "Info": {
                "ShaderResources": "shaders",
                "Types": {                                                                  
                    "Glf_OIIOImage" : {
                        "bases": ["GlfImage"],
                        "imageTypes": ["bmp", "exr", "jpg", "png", "tif", "zfile", "tx"],
                        "precedence": 0 
                    },
                    "Glf_StbImage" : {
                        "bases": ["GlfImage"],
                        "imageTypes": ["bmp", "jpg", "png", "tga", "hdr"],
                        "precedence": 2
                    },
                    "GlfPtexTexture" : {
                        "bases": ["GlfTexture"],
                        "textureTypes": ["ptx", "ptex"],
                        "precedence": 1
                    },
                    "GlfUVTexture" : {
                        "bases": ["GlfBaseTexture"],
                        "textureTypes": ["*"],
                        "precedence": 0
                    }
                }
            },
            "LibraryPath": "@PLUG_INFO_LIBRARY_PATH@",
            "Name": "glf",
            "ResourcePath": "@PLUG_INFO_RESOURCE_PATH@",
            "Root": "@PLUG_INFO_ROOT@",
            "Type": "library"
        }
    ]
}
```


## How To Find Where To Look
Like mentioned in past sections, there's no one way of finding out
how USD uses its own plugins. At best, you can query what plugins are
currently being used and work backwards from there.

That said, it's not all hopeless. Here's a few methods for searching that were
used to write this article

### Search for plugInfo.json files
USD's plugin system relies on these files so it makes sense that we can find
pretty much any plugin under the sun just by searching for those files

Linux:
```
git clone https://github.com/PixarAnimationStudios/USD && cd USD
find -type f -name "plugInfo.json"
```

Plugins are typically "found" in USD by either a special key under "Info", like
"UsdUtilsPipeline"

```json
{
    "Plugins": [
        {
            "Name": "Default Camera Name",
            "Type": "resource",
            "Info": {
                "UsdUtilsPipeline": {
                    # ...
                }
            }
        }
    ]
}
```

or USD will search for a specific type, using the "bases" key of a plugin, like this

```json
{
    "Plugins": [
        {
            "Info": {
                "Types": {
                    "URIResolver" : {
                        "bases": ["ArResolver"]
                    }
                }
            }
        }
    ]
}
```

In both cases, once you see a plugInfo.json, you can read the keys
under "Info" or search for PluginRegistry for methods that require
`ArResolver` and you're pretty likely to find exactly where that
`plugInfo.json` is meant to be used.


### Search for uses of registry classes
Searching C++ code for phrases like `GetAllPlugins`,
`GetAllDerivedTypes`, and really any public
member function in [the PlugRegistry class](https://graphics.pixar.com/usd/docs/api/class_plug_registry.html)
will find many plugins, right away.

The only thing to keep in mind with this search method is that there are
multiple registries in USD. There's:

 - [KindRegistry](https://graphics.pixar.com/usd/docs/api/class_kind_registry.html)
 - [PlugRegistry](https://graphics.pixar.com/usd/docs/api/class_plug_registry.html)
 - [Sdf_FileFormatRegistry](https://graphics.pixar.com/usd/docs/api/file_format_registry_8h.html)
 - [ShaderResourceRegistry](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/imaging/lib/hio/glslfx.cpp#L88-L94)
 - [UsdImagingAdapterRegistry](https://graphics.pixar.com/usd/docs/api/class_usd_imaging_adapter_registry.html)

And possibly others that just aren't listed here yet.

So keep that in mind while searching. If you search by-registry and
can't find what you're looking for, consider the idea that you may need
to be looking for a different registry.


### Search Online
There's a USD repository called
[parallax/ar-export](https://github.com/parallax/ar-export/tree/master/libs/USDPython/USD/usd)
that has a list of many `plugInfo.json` file examples that is a decent
reference. There's also repositories from VFX companies, like Luma and
RodeoFX. Many of those repositories will have example plugin uses.
