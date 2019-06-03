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
cd {some_concept_cpp_folder}
mkdir build
cd build
cmake ..
make
./run_it
```

## Python
Python modules can always run using `python name_of_module.py`


## Studying
This repository exists as source-code reference. That said, if you want
to treat as if this is a library of tutorials, here's the recommended
viewing order:

[add_comment](concepts/add_comment)

[set_kind](concepts/set_kind)

[specializes](concepts/specializes)

[asset_info](concepts/asset_info)

[world_bounding_box](concepts/world_bounding_box)

[variant_set_in_stronger_layer](concepts/variant_set_in_stronger_layer)

[variant_set_production_shot](concepts/variant_set_production_shot)

[purposes](concepts/purposes)

[orphaned_over](concepts/orphaned_over)

[enable_debugging](concepts/enable_debugging)

[value_clips](concepts/value_clips)

[caching](concepts/caching)

[multi_payload](concepts/multi_payload)

[notices](concepts/notices)

[notice_send](concepts/notice_send)

[mesh_with_materials](concepts/mesh_with_materials)


## Roadmap
See [This wiki page](https://github.com/ColinKennedy/USD-Cookbook/wiki/road-map)
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
- USD 19.05
