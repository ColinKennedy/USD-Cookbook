// IMPORT STANDARD LIBRARIES
#include <algorithm>
#include <iostream>
#include <iterator>
#include <string>
#include <vector>

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/usd/sdf/path.h>
#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usd/variantSets.h>
#include <pxr/usd/usdGeom/sphere.h>


struct VariantData {
    pxr::SdfPath selector;
    std::string variant_set;
    std::string selection;
};


std::vector<pxr::SdfPath> _get_all_parents(pxr::SdfPath const &path)
{
    auto parent = path;
    std::vector<pxr::SdfPath> output;

    while (!parent.IsRootPrimPath())
    {
        output.push_back(parent);
        parent = parent.GetParentPath();
    }

    return output;
}


std::vector<VariantData> _gather_variant_selection(pxr::SdfPath const &path)
{
    std::vector<VariantData> output {};
    auto parents = _get_all_parents(path);
    std::reverse(std::begin(parents), std::end(parents));

    for (auto const &path_ : parents)
    {
        auto data = path_.GetVariantSelection();
        auto variant_set = data.first;
        auto selection = data.second;

        if (variant_set.empty() || selection.empty())
        {
            continue;
        }

        VariantData item {path_.StripAllVariantSelections(), variant_set, selection};
        output.emplace_back(item);
    }

    return output;
}


pxr::UsdPrim get_prim_at_path(pxr::UsdStagePtr const &stage, pxr::SdfPath const &path)
{
    if (!path.ContainsPrimVariantSelection())
    {
        return stage->GetPrimAtPath(path);
    }

    auto root = path.GetPrimOrPrimVariantSelectionPath();

    // TODO : Add check here

    for (auto variant_data : _gather_variant_selection(root))
    {
        auto prim = stage->GetPrimAtPath(pxr::SdfPath{variant_data.selector});
        auto selector = prim.GetVariantSets().GetVariantSet(variant_data.variant_set);
        selector.SetVariantSelection(variant_data.selection);
    }

    auto composed_path = path.StripAllVariantSelections();

    return stage->GetPrimAtPath(composed_path.GetPrimPath());
}


int main() {
    auto stage = pxr::UsdStage::CreateInMemory();
    stage->GetRootLayer()->ImportFromString(
        R""""(#usda 1.0

        def Scope "root" (
            variantSets = ["foo"]
        )
        {
            variantSet "foo" = {
                "base" { def Scope "prim1"
                    {
                        def Sphere "a_sphere"
                        {
                            double radius = 3
                        }
                    }
                }
                "another" {
                    def Scope "prim2" (
                        variantSets = ["bar"]
                    )
                    {
                        variantSet "bar" = {
                            "one" {
                                def Sphere "sphere"
                                {
                                    double radius = 2
                                }
                            }
                        }
                    }
                }
            }
        }
        )""""
    );

    auto variant_sphere = pxr::UsdGeomSphere(
        get_prim_at_path(
            stage,
            pxr::SdfPath{"/root{foo=base}prim1/a_sphere"}
        )
    );
    double radius;
    variant_sphere.GetRadiusAttr().Get(&radius);
    std::cout << "This value should be 3: \"" << radius << "\"\n";

    auto nested_variant_sphere = pxr::UsdGeomSphere(
        get_prim_at_path(
            stage,
            pxr::SdfPath{"/root{foo=another}prim2{bar=one}sphere"}
        )
    );
    nested_variant_sphere.GetRadiusAttr().Get(&radius);
    std::cout << "This value should be 2: \"" << radius << "\"\n";

    return 0;
}
