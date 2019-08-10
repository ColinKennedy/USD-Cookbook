## Explanation

Not all VariantSets are created equal. Suppose you have 2 applications,
application_a and application_b. application_a is meant to let the user
view different variant sets, add opinions to the user's stage, and write
that stage to file.

The other application, application_b, assumes that the stage
will load certain variant sets on-startup to show some data to
the user. Perhaps application_b uses a [variant set fallback
plugin](../../concepts/variant_fallbacks/README.md) to make sure
everything loads as expected.

The trouble is, variant set fallbacks only get chosen if there's no
opinion set onto a VariantSet. But someone wrote a VariantSet selection
in application_a while they were making changes to the stage.

What we really need, in this scenario, is for application_a to not write
variant selections for the VariantSets that we care about so that it
doesn't get in the way of application_b.

This is precisely what VariantSet selection export policies are made
to do. In fact, you can have different applications have completely
different VariantSet selection policies, so you can finely which of your
applications write variant selections for which VariantSets.


## How to setup a variant selection export policy
Like everything customizable in USD, we'll use a plugin.

In our earlier example with the two applications, pretend that this is
how you'd call them:

```bash
python application_a.py
python application_b.py
```

- Define a plugInfo.json file to define the selection export policies

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

- Save that as a file called "plugInfo.json" and put it in a folder somewhere.
- Add the new file to your `PXR_PLUGINPATH_NAME` environment variable, like so:

```bash
PXR_PLUGINPATH_NAME=$PWD/plugin:$PXR_PLUGINPATH_NAME python application_a.py
python application_b.py
```

Now application_a.py and application_b.py have different selection
export policies.


## How to use a variant selection export policy
From what I've read so far, it looks like the selection export policies
actually integrated into the literal export methods of USD. You have
to implement logic in your applications to actually make use of the
selection export policies (which is a huge shame!)

Luckily, USD makes this easy to do:

```python
from pxr import UsdUtils
UsdUtils.GetRegisteredVariantSets()
```

If you dig around the USD source code, you'll see a common pattern
where, just before export, variant sets are checked and set, if needed.

Exerpt from UsdKatana:

```cpp
//
// Set attributes for variant sets that apply (e.g. modelingVariant, 
// lodVariant, shadingVariant).
//

for (const auto& regVarSet: UsdUtilsGetRegisteredVariantSets()) {

    // only handle the "always" persistent variant sets.
    switch (regVarSet.selectionExportPolicy) {
        case UsdUtilsRegisteredVariantSet::SelectionExportPolicy::Never:
        case UsdUtilsRegisteredVariantSet::SelectionExportPolicy::IfAuthored:
            continue;
        case UsdUtilsRegisteredVariantSet::SelectionExportPolicy::Always:
            break;
    }

    const std::string& varSetName = regVarSet.name;

    std::string variantSel;
    if (UsdVariantSet variant = prim.GetVariantSet(varSetName)) {
        variantSel = variant.GetVariantSelection();
    }
    if (!variantSel.empty()) {
        attrs.set(varSetName, FnKat::StringAttribute(variantSel));
    }
}
```

In this case, `attrs` is a mapping of information that gets written
to-disk as part of the export process. But only registered variant sets
actually get exported.

There's a similar block of code in the UsdMaya translator plugin, too.

Really though, it's up to you to decide how to you want to use them.
Maya even has logic that allows attributes that only partially match
registered variant selection names to export, for example. Use this
feature however makes sense for your pipeline.

## Important Note
For some reason, the example for variant selection export policies is written incorrectly.
It shows a JSON with a list-of-dicts but if you check the code, it clearly expects
RegisteredVariantSets to be a dictionary.

```cpp
if (!registeredVariantSetsValue.IsObject()) {
    TF_CODING_ERROR(
            "%s[UsdUtilsPipeline][RegisteredVariantSets] was not a dictionary.",
            plug->GetName().c_str());
    continue;
}
```

Maybe it was a typo that was mistakenly not fixed?


## See Also
https://graphics.pixar.com/usd/docs/api/pipeline_8h.html#af8c5904ce00b476edc137bb4ae0e114d
https://graphics.pixar.com/usd/docs/api/struct_usd_utils_registered_variant_set.html#a2b2b4d4a3287ed9efc76aaa85fb76d9c
https://graphics.pixar.com/usd/docs/api/class_plug_registry.html
