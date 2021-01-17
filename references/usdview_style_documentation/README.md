**Update**
This page used to explain all the font / icons / etc of usdview. But
this page is unnecessary because usdview already has a way to show what
everything means.

To find out what a specific color or icon means, simply press the "?"
button in the lower-left corner of the widgets in usdview.

![usdview_legend](https://user-images.githubusercontent.com/10103049/104829527-a4664000-5829-11eb-80d9-d46d5afd4f49.gif)

After the "?", usdview will expand to show a legend which explains everything.

Prefer everything shown in usdview over anything you see here.


# Quick Explanation
Have you ever wondered what all the text colors, fonts, and icons in
usdview mean? The different combinations of data can be pretty complex.
This page will explain usdview's visuals, and how the USD API is used
to achieve them.

This page contains everything you need to know.


## A breakdown of usdview
`usdview` has lots rules for how its prim / property information is
displayed. To help make sense of it all, [This usdview_style_stage.usda
file](usdview_style_stage.usda) contains a simple stage for every single
color / font / icon that usdview uses.

That stage can be used as a reference while viewing the rest of this page.

```bash
usdview usdview_style_stage.usda
```

## Prims
### Prim Text Colors

|                                                       Name                                                        |               Description               |       Value        |    Location    |
|-------------------------------------------------------------------------------------------------------------------|-----------------------------------------|--------------------|----------------|
| ![Normal](https://user-images.githubusercontent.com/10103049/64095938-23caa080-cd15-11e9-9adf-338ea0175d6f.png)   | Neither an instance or a master         | rgb(227, 227, 227) | /SomePrim      |
| ![Instance](https://user-images.githubusercontent.com/10103049/64096068-7e63fc80-cd15-11e9-800a-42fe04e59a98.png) | An instanced Prim                       | rgb(135, 206, 250) | /InstancedItem |
| ![Master](https://user-images.githubusercontent.com/10103049/64096145-b10df500-cd15-11e9-9046-0a87b7fc36ec.png)   | A Prim which is used by instances       | rgb(118, 136, 217) | `/__Master_1`  |
| ![Has Arcs](https://user-images.githubusercontent.com/10103049/64096004-4eb4f480-cd15-11e9-83b6-619bb7f18849.png) | A Prim that contains 1+ Composition Arc | rgb(222, 158, 46)  | /Inherited     |



### Prim Fonts

|    Name     |  Style  |                                   Description                                   |   Location    |
|-------------|---------|---------------------------------------------------------------------------------|---------------|
| Abstract    | Normal  | A class Prim. Enable "Show" > "Abstract Prims (Classes)"                        | /SomeClass    |
| Defined     | Bold    | A normal Prim that will be in default traversals                                | /SomePrim     |
| `over` Prim | Italics | An undefined Prim (an Orphaned Over). Enable "Show" > "Undefined Prims (Overs)" | /OrphanedOver |



## Properties
### Property Text Colors

|                                                            Name                                                             |                         Description                          |       Value        |                Location                 |
|-----------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------|--------------------|-----------------------------------------|
| ![From Default](https://user-images.githubusercontent.com/10103049/64096828-7efd9280-cd17-11e9-89ac-19d3a48d362e.png)       | The property's default (non-time-sampled) value              | rgb(135, 206, 250) | /SomePrim.default_property              |
| ![From Time Sample](https://user-images.githubusercontent.com/10103049/64096862-93418f80-cd17-11e9-8ac2-e08dd94722a3.png)   | The value comes from an authored time value                  | rgb(177, 207, 153) | /SomePrim.time_samples_property         |
| ![From Type Fallback](https://user-images.githubusercontent.com/10103049/64097222-840f1180-cd18-11e9-87d5-c4e05474aaf0.png) | No value was found so USD used the Prim's type as a fallback | rgb(222, 158, 46)  | /SomePrim.visibility                    |
| ![From Value Clip](https://user-images.githubusercontent.com/10103049/64096895-b10ef480-cd17-11e9-901a-1570ed5f6dcf.png)    | The value resolved to a stitched clip layer                  | rgb(230, 150, 230) | /PrimWithValueClips.inManifestAndInClip |
| ![None](https://user-images.githubusercontent.com/10103049/64097313-ca647080-cd18-11e9-8c3d-87e203f9e9cb.png)               | No value could be found                                      | rgb(140, 140, 140) | /SomePrim.xformOpOrder                  |


### Property Type Column
In `usdview`, the "Type" Column can contain an icon and/or
text. Most of the time, you'll only see an icon like
![usd-cmp-icon.png](https://user-images.githubusercontent.com/10103049/64098197-1adccd80-cd1b-11e9-8464-4f726472ab47.png),
![usd-attr-plain-icon.png](https://user-images.githubusercontent.com/10103049/64097798-064c0580-cd1a-11e9-8b6c-4d4d47ec3928.png), or
![usd-rel-plain-icon.png](https://user-images.githubusercontent.com/10103049/64097833-1d8af300-cd1a-11e9-9086-1f373bfb52e9.png). But sometimes,
you'll see text, too.

If a Property is inherited, there's literally an "(i)" written in the
Type column. For example, `/Parent/Child.primvars:foo`.

It's important to note that when we say "inherited" with Properties,
that isn't referring to the "inherits" Composition Arc. In USD, certain
properties from ancestral Prims cascade down to their children.

e.g.
 - All primvars
 - model:drawMode
 - skel:skeleton
 - material collection bindings

This "Property inheritance" is how USD adds different values onto
instanced Prims without breaking their instancing.


### Property Fonts
Property fonts are always the same unless the Property is inherited
from an ancestor Prim. If that happens, the Property is written
in Italics and slightly smaller than usual. See [Property Type
Column](#Property-Type-Column) for details.

Example property: `/Parent/Child.primvars:foo`


### Icons

|                                                                 Icon                                                                  |                                             Explanation                                             |                Location                |
|---------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|----------------------------------------|
| ![usd-attr-plain-icon.png](https://user-images.githubusercontent.com/10103049/64097798-064c0580-cd1a-11e9-8b6c-4d4d47ec3928.png)      | A Plain Attribute. Nothing Special                                                                  | /SomePrim.purpose                      |
| ![usd-attr-with-conn-icon.png](https://user-images.githubusercontent.com/10103049/64097752-ef0d1800-cd19-11e9-8986-ade76e5c0eee.png)  | A "terminal" Property that connects to a "port" Property                                            | /card/boardMat.outputs:surface         |
| ![usd-cmp-icon.png](https://user-images.githubusercontent.com/10103049/64098197-1adccd80-cd1b-11e9-8464-4f726472ab47.png)             | A resolved value that was created in a Session Layer. For example: Missing Bounding box information | /SomePrim.World Bounding Box           |
| ![usd-conn-icon.png](https://user-images.githubusercontent.com/10103049/64098151-fc76d200-cd1a-11e9-9ac8-76bd4e67ac71.png)            | A "port" Property that a "terminal" Property connects into                                          | /card/boardMat.outputs:surface         |
| ![usd-rel-plain-icon.png](https://user-images.githubusercontent.com/10103049/64097833-1d8af300-cd1a-11e9-9086-1f373bfb52e9.png)       | A Relationship that has no targets                                                                  | /SomePrim.relationship_with_no_targets |
| ![usd-rel-with-target-icon.png](https://user-images.githubusercontent.com/10103049/64097942-6478e880-cd1a-11e9-95df-9d8ead6a71f7.png) | A Relationship that has 1-or-more targets                                                           | /SomePrim.relationship_with_targets    |
| ![usd-target-icon.png](https://user-images.githubusercontent.com/10103049/64098082-d3564180-cd1a-11e9-935e-c86a71db739e.png)          | A Relationship's destination Prim or Property Target                                                | /SomePrim.relationship_with_targets    |



# References

[the main function that sets property style data](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usdImaging/lib/usdviewq/appController.py#L3341-L3456)

[GetPropertyColor function](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usdImaging/lib/usdviewq/common.py#L284-L299)

[UIPrimTypeColors](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usdImaging/lib/usdviewq/common.py#L50-L54)

[UIPropertyValueSourceColors](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usdImaging/lib/usdviewq/common.py#L56-L61)
