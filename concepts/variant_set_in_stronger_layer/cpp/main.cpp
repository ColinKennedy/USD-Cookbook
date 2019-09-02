// IMPORT STANDARD LIBRARIES
#include <cstdio>
#include <string>

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/usd/sdf/layer.h>
#include <pxr/usd/sdf/types.h>
#include <pxr/usd/usd/editContext.h>
#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usd/variantSets.h>
#include <pxr/usd/usdGeom/sphere.h>


constexpr char TEMPORARY_BASIC_STAGE[] = "/tmp/mytemp.usda";


void create_basic_stage(std::string const &path) {
    auto stage = pxr::UsdStage::CreateNew(path);
    auto sphere = pxr::UsdGeomSphere::Define(stage, pxr::SdfPath("/SomeSphere"));

    auto variants = sphere.GetPrim().GetVariantSets();
    auto variant = variants.AddVariantSet("some_variant");

    variant.AddVariant("variant_name_1");
    variant.AddVariant("variant_name_2");
    variant.AddVariant("variant_name_3");

    auto radius = sphere.GetRadiusAttr();

    // XXX: In the Python API, the variant set edits are applied in a "with" block
    //      The variant set resets when the "with" block exits
    //
    //      In C++, the destructor `pxr::UsdEditContext::~UsdEditContext()`
    //      is used to reset the variant set. So we just need to wrap the
    //      context in a scope and it'll do the same thing. Cool, right?
    //
    {
        variant.SetVariantSelection("variant_name_1");
        pxr::UsdEditContext context {variant.GetVariantEditContext()};
        radius.Set(1.0);
    }

    {
        variant.SetVariantSelection("variant_name_2");
        pxr::UsdEditContext context {variant.GetVariantEditContext()};
        radius.Set(2.0);
    }

    {
        variant.SetVariantSelection("variant_name_3");
        pxr::UsdEditContext context {variant.GetVariantEditContext()};
        radius.Set(3.0);
    }

    // XXX: We set this attribute just to show that "variant_name_3" isn't still active
    pxr::VtArray<pxr::GfVec3f> extent {{3.0, 3.0, 3.0}};
    sphere.GetExtentAttr().Set(extent);

    stage->Save();
}

int main() {
    std::string path {TEMPORARY_BASIC_STAGE};
    create_basic_stage(path);
    // pxr::UsdStage::Create
    return 0;
}
