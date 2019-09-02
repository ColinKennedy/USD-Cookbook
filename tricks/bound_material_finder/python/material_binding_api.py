#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A module that contains `get_bound_material`.

`get_bound_material` is an updated function to find the bound material of a USD Prim.

Warning:
    No guarantees on if `get_bound_material` works correctly, though
    it's modelled after a Pixar function so it should work. That said,
    heavily unittest this function before using it in production.

"""

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Usd, UsdShade

# XXX : The USD documentation mentions that it's okay to have custom
# material purposes but the USD standard only supports 2 (technically 3,
# since allPurpose is empty). Anyway, this tuple can change to whatever
# you need it to be for your pipeline.
#
_ALLOWED_MATERIAL_PURPOSES = (
    UsdShade.Tokens.full,
    UsdShade.Tokens.preview,
    UsdShade.Tokens.allPurpose,
)


def get_bound_material(
    prim, material_purpose=UsdShade.Tokens.allPurpose, collection=""
):
    """Find the strongest material for some prim / purpose / collection.

    If no material is found for `prim`, this function will check every
    ancestor of Prim for a bound material and return that, instead.

    Reference:
        https://graphics.pixar.com/usd/docs/UsdShade-Material-Assignment.html#UsdShadeMaterialAssignment-MaterialResolve:DeterminingtheBoundMaterialforanyGeometryPrim

    Args:
        prim (`pxr.Usd.Prim`):
            The path to begin looking for material bindings.
        material_purpose (str, optional):
            A specific name to filter materials by. Available options
            are: `UsdShade.Tokens.full`, `UsdShade.Tokens.preview`,
            or `UsdShade.Tokens.allPurpose`.
            Default: `UsdShade.Tokens.allPurpose`
        collection (str, optional):
            The name of a collection to filter by, for any found
            collection bindings. If not collection name is given then
            the strongest collection is used, instead. Though generally,
            it's recommended to always provide a collection name if you
            can. Default: "".

    Raises:
        ValueError:
            If `prim` is invalid or if `material_purpose` is not an allowed purpose.

    Returns:
        `pxr.UsdShade.Material` or NoneType:
            The strongest bound material, if one is assigned.

    """
    def is_collection_binding_stronger_than_descendents(binding):
        return (
            UsdShade.MaterialBindingAPI.GetMaterialBindingStrength(
                binding.GetBindingRel()
            )
            == "strongerThanDescendents"
        )

    def is_binding_stronger_than_descendents(binding, purpose):
        """bool: Check if the given binding/purpose is allowed to override any descendent bindings."""
        return (
            UsdShade.MaterialBindingAPI.GetMaterialBindingStrength(
                binding.GetDirectBindingRel(materialPurpose=purpose)
            )
            == "strongerThanDescendents"
        )

    def get_collection_material_bindings_for_purpose(binding, purpose):
        """Find the closest ancestral collection bindings for some `purpose`.

        Args:
            binding (`pxr.UsdShade.MaterialBindingAPI`):
                The material binding that will be used to search
                for a direct binding.
            purpose (str):
                The name of some direct-binding purpose to filter by. If
                no name is given, any direct-binding that is found gets
                returned.

        Returns:
            list[`pxr.UsdShade.MaterialBindingAPI.CollectionBinding`]:
                The found bindings, if any could be found.

        """
        # XXX : Note, Normally I'd just do
        # `UsdShadeMaterialBindingAPI.GetCollectionBindings` but, for
        # some reason, `binding.GetCollectionBindings(purpose)` does not
        # yield the same result as parsing the relationships, manually.
        # Maybe it's a bug?
        #
        # return binding.GetCollectionBindings(purpose)
        #
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
        """Find the bound material, using direct binding, if it exists.

        Args:
            binding (`pxr.UsdShade.MaterialBindingAPI`):
                The material binding that will be used to search
                for a direct binding.
            purpose (str):
                The name of some direct-binding purpose to filter by. If
                no name is given, any direct-binding that is found gets
                returned.

        Returns:
            `pxr.UsdShade.Material` or NoneType: The found material, if one could be found.

        """
        relationship = binding.GetDirectBindingRel(materialPurpose=purpose)
        direct = UsdShade.MaterialBindingAPI.DirectBinding(relationship)

        if not direct.GetMaterial():
            return None

        material = direct.GetMaterialPath()
        prim = binding.GetPrim().GetStage().GetPrimAtPath(material)

        if not prim.IsValid():
            return None

        return UsdShade.Material(prim)

    if not prim.IsValid():
        raise ValueError('Prim "{prim}" is not valid.'.format(prim=prim))

    if material_purpose not in _ALLOWED_MATERIAL_PURPOSES:
        raise ValueError(
            'Purpose "{material_purpose}" is not valid. Options were, "{options}".'.format(
                material_purpose=material_purpose,
                options=sorted(_ALLOWED_MATERIAL_PURPOSES),
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

            for collection_binding in get_collection_material_bindings_for_purpose(
                binding, purpose
            ):
                binding_collection = collection_binding.GetCollection()

                if collection and binding_collection.GetName() != collection:
                    continue

                membership = binding_collection.ComputeMembershipQuery()

                if membership.IsPathIncluded(parent.GetPath()) and (
                    not material
                    or is_collection_binding_stronger_than_descendents(
                        collection_binding
                    )
                ):
                    material = collection_binding.GetMaterial()

            # Keep searching ancestors until we hit the scene root
            parent = parent.GetParent()

        if material:
            return material


def main():
    """Run the main execution of the current script."""
    stage = Usd.Stage.Open("../usda/office_set.usda")

    prim = stage.GetPrimAtPath("/Office_set/Desk_Assembly/Cup_grp")
    print(
        "The next 3 prints should be /Office_set/Materials/Default because no collections don't include Cup_grp's path."
    )
    print(get_bound_material(prim, collection="Erasers").GetPath())
    print(get_bound_material(prim, collection="Shafts").GetPath())
    print(get_bound_material(prim).GetPath())

    prim = stage.GetPrimAtPath("/Office_set/Desk_Assembly/Cup_grp/Pencil_1/Geom/Shaft")
    print(
        'The next 2 prints should be /Office_set/Materials/YellowPaint even though only the first line specifies the "Shafts" collection. The reason is because the last found collection is found if no name is given.'
    )
    print(get_bound_material(prim, collection="Shafts").GetPath())
    print(get_bound_material(prim).GetPath())

    prim = stage.GetPrimAtPath(
        "/Office_set/Desk_Assembly/Cup_grp/Pencil_1/Geom/EraserHead"
    )
    print(
        'The next 2 prints should be /Office_set/Materials/PinkPearl even though only the first line specifies the "Erasers" collection. The reason is because the last found collection is found if no name is given.'
    )
    print(get_bound_material(prim, collection="Erasers").GetPath())
    print(get_bound_material(prim).GetPath())


if __name__ == "__main__":
    main()
