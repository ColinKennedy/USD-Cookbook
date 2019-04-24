// IMPORT STANDARD LIBRARIES
#include <string>

// IMPORT THIRD-PARTY LIBRARIES
#include "pxr/usd/sdf/schema.h"
#include "pxr/usd/usd/stage.h"
#include "pxr/usd/usdGeom/sphere.h"


char const ASSET_PATH[] = "/tmp/asset.usda";
char const SEQUENCE_PATH[] = "/tmp/sequence.usda";
char const SHOT_PATH[] = "/tmp/shot.usda";


std::string create_asset() {
    auto stage = pxr::UsdStage::CreateNew(ASSET_PATH);
    auto sphere = pxr::UsdGeomSphere::Define(stage, pxr::SdfPath("/SomeSphere"));

    stage->GetRootLayer()->SetDocumentation("This file contains the \"character\" that will be changed in other layers.");

    stage->Save();

    return std::string(ASSET_PATH);
}


std::string create_sequence() {
    auto stage = pxr::UsdStage::CreateNew(SEQUENCE_PATH);
    auto prim = stage->OverridePrim(pxr::SdfPath("/SomeSphere"));

    stage->GetRootLayer()->SetDocumentation(
        "A common set of data for an entire sequence.");
    stage->SetMetadata(
        pxr::SdfFieldKeys->Comment, "We override the character to make it bigger and add some viewing option.");

    stage->Save();

    return std::string(SEQUENCE_PATH);
}

int main() {
    auto asset = create_asset();
    auto sequence = create_sequence();

    return 0;
}
