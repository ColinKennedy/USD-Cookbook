This repository is a collection of simple USD projects. Each project
shows off a single feature or group of USD features.


## Structure summary

This repository is split into six categories

- Features
- Concepts
- Tricks
- Plugins
- Tools
- References

**Features** highlight a single class or set of functions for working in USD.

**Concepts** take features explained in Features and extends them to real-world examples.

**Tricks** are simple, isolated ideas using USD Features.

**Plugins** show how to customize USD to suit your pipeline.

**Tools** are miscellaneous scripts that are built to do a specific task, with USD.

**References** are useful pages for finding more information about USD and how to interact with it in your projects.

Every project in this repository will show how to work in Python, C++,
and USDA wherever possible.


## How to view
If a concept folder is trying to show off a USD feature but it takes a
lot of code then the top-level README.md file is there to summarize the
important bits. It may also refer to other resources for where to read
more.

Lastly, source-code files may contain explanations for what is shown.
Each of these lines is marked with `XXX`.


## How to build
### C++
Unless a C++ project has specific instructions, every project compiles
and executes using the following commands:

```bash
cd {some_concept_cpp_folder}/build
USD_INSTALL_ROOT=/wherever/you/installed/USD/to cmake ..
make
./run_it
```

`USD_INSTALL_ROOT` typically defaults to `/usr/local/USD`
on Linux but your location may vary.
See [USD's build documentation](https://github.com/PixarAnimationStudios/USD#3-run-the-script) for details.


### Python
Python modules can always run using `python name_of_module.py`


## Sections
Here are links of a recommended viewing order for every project in this repository.


### Features

[Adding comments to USD files](features/add_comment)

[SetKind onto UsdPrim](features/set_kind)

[specializes composition arc](features/specializes)

[Using Prim AssetInfo](features/asset_info)

[Defining customizable userProperties](features/userProperties)

[Edit Targets](features/edit_targets)

[Value resolution caching](features/value_caching)

[Computing bounding boxes, using UsdGeomImageable and UsdGeomBBoxCache](features/world_bounding_box)

[Pixar's specializes example](features/specializes_glossary_example)

[Using "purposes" on UsdPrim objects](features/purposes)

[UsdResolveInfo - Finding where opinions come from](features/usd_resolve_info)

[Enable debugging messages and write your own](features/enable_debugging)

[Profiling USD stages](features/profiling_usd.md)

[How to use Value Clips](features/value_clips)

[Setting Time Varying Attributes With Sdf](features/time_varying_attributes_sdf)

[SdfChangeBlock - Efficient USD authoring](features/sdf_change_block)

[SdfBatchNamespaceEdit and SdfNamespaceEdit - Efficient USD authoring](features/batch_namespace_edit)

[UsdStageCache - caching USD stages](features/caching)

[TfNotice - Run functions when a stage changes, using callbacks](features/notices)

[TfNotice - Send your own custom callbacks](features/notice_send)


### Concepts

[Valid Model Hierarchies](concepts/valid_model_hierarchies)

[Understanding VariantSets](concepts/variant_set_understanding)

[Overriding VariantSets](concepts/variant_set_in_stronger_layer)

[Use weaker layers to modify stronger layers](concepts/use_weaker_layers_to_modify_stronger_layers)

[How to uniquify an instanced UsdPrim](concepts/uniquify_an_instance)

[UsdRelationship Forwarding](concepts/relationship_forwarding)

[Using VariantSets in a production scenario](concepts/variant_set_production_shot)

[A practical example of the "specializes" composition arc](concepts/specializes_a_practical_example)

[The "specializes" composition arc as a fallback mechanism](concepts/specializes_as_a_fallback_mechanism)

[Reference a Prim in the current SdfLayer](concepts/reference_into_prim)

[How to find "Orphaned" overs](concepts/orphaned_over)

[A mesh with a material](concepts/mesh_with_materials)

[Asset composition arcs - how subLayers, references, and payloads work together](concepts/asset_composition_arcs.md)


### Tricks

[Printing and modifiying prims using the C++ STL](tricks/stl_iteration)

[Custom traversals with boost](tricks/stl_iteration2)

[Variant auto-selections - Using VariantSets to modify other VariantSets](tricks/variant_set_auto_selections )

[Copy opinions from a VariantSet onto another Prim](tricks/copy_variant_set_to_prim)

[Find An Attribute's Source](tricks/attribute_source_check)

[Find a Prim's bound material (includes collections API)](tricks/bound_material_finder)

[2-pass exporting - Export USD stages 100x faster](tricks/fast_export)

[Flatten a USD layer stack](tricks/flatten_layer_stack)

[Multi-payloads - Yes, you can have more than one](tricks/multi_payload)

[Getting Prims through VariantSets](tricks/get_sdf_prim_path)


### Plugins

[usdview_auto_reloader - Update layers in usdview automatically](plugins/usdview_auto_reloader)

[usdview_root_loader - Recursively load / unload Prim payloads](plugins/usdview_root_loader)

[usdview_purpose_swap - Change between proxy and render purposes with a single button](plugins/usdview_purpose_swap)

[usdview_copy_camera - Make a prim in usdview to represent the current view](plugins/usdview_copy_camera)

[VariantSet fallback selections](plugins/variant_fallbacks)

[VariantSet selection export polices](plugins/registered_variant_selection_export_policies)

[Adding custom metadata](plugins/plugin_metadata)

[Custom USD schemas](plugins/custom_schemas_with_python_bindings)

[A custom ArResolver plugin](tools/custom_resolver)


### Tools

[usd_searcher - A command-line tool for searching USD files](tools/usd_searcher)

[Exporting UsdSkel from scratch](tools/export_usdskel_from_scratch)


### References

[extentsHint and bounding boxes](references/extents_hint_and_bounding_boxes)

[Link Python Documentation To USD's Documentation](references/link_to_the_api_documentation)

[Understanding usdview](references/usdview_style_documentation)

[The USD supported plugin mastersheet](references/working_with_plugins.md)

[Where to find more resources](references/where_to_find_resources.md)


## Studying

There's also Anki deck for this repository, which you can download
[by clicking here](https://drive.google.com/file/d/1qx8N9wwL2ufviuWcQrY3zT2S6GN6nrg7/view?usp=sharing)


## Roadmap
See [This wiki page](https://github.com/ColinKennedy/USD-Cookbook/wiki)
for a list of planned topics that will be added in the future.


## Contributing
This repository is a constant WIP. If there's something that you'd like
to see written about, please suggest it as an issue so that I / others
can pick it up and work on it. Also, if you have something that you'd
like to contribute, please make a PR. Submissions are welcome!


## Disclaimer
But note: This repository may not actually show the best way to do
things in USD. It's just a collection of (my) personal findings. Also,
as Pixar comes out with new USD releases and learning resources, this
information may become out-of-date. Always prefer primary guides and
documentation over anything that you see here.


## Final Note
Tested with:
- CentOS 7.6
- USD 19.07
- cmake version 3.13.4
- make 3.82
- g++ 8.3.0
