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

Features highlight a single class or set of functions for working in USD.
Concepts take features explained in Features and extends them to real-world examples.
Tricks are simple, isolated ideas using USD Features.
Plugins show how to customize USD to suit your pipeline.
Tools are miscellaneous scripts that are built to do a specific task, with USD.
References are articles that show where to find more information.

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

[add_comment](concepts/add_comment)

[set_kind](concepts/set_kind)

[specializes](concepts/specializes)

[asset_info](concepts/asset_info)

[userProperties](concepts/userProperties)

[value_caching](concepts/value_caching)

[world_bounding_box](concepts/world_bounding_box)

[specializes_glossary_example](tricks/specializes_glossary_example)

[purposes](concepts/purposes)

[usd_resolve_info](concepts/usd_resolve_info)

[enable_debugging](concepts/enable_debugging)

[profiling](guides/profiling_usd.md)

[value_clips](concepts/value_clips)

[sdf_change_block](concepts/sdf_change_block)

[batch_namespace_edit](concepts/batch_namespace_edit)

[caching](concepts/caching)

[notices](concepts/notices)

[notice_send](concepts/notice_send)


### Concepts

[uniquify_an_instance](tricks/uniquify_an_instance)

[relationship_forwarding](concepts/relationship_forwarding)

[variant_set_in_stronger_layer](tricks/variant_set_in_stronger_layer)

[variant_set_production_shot](tricks/variant_set_production_shot)

[specializes_a_practical_example](tricks/specializes_a_practical_example)

[specializes_as_a_fallback_mechanism](tricks/specializes_as_a_fallback_mechanism)

[reference_into_prim](tricks/reference_into_prim)

[orphaned_over](tricks/orphaned_over)

[mesh_with_materials](concepts/mesh_with_materials)

[asset_composition_arcs](guides/asset_composition_arcs.md)


### Tricks

[stl_iteration](tricks/stl_iteration)

[stl_iteration2](tricks/stl_iteration2)

[variant_set_auto_selections](tricks/variant_set_auto_selections )

[copy_variant_set_to_prim](concepts/copy_variant_set_to_prim)

[bound_material_finder](concepts/bound_material_finder)

[fast_export](tricks/fast_export)

[flatten_layer_stack](tricks/flatten_layer_stack)

[multi_payload](concepts/multi_payload)


### Plugins

[usdview_auto_reloader](tricks/usdview_auto_reloader)

[usdview_root_loader](tricks/usdview_root_loader)

[variant_fallbacks](concepts/variant_fallbacks)

[registered_variant_selection_export_polices](guides/registered_variant_selection_export_policies)

[plugin_metadata](concepts/plugin_metadata)

[custom_schemas_with_python_bindings](tricks/custom_schemas_with_python_bindings)


### Tools

[custom_resolver](concepts/custom_resolver)

[usd_searcher](tricks/usd_searcher)

[export_usdskel_from_scratch](tricks/export_usdskel_from_scratch)


### References

[usdview_style_documentation](guides/usdview_style_documentation)

[where_to_find_resources](guides/where_to_find_resources.md)

[working_with_plugins](guides/working_with_plugins.md)


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
