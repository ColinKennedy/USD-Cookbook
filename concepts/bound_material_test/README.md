## Quick Explanation
The function for finding bound materials on a USD prim is unfortunately
not concise enough to just paste into this file. So instead, here's some links

### C++
Coming soon

### Python
[material_binding_api.py](python/material_binding_api.py) has a
`get_bound_material` function. Use that to query the bound material of a
USD Prim. It takes into account the new material collections API.


## Longer Explanation (optional reading)
The USD documentation has a few issues when it comes to the new USD
Collections API. It's partly out of date and also is missing key
information for people to make use of it. This section is has one
purpose - provide an up-to-date reference for discovering material
bindings.

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

If you check out [materials.py](python/materials.py), you'll see the
old, deprecated method for querying material bindings.

Now check out [material_binding_api.py](python/material_binding_api.py)
and you'll see the new-and-improved method which takes into account the
new material collections API.


## Details (if you're curious. Not required reading)
### Justification for this project
As far as I could find, there's only two canonical
pages that show source code for getting/authoring
material assignment in USD. The [Simple Shading in USD
tutorial](https://graphics.pixar.com/usd/docs/Simple-Shading-in-USD.html
) (and I guess, by extension, also the [End to End
Example](https://graphics.pixar.com/usd/docs/End-to-End-Example.html)).
But that is direct material bindings. It's "old-hat", by USD's standards.
Direct bindings are still good as long as:

- You don't have to care about overriding shading on instanced Prims
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
The lines that define `collection:*:includes = ` need to end in `[` or
USD 19.07 will syntax error. Also every `expansionRule` needs to be a
token / uniform token, not a Relationship.

```usda
uniform token collection:Erasers:expansionRule = "expandPrims"
rel collection:Erasers:includes = [
	</Office_set/Desk_Assembly/Cup_grp/Pencil_1/Geom/EraserHead>,
	...
```

Someone may dislike these nitpicks since they're simple fixes but it's
the most documentation that we have currently and it doesn't work.
Anyone looking to get stuff done can't use this to work.


#### The Pseudo-code "GetBoundMaterial" matches the name of a method that is deprecated
The
[GetBoundMaterial](https://graphics.pixar.com/usd/docs/UsdShade-Material
-Assignment.html#UsdShadeMaterialAssignment-MaterialResolve:Determiningt
heBoundMaterialforanyGeometryPrim) function listed in the "UsdShade
Material Assignment" page isn't immediately copy-and-pasteable because
it's pseudo-code for the proposal. So the reader's next immediate thought
is "I bet if I check the USD API documentation, I'll find the equivalent
function".

[Found
it](https://graphics.pixar.com/usd/docs/api/class_usd_shade_material.htm
l#ac8a3ccb7c9859aabc5ba699b4addb834). Except
surprise, the method is deprecated. And [so is
GetBindingRel](https://graphics.pixar.com/usd/docs/api/class_usd_shade_m
aterial.html#a7d254deef591583ada16825840dd49a9).

The good news though is that the pseudo-code itself is fine, as long as
you're willing to write it out. Which is what this project is for.

Quick last note: it looks like `pxr::UsdShadeMaterial::AllPurpose` was
moved to `pxr::UsdShadeTokens->allPurpose`? Not totally sure if that's
correct.


## See Also
USD ships with a command-line python module called "complianceChecker"
which has an interesting way of querying material relationships on
prims. It's great but it doesn't answer the question of "which material
is bound to this Prim". Instead, it answers "if this Prim has material
bindings, are they broken?". The use-case is different but it is still
very useful.

[UsdUtils complianceChecker script](https://github.com/PixarAnimationStudios/USD/blob/32ca7df94c83ae
19e6fd38f7928d07f0e4cf5040/pxr/usd/lib/usdUtils/complianceChecker.py#L39
6-L421).


https://graphics.pixar.com/usd/docs/api/class_usd_shade_material_binding_a_p_i.html#a08ca12ce6b9929448e74e5a0ee310c05
https://graphics.pixar.com/usd/docs/UsdShade-Material-Assignment.html#UsdShadeMaterialAssignment-MaterialResolve:DeterminingtheBoundMaterialforanyGeometryPrim
https://graphics.pixar.com/usd/docs/api/class_usd_shade_material.html#a52c7fe053819a1b71103f7a2b6a730e8
https://graphics.pixar.com/usd/docs/api/class_usd_collection_a_p_i_1_1_membership_query.html
https://graphics.pixar.com/usd/docs/api/class_usd_shade_material_binding_a_p_i.html
