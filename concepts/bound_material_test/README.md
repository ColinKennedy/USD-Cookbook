## Quick Explanation
The USD documentation is a few issues when it comes to the new USD
Collections API. It's partly out of date and also is missing key
information to be useful. This section is has one purpose - provide an
up-to-date reference for discovering material bindings.

Note:
    In the future, new information / reference material may be found that
    will make this project redundant. If that's the case, please delete
    this page.


### Summary
Do not use `UsdShadeMaterial` for querying information about materials.
It's deprecated. Instead, prefer `UsdShadeMaterialBindingAPI`.
[Pixar also recommends to use UsdShadeMaterialBindingAPI,
too](https://graphics.pixar.com/usd/docs/UsdShade-Material-Assignment.ht
ml#UsdShadeMaterialAssignment-UsdShadeAPI) but they don't go into detail
on how to use it.

If you check out 
Here's how you can query all of the material bindings on a Prim.


This snippet is a modified version that Pixar
provides from their [UsdUtils complianceChecker
script](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae
19e6fd38f7928d07f0e4cf5040/pxr/usd/lib/usdUtils/complianceChecker.py#L39
6-L421). But instead of trying to find invalid material binding
definitions, we focus on just getting back the correct material.

You could also use the same code to validate that material bindings are
correct in USD files in your own pipeline.


## Details
### Justification for this project
As far as I could find, there's only two canonical pages that
talk about material assignment in USD. The [Simple Shading in USD
tutorial](https://graphics.pixar.com/usd/docs/Simple-Shading-in-USD.html
) (and I guess, by extension, also the [End to End
Example](https://graphics.pixar.com/usd/docs/End-to-End-Example.html)).
This page covers direct material bindings. It's "old-hat" but still good
assuming that

- You don't have to care about overriding shading on instancing
- You're fine with having less control over who is allowed to override
material assignments

If either point is problematic for you (which is should, because most
pipelines of any complexity need per-instance material assignment),
the USD documentation suggests using USDCollectionAPI. From what
I could see, this is the only page where USD files and API are
explained in the same place, the [UsdShade Material Assignment
page](https://graphics.pixar.com/usd/docs/UsdShade-Material-Assignment.h
tml).


But this page has several problems.


#### The provided material USDA example file doesn't work
- The materials example in this page doesn't work.
   - e.g. If you copy/paste the "Resolving Hierarchically-bound
   Materials" into a USD file, it'll syntax error because `token` is
   missing from outputs.


#### The provided Set-Shaded Office_set has multiple syntax errors
The lines that define `collection:*:includes = ` need to end in `[` or USD 19.07 will syntax error. Also every `expansionRule` needs to be a token / uniform token, not a Relationship.

```usda
uniform token collection:Erasers:expansionRule = "expandPrims"
rel collection:Erasers:includes = [
	</Office_set/Desk_Assembly/Cup_grp/Pencil_1/Geom/EraserHead>,
	...
```

Someone may dislike these nitpicks since they're simple fixes but it's
the most documentation that we have currently and it doesn't work. For
the uninitiated, this is a point of friction.


#### The Pseudo-code "GetBoundMaterial" is deprecated
The
[GetBoundMaterial](https://graphics.pixar.com/usd/docs/UsdShade-Material
-Assignment.html#UsdShadeMaterialAssignment-MaterialResolve:Determiningt
heBoundMaterialforanyGeometryPrim) function listed in the "UsdShade
Material Assignment" page isn't immediately copy-and-pasteable because
it's just an example for the proposal. So a client's next immediate
thought is "I bet if I check the USD API documentation, I'll find the
equivalent function".

[Found it](https://graphics.pixar.com/usd/docs/api/class_usd_shade_material.html#ac8a3ccb7c9859aabc5ba699b4addb834). Except it's deprecated. [So is GetBindingRel](https://graphics.pixar.com/usd/docs/api/class_usd_shade_material.html#a7d254deef591583ada16825840dd49a9).

So now what?

Until there's a canonical reference of how to get a bound material,
there's a snippet of code in the [UsdUtils complianceChecker
script](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae
19e6fd38f7928d07f0e4cf5040/pxr/usd/lib/usdUtils/complianceChecker.py#L39
6-L421) that reliably gets material binding information.



Binding tests

Even though the ancestral binding is weaker (for the mesh) than the descendant-binding, when a GL renderer asks </Bob/Geom/Body> what shading network it should use, the answer should be the glslfx:surface

