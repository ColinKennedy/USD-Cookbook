#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Usd, UsdShade

_ALLOWED_MATERIAL_PURPOSES = (
    UsdShade.Tokens.full,
    UsdShade.Tokens.preview,
    UsdShade.Tokens.allPurpose,
)


# TODO : Add `collection` as an input to this function
def get_bound_material(prim, material_purpose=UsdShade.Tokens.allPurpose):
    def is_binding_stronger_than_descendents(binding, purpose):
        return (
            UsdShade.MaterialBindingAPI.GetMaterialBindingStrength(
                binding.GetDirectBindingRel(materialPurpose=purpose)
            )
            == "strongerThanDescendents"
        )

    def get_collection_material_bindings_for_purpose(binding, purpose):
        # XXX : Note, Normally I'd just do
        # `UsdShadeMaterialBindingAPI.GetCollectionBindings` but, for
        # some reason, `binding.GetCollectionBindings(purpose)` does not
        # yield the same result as parsing the relationships, manually.
        # Maybe it's a bug?
        #
        # return binding.GetCollectionBindings(purpose)
        parent = binding.GetPrim()

        # TODO : We're doing quadratic work here... not sure how to improve this section
        while not parent.IsPseudoRoot():
            binding = binding.__class__(parent)

            material_bindings = [
                UsdShade.MaterialBindingAPI.CollectionBinding(relationship)
                for relationship in binding.GetCollectionBindingRels(purpose)
                if relationship.IsValid()
            ]

            if material_bindings:
                return material_bindings

            parent = parent.GetParent()

        return []

    def get_direct_bound_material_for_purpose(binding, purpose):
        relationship = binding.GetDirectBindingRel(materialPurpose=purpose)
        direct = UsdShade.MaterialBindingAPI.DirectBinding(relationship)

        if not direct.GetMaterial():
            return None

        material = direct.GetMaterialPath()
        prim = binding.GetPrim().GetStage().GetPrimAtPath(material)

        if not prim.IsValid():
            return None

        return prim

    if not prim.IsValid():
        raise ValueError('Prim "{prim}" is not valid.'.format(prim=prim))

    if material_purpose not in _ALLOWED_MATERIAL_PURPOSES:
        raise ValueError(
            'Purpose "{material_purpose}" is not valid. Options were, "{options}".'.format(
                material_purpose=material_purpose, options=sorted(_ALLOWED_MATERIAL_PURPOSES)
            )
        )

    purposes = {material_purpose, UsdShade.Tokens.allPurpose}

    for purpose in purposes:
        material = None
        parent = prim

        while not parent.IsPseudoRoot():
            binding = UsdShade.MaterialBindingAPI(parent)

            if not material or is_binding_stronger_than_descendents(binding, purpose):
                material = get_direct_bound_material_for_purpose(binding, purpose)

            for binding in get_collection_material_bindings_for_purpose(
                binding, purpose
            ):
                binding_collection = binding.GetCollection()
                membership = binding_collection.ComputeMembershipQuery()

                if membership.IsPathIncluded(parent.GetPath()) and (
                    not material
                    or is_binding_stronger_than_descendents(binding, purpose)
                ):
                    material = binding.GetMaterial()

            # Keep searching ancestors until we hit the scene root
            parent = parent.GetParent()

        if material:
            return material


def main():
    """Run the main execution of the current script."""
    stage = Usd.Stage.Open("./office_set.usda")

    prim = stage.GetPrimAtPath("/Office_set/Desk_Assembly/Cup_grp")
    material = get_bound_material(prim)
    # print(get_bound_material(prim, collection="Shafts"))
    print(get_bound_material(prim))

    # prim = stage.GetPrimAtPath("/Office_set/Desk_Assembly/Cup_grp")
    # print(get_bound_material(prim, collection="Erasers"))
    # print(get_bound_material(prim, collection="Shafts"))
    # print(get_bound_material(prim))

    # prim = stage.GetPrimAtPath("/Office_set/Desk_Assembly/Cup_grp/Pencil_1/Geom/Shaft")
    # print(get_bound_material(prim, collection="Shafts"))
    # print(get_bound_material(prim))
    #
    # prim = stage.GetPrimAtPath("/Office_set/Desk_Assembly/Cup_grp/Pencil_1/Geom/Erasers")
    # print(get_bound_material(prim, collection="EraserHeads"))
    # print(get_bound_material(prim))


if __name__ == "__main__":
    main()
