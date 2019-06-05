It's possible to force a parent VariantSet to change the selection of a child
VariantSet.

The way you do this is to make use of 3 features:
1. non-concrete Prims (in this case, class)
2. References
3. Variants

The basic Prim structure goes like this

- Parent
 - Child that contains VariantSet(s) that we want to modify
 - Some VariantSet which has opinions for the child and its VariantSets

The parent has a VariantSet that will author 1 Prim, which has variant
selection information stored in its metadata, inside the (). In this
example, this would be "/Parent/HiddenContainer".

Then in the child, in this case "/Parent/ChildSphere", you add a Reference to
"/Parent/HiddenContainer". Because of the way Reference pulls in the Target Prim's information, 
"/Parent/ChildSphere" now contains the Variant selection that is written in "/Parent/HiddenContainer"!

If you open variant_set_auto_selections.usda in usdview, the effect should be obvious. Whenever you change "parent_variant_set", the "/Parent/HiddenContainer" class will change its Variant selection. "/Parent/ChildSphere" picks up this Variant selection and then uses it, as its own.
