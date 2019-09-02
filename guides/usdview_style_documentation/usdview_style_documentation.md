# Quick Explanation
What you ever wondered what all the text colors, fonts, and icons in
usdview means? The different combinations of data can be pretty complex.
This article will explain usdview's visuals, and how the USD API is used
to achieve them.

This page contains everything you need to know.


## A breakdown of usdview
`usdview` has lots rules for how its prim / property information is
displayed. To help make sense of it all, [This usdview_style_stage.usda
file](usdview_style_stage.usda) contains a simple stage for every single
color / font / icon that usdview uses.

That stage can be used as a reference while viewing the rest of this section

```bash
usdview usdview_style_stage.usda
```


### Prim Text Colors
Name|Description|Value|Location
Normal|Neither an instance or a master|rgb(227, 227, 227)|/SomePrim
Instance|An instanced Prim|rgb(135, 206, 250)|/InstancedItem
Master|A Prim which is used by instances|rgb(118, 136, 217)|`/__Master_1`
Has Arcs|A Prim that contains 1+ Composition Arc|rgb(222, 158, 46)|/Inherited


### Property Text Colors
Name|Description|Value|Location
Time Sample|The value comes from an authored time value|rgb(177, 207, 153)|/SomePrim.time_samples_property
Value Clip|The value resolved to a stitched clip layer|rgb(230, 150, 230)|TODO
Type fallback|No value was found so USD used the Prim's type as a fallback|rgb(222, 158, 46)|/SomePrim.visibility
Default|The property's default (non-time-sampled) value|rgb(135, 206, 250)|/SomePrim.default_property
None|No value could be found|rgb(140, 140, 140)|/SomePrim.xformOpOrder


### Fonts
Name|Style|Description|Location
Abstract|Normal|A class Prim. Enable "Show" > "Abstract Prims (Classes)"|/SomeClass
Defined|Bold|A normal Prim that will be in default traversals|/SomePrim
Overed Prim|Italics|An undefined Prim (an Orphaned Over). Enable "Show" > "Undefined Prims (Overs)"|/OrphanedOver

Inherited|TODO


### Icons
Icon|Explanation|Location
![](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usdImaging/lib/usdviewq/icons/usd-cmp-icon.png)|This means "blah"


![](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usdImaging/lib/usdviewq/icons/usd-conn-icon.png)|TODO

![](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usdImaging/lib/usdviewq/icons/usd-attr-plain-icon.png)

![](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usdImaging/lib/usdviewq/icons/usd-attr-with-conn-icon.png)

![](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usdImaging/lib/usdviewq/icons/usd-rel-plain-icon.png)|A relationship with no authored targets

![](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usdImaging/lib/usdviewq/icons/usd-rel-with-target-icon.png)|A relationship that points to 1-or-more targets

![](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usdImaging/lib/usdviewq/icons/usd-target-icon.png)|A Relationship's destination Prim / Property target

![](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usdImaging/lib/usdviewq/icons/usd-conn-icon.png)

![](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usdImaging/lib/usdviewq/icons/usd-cmp-icon.png)


# References

[GetPropertyColor function](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usdImaging/lib/usdviewq/common.py#L284-L299)

[UIPrimTypeColors](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usdImaging/lib/usdviewq/common.py#L50-L54)

[UIPropertyValueSourceColors](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae19e6fd38f7928d07f0e4cf5040/pxr/usdImaging/lib/usdviewq/common.py#L56-L61)
