// IMPORT STANDARD LIBRARIES
#include <string>

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usd/editContext.h>
#include <pxr/usd/usd/variantSets.h>
#include <pxr/usd/usdGeom/sphere.h>


char const ASSET_PATH[] = "/tmp/asset.usda";
char const SEQUENCE_PATH[] = "/tmp/sequence.usda";
char const SHOT_PATH[] = "/tmp/shot_v001.usda";


std::string create_asset() {
    auto stage = pxr::UsdStage::CreateNew(ASSET_PATH);
    auto sphere = pxr::UsdGeomSphere::Define(stage, pxr::SdfPath("/SomeSphere"));

    stage->GetRootLayer()->SetDocumentation("This file contains the \"character\" that will be changed in other layers.");

    stage->Save();

    return std::string(ASSET_PATH);
}


std::string create_sequence(std::string const &asset) {
    auto stage = pxr::UsdStage::CreateNew(SEQUENCE_PATH);
    auto prim = stage->OverridePrim(pxr::SdfPath("/SomeSphere"));

    auto root = stage->GetRootLayer();
    root->InsertSubLayerPath(asset);

    root->SetDocumentation(
        "A common set of data for an entire sequence.");
    stage->SetMetadata(
        pxr::SdfFieldKeys->Comment,
        "We override the character to make it bigger and add some viewing option."
    );

    auto variants = prim.GetVariantSets();
    auto variant = variants.AddVariantSet("some_variant_set");
    variant.AddVariant("variant_name_1");

    variant.SetVariantSelection("variant_name_1");
    auto sphere = pxr::UsdGeomSphere(prim);

    {
        pxr::UsdEditContext context {variant.GetVariantEditContext()};
        pxr::VtArray<pxr::GfVec3f> color {{1, 0, 0}};
        sphere.GetDisplayColorAttr().Set(color);
    }

    stage->Save();

    return std::string(SEQUENCE_PATH);
}


std::string create_shot(std::string const &sequence) {
    auto stage = pxr::UsdStage::CreateNew(SHOT_PATH);
    auto prim = stage->OverridePrim(pxr::SdfPath("/SomeSphere"));

    stage->GetRootLayer()->InsertSubLayerPath(sequence);
    stage->GetRootLayer()->SetDocumentation("This shot takes the common settings from sequence.usda and adds to them.");

    auto variant = prim.GetVariantSet("some_variant_set");

    variant.AddVariant("variant_name_2");
    variant.SetVariantSelection("variant_name_2");

    auto sphere = pxr::UsdGeomSphere(prim);
    {
        pxr::UsdEditContext context {variant.GetVariantEditContext()};
        pxr::VtArray<pxr::GfVec3f> color {{0, 1, 0}};
        sphere.GetDisplayColorAttr().Set(color);
    }

    stage->Save();

    return SHOT_PATH;
}


int main() {
    auto asset = create_asset();
    auto sequence = create_sequence(asset);
    create_shot(sequence);

    return 0;
}
