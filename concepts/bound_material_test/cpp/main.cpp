// IMPORT STANDARD LIBRARIES
#include <iostream>
#include <set>
#include <vector>

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/base/tf/token.h>
#include <pxr/usd/sdf/path.h>
#include <pxr/usd/usd/prim.h>
#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usdShade/material.h>
#include <pxr/usd/usdShade/materialBindingAPI.h>
#include <pxr/usd/usdShade/tokens.h>


static std::set<pxr::TfToken> const _ALLOWED_MATERIAL_PURPOSES {
    pxr::UsdShadeTokens->full,
    pxr::UsdShadeTokens->preview,
    pxr::UsdShadeTokens->allPurpose,
};


bool _is_binding_stronger_than_descendents(
    pxr::UsdShadeMaterialBindingAPI const &binding,
    pxr::TfToken const &purpose
) {
    static pxr::TfToken const strength {"strongerThanDescendents"};

    return pxr::UsdShadeMaterialBindingAPI::GetMaterialBindingStrength(
        binding.GetDirectBindingRel(purpose)) == strength;
}


bool _is_binding_stronger_than_descendents(
    pxr::UsdShadeMaterialBindingAPI::CollectionBinding const &binding,
    pxr::TfToken const &purpose
) {
    static pxr::TfToken const strength {"strongerThanDescendents"};

    return pxr::UsdShadeMaterialBindingAPI::GetMaterialBindingStrength(
        binding.GetBindingRel()) == strength;
}


std::vector<pxr::UsdShadeMaterialBindingAPI::CollectionBinding> _get_collection_material_bindings_for_purpose(
    pxr::UsdShadeMaterialBindingAPI const &binding,
    pxr::TfToken const &purpose
) {
    auto parent = binding.GetPrim();

    for (; not parent.IsPseudoRoot(); parent = parent.GetParent()) {
        auto binding = pxr::UsdShadeMaterialBindingAPI {parent};

        // TODO: Check if this function works in C++
        auto material_bindings = binding.GetCollectionBindings(purpose);

        if (!material_bindings.empty()) {
            return material_bindings;
        }
    }

    return {};
}


pxr::UsdShadeMaterial _get_direct_bound_material_for_purpose(
    pxr::UsdShadeMaterialBindingAPI const &binding,
    pxr::TfToken const &purpose
) {
    auto relationship = binding.GetDirectBindingRel(purpose);
    auto direct = pxr::UsdShadeMaterialBindingAPI::DirectBinding {relationship};

    if (!direct.GetMaterial()) {
        return pxr::UsdShadeMaterial {};
    }

    auto material = direct.GetMaterialPath();
    auto prim = binding.GetPrim().GetStage()->GetPrimAtPath(material);

    if (!prim.IsValid()) {
        return pxr::UsdShadeMaterial {};
    }

    return pxr::UsdShadeMaterial {prim};
}


pxr::UsdShadeMaterial get_bound_material(
    pxr::UsdPrim const &prim,
    pxr::TfToken material_purpose=pxr::UsdShadeTokens->allPurpose,
    std::string const &collection=""
) {
    if (!prim.IsValid()) {
        throw "prim \"" + prim.GetPath().GetString() + "\" is not valid";
    }

    if (std::find(std::begin(_ALLOWED_MATERIAL_PURPOSES), std::end(_ALLOWED_MATERIAL_PURPOSES), material_purpose) == std::end(_ALLOWED_MATERIAL_PURPOSES)) {

    }

    std::set<pxr::TfToken> purposes = {material_purpose, pxr::UsdShadeTokens->allPurpose};
    pxr::UsdPrim parent;

    for (auto const &purpose : purposes) {
        pxr::UsdShadeMaterial material;

        for (parent = prim; not parent.IsPseudoRoot(); parent = parent.GetParent()) {
            auto binding = pxr::UsdShadeMaterialBindingAPI {parent};

            if (!material || _is_binding_stronger_than_descendents(binding, purpose)) {
                material = _get_direct_bound_material_for_purpose(binding, purpose);
            }

            for (auto const &binding : _get_collection_material_bindings_for_purpose(binding, purpose)) {
                auto binding_collection = binding.GetCollection();

                if (!collection.empty() && binding_collection.GetName() != collection) {
                    continue;
                }

                auto membership = binding_collection.ComputeMembershipQuery();

                if (membership.IsPathIncluded(parent.GetPath()) && (!material || _is_binding_stronger_than_descendents(binding, purpose))) {
                    material = binding.GetMaterial();
                }
            }
        }

        if (material) {
            return material;
        }
    }

    return pxr::UsdShadeMaterial {};
}


pxr::UsdShadeMaterial get_bound_material(
    pxr::UsdPrim const &prim,
    std::string const &collection=""
) {
    return get_bound_material(prim, pxr::UsdShadeTokens->allPurpose, collection);
}


int main() {
    auto stage = pxr::UsdStage::Open("../../usda/office_set.usda");

    auto prim = stage->GetPrimAtPath(pxr::SdfPath {"/Office_set/Desk_Assembly/Cup_grp"});
    std::cout << "The next 3 prints should be </Office_set/Materials/Default> because no collections don't include Cup_grp's path.\n";
    std::cout << get_bound_material(prim, "Erasers").GetPath();

    return 0;
}
