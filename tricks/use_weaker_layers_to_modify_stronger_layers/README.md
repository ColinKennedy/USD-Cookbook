This section is somewhat of a mix between two separate sections,
[Overriding VariantSets](../../concepts/variant_set_in_stronger_layer) 
and 
[Variant auto-selections - Using VariantSets to modify other VariantSets](../variant_set_auto_selections).

The idea is this - We can add variant selections from stronger layers
and we can even use variant sets to modify other variant sets.

Can a variant set from a weaker layer modify a stronger layer?

**Yes, it can**


## Examples
[simple.usda](simple.usda) shows the composition arcs without extra layers.

[over.usda](over.usda) shows a weaker layer's overs being used to modify Prims defined in a stronger layer.

[state_switch.usda](state_switch.usda) uses a weaker layer to force variants in a stronger layer.

[complex.usda](complex.usda) demonstrates how to use weak
variant sets to modify composition arcs in stronger layers.

This topic is very broad and has many applications.


## How It Works
Recall that in [Understanding VariantSets](../../concepts/variant_set_understanding)
it was mentioned that Variant Sets wrap the whole Prim, not just its
children. You can exploit this behavior to do things like add overs,
composition arcs, and other details onto a Prim.


### Limitations
- It's not a good idea to define new variant sets within weaker layers.

Check out [nested_variant_example](nested_variant_example.usda).
It kind of works but kind of doesn't. For example, if you switch
to geo=selection_1, it shows the look variant. But if you switch
to geo=selection_2 then it disappears. Likewise, if you're using
variant selection fallbacks then switching to look=look_1 will cause
geo=selection_2 to be selected. In other words, selecting a variant
in the "look" variantSet effectively erases the "look" variantSet's
existence.

- Session selections will take priority over any "auto-change" behavior.

[state_switch.usda](state_switch.usda) shows this limitation clearly.
The point of state_switch.usda is you're supposed to use </_container>
and "some_other_variant=force_selection_1_in_the_geo_variant_set" to
force "geo=selection_1" on the same Prim. But if "geo" already has a
selection like "geo=selection_2", then that selection takes priority.

This same problem applies to any Prim which inherits from </_container>,
such as </item_2>. If you change the variant selections of
</_container>, it should apply to all child Prims like </item_1> and
</item_2>. But if any of the child Prims were given their own selections
then the auto-switch behavior doesn't happen for that Prim.

Depending on your scenario, this might actually be something you want.
But if you're trying to rely on that behavior, this is definitely a
problem you'd run into.
