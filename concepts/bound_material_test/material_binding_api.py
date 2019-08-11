#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Usd, UsdShade

_ALLOWED_MATERIAL_PURPOSES = (
    UsdShade.Tokens.full,
    UsdShade.Tokens.preview,
    UsdShade.Tokens.allPurpose,
)


def get_binding_relationships(prim):
    relationships = prim.GetRelationships()

    return [
        relationship
        for relationship in relationships
        if relationship.GetName().startswith(UsdShade.Tokens.materialBinding)
    ]


# def get_material(prim, stage=None):
#     if not stage:
#         stage = prim.GetStage()
#
#     for relationship in get_binding_relationships(prim):
#         targets = len(relationship.GetTargets())
#
#         if targets == 1:
#             binding = UsdShade.MaterialBindingAPI.DirectBinding(relationship)
#
#             if binding.GetMaterial():
#                 material = binding.GetMaterialPath()
#
#                 return stage.GetPrimAtPath(material)
#         elif targets == 2:
#             collection = UsdShade.MaterialBindingAPI.CollectionBinding(relationship)
#             material = collection.GetMaterial()
#
#             if material:
#                 return stage.GetPrimAtPath(collection.GetMaterialPath())
#
#             collection_ = collection.GetCollection()
#
#             if collection_:
#                 return stage.GetPrimAtPath(collection.GetCollectionPath())
#
#     return None
#
#
# def main():
#     """Run the main execution of the current script."""
#     stage = Usd.Stage.Open("./materials.usda")
#     prim = stage.GetPrimAtPath("/Bob/Geom/Body")
#
#     print(get_material(prim))


def get_bound_material(prim, collection="", purpose=UsdShade.Tokens.allPurpose):
    if purpose not in _ALLOWED_MATERIAL_PURPOSES:
        raise ValueError(
            'Purpose "{purpose}" is not valid. Options were, "{options}".'.format(
                purpose=purpose, options=sorted(_ALLOWED_MATERIAL_PURPOSES)
            )
        )

    binding = UsdShade.MaterialBindingAPI(prim)

    if collection:
        relationship = binding.GetCollectionBindingRel(
            collection, materialPurpose=purpose
        )

        if relationship.IsValid():
            collection_binding = UsdShade.MaterialBindingAPI.CollectionBinding(
                relationship
            )

            return prim.GetStage().GetPrimAtPath(collection_binding.GetMaterialPath())

    # XXX : If no collection was requested OR the collection requested
    # was not found, it may be possible that `prim` has a fallback
    # direct binding applied.
    #
    relationship = binding.GetDirectBindingRel(materialPurpose=purpose)
    binding = UsdShade.MaterialBindingAPI.DirectBinding(relationship)

    return prim.GetStage().GetPrimAtPath(binding.GetMaterialPath())


def main():
    """Run the main execution of the current script."""
    stage = Usd.Stage.Open("./office_set.usda")
    prim = stage.GetPrimAtPath("/Office_set/Desk_Assembly")

    print(get_bound_material(prim))
    print(get_bound_material(prim, collection="Erasers"))
    print(get_bound_material(prim, collection="Shafts"))


if __name__ == "__main__":
    main()
