This repository is a collection of simple USD projects. Each project
shows off a single feature or group of USD features.


## Structure summary

```
Folders
- concepts/
 - {CONCEPT_NAME}
  - README.md
  - cpp/
  - python/
  - usda/
- guides/
- tricks/
```

Each USD feature is in the "concepts" folder. Most features have a C++,
python, and USDA project folder where you can see how to author that
feature in each representation and how it actually looks when it gets
written in USD.


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


## Folder Explanation
- `concepts` is where you'll find simple, single features shown by-example.
It will have C++, Python, and USDA example projects (whenever possible).
If you're the type that makes flashcards, you'll get the most mileage
here.
- `guides` contains articles of ideas and references that help a user
learn USD.
- `tricks` is a mixed bag of situations that come up in production and
general proof-of-concepts on how to do certain operations in USD. This
folder has projects that are too complex or niche to fit in `concepts`.
There's no defined structure for this folder.


## Studying
This repository exists mainly as a reference for USD source-code. That
said, if you want to treat as if this is a library of tutorials, here's
a recommended viewing order:

[add_comment](concepts/add_comment)

[set_kind](concepts/set_kind)

[specializes](concepts/specializes)

[uniquify_an_instance](tricks/uniquify_an_instance)

[asset_info](concepts/asset_info)

[userProperties](concepts/userProperties)

[world_bounding_box](concepts/world_bounding_box)

[relationship_forwarding](concepts/relationship_forwarding)

[variant_set_in_stronger_layer](tricks/variant_set_in_stronger_layer)

[variant_set_production_shot](tricks/variant_set_production_shot)

[specializes_glossary_example](tricks/specializes_glossary_example)

[specializes_a_practical_example](tricks/specializes_a_practical_example)

[specializes_as_a_fallback_mechanism](tricks/specializes_as_a_fallback_mechanism)

[purposes](concepts/purposes)

[reference_into_prim](tricks/reference_into_prim)

[stl_iteration](tricks/stl_iteration)

[stl_iteration2](tricks/stl_iteration2)

[orphaned_over](tricks/orphaned_over)

[variant_set_auto_selections](tricks/variant_set_auto_selections )

[copy_variant_set_to_prim](concepts/copy_variant_set_to_prim)

[enable_debugging](concepts/enable_debugging)

[profiling](guides/profiling_usd.md)

[usdview_auto_reloader](tricks/usdview_auto_reloader)

[variant_fallbacks](concepts/variant_fallbacks)

[registered_variant_selection_export_polices](guides/registered_variant_selection_export_polices)

[plugin_metadata](concepts/plugin_metadata)

[custom_resolver](concepts/custom_resolver)

[bound_material_finder](concepts/bound_material_finder)

[fast_export](tricks/fast_export)

[flatten_layer_stack](tricks/flatten_layer_stack)

[value_clips](concepts/value_clips)

[mesh_with_materials](concepts/mesh_with_materials)

[sdf_change_block](concepts/sdf_change_block)

[batch_namespace_edit](concepts/batch_namespace_edit)

[caching](concepts/caching)

[multi_payload](concepts/multi_payload)

[asset_composition_arcs](guides/asset_composition_arcs.md)

[export_usdskel_from_scratch](tricks/export_usdskel_from_scratch)

[notices](concepts/notices)

[notice_send](concepts/notice_send)

[where_to_find_resources](guides/where_to_find_resources.md)

[working_with_plugins](guides/working_with_plugins.md)


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
