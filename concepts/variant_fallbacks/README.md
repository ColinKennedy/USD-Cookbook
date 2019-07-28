## Quick Explanation
### The Easy Way
Before opening a stage, you can set the fallback options by VariantSet
name. It's pretty easy:

```python
Usd.Stage.SetGlobalVariantFallbacks({"some_variant_set_name": ["foo", "bar"]})
stage = Usd.Stage.Open("some_file.usda")
# Assuming `stage` has any VariantSet called "some_variant_set_name",
# those VariantSets may have either "foo" or "bar" variants as their
# default selection. USD will only select one of those 2 options if the
# variant already exists on the VariantSet.
```

Make sure to note USD's documentation for `SetGlobalVariantFallbacks`
which says: "This does not affect existing UsdStages".


### The Hard Way
If you want a more systemic way of setting global variant fallbacks, USD
lets you define VariantSet selection fallbacks using its plugin system.
The rest of this document explains how to do that.


## The Problem That This Folder Solves
By default, if you author a VariantSet with 1+ variant inside of it, USD
still won't select any of them. So for example, if you made a USD file
like this:

```usda
#usda 1.0

def Xform "SomePrim" (
    prepend variantSets = "some_variant_set_name"
)
{
    variantSet "some_variant_set_name" = {
        "bar" {
            def Sphere "Child"
            {
                # ... more stuff ...
            }
        }
        "foo" {
            def Sphere "Child"
            {
                # ... more stuff ...
            }
        }
    }
}
```

And then you loaded the file in usdview, the "some_variant_set_name"
VariantSet will have nothing selected. Neither "foo" nor "bar". But what
if you're depending on either "foo" or "bar" being selected? There's
no out-of-the-box way to do this but you can easily extend USD to tell
it to search for "foo" or "bar" variants by writing a Variant Fallback
plugin.


## The Variant Fallback Plugin
Here's the example `plugInfo.json` that is used in this folder:

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

Most of the keys and values listed above are completely standard for any
USD plugin. The parts worth mentioning is this bit:

```json
...

"UsdVariantFallbacks": {
    "some_variant_set_name": ["possible_fallback_1", "possible_fallback_2", "possible_fallback_3", "foo", "bar"]
}

...
```

The "UsdVariantFallbacks" key just comes from reading
source-code and the "Variant Management" section on this page:
https://graphics.pixar.com/usd/docs/api/class_usd_stage.html. Each
key is the name of a VariantSet that you're added default values for
and the list of each variant that is a valid default value for that
VariantSet. USD will try each variant in left-to-right order when it
finds a VariantSet called "some_variant_set_name" until it finds an
authored variant that matches a default. Otherwise, no default variant
is selected.


### Extra Context On How This Works
If you check out the documentation for PcpCache, you'll see a method called [SetVariantFallbacks](https://graphics.pixar.com/usd/docs/api/class_pcp_cache.html#a7e4146ac269e86cb8b033b8c71d55581). Sounds promising, right?
Well, it turns out that every UsdStage contains a PcpCache and runs `SetVariantFallbacks` [when the USD Stage is first opened](https://github.com/PixarAnimationStudios/USD/blob/master/pxr/usd/lib/usd/stage.cpp#L451). 
Dig around a bit more and you'll see that `GetGlobalVariantFallbacks` returns `_usdGlobalVariantFallbackMap`, [which is created here](https://github.com/PixarAnimationStudios/USD/blob/master/pxr/usd/lib/usd/stage.cpp#L187-L219).

And there's our answer. The fallback map is just reading from USD's
discovered plugins. Now all we have to do is provide our own fallbacks
and USD will happily accept it.


## See Also
Read the section titled "Variant Management" on this page: https://graphics.pixar.com/usd/docs/api/class_usd_stage.html
https://github.com/PixarAnimationStudios/USD/blob/master/pxr/usd/lib/usd/stage.cpp
https://graphics.pixar.com/usd/docs/api/class_pcp_cache.html
https://graphics.pixar.com/usd/docs/api/pcp_page_front.html
