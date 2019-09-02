// IMPORT STANDARD LIBRARIES
#include <iostream>
#include <string>

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/usd/usd/primRange.h>
#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usdGeom/sphere.h>


char const BASE_STAGE_PATH[] = "/tmp/base.usda";
char const OVER_STAGE_PATH[] = "/tmp/over.usda";

std::string create_basic_stage() {
    auto stage = pxr::UsdStage::CreateNew(BASE_STAGE_PATH);
    auto sphere = pxr::UsdGeomSphere::Define(stage, pxr::SdfPath("/SomeSphere"));
    sphere.GetRadiusAttr().Set(4.0);

    stage->Save();

    return BASE_STAGE_PATH;
}


// This stage intentionally makes 1 over that actually defines something
// And then 3 other overs which do not override any concrete Prim
//
auto create_over_stage(std::string const &path) {
    auto stage = pxr::UsdStage::CreateNew(OVER_STAGE_PATH);

    stage->OverridePrim(pxr::SdfPath("/SomethingNameThatIsNotSomeSphere"));
    stage->OverridePrim(pxr::SdfPath("/AnotherOne"));
    stage->OverridePrim(pxr::SdfPath("/AnotherOne/AndAnotherOne"));
    stage->OverridePrim(pxr::SdfPath("/SomeSphere"));

    return stage;
}


int main() {
    auto base = create_basic_stage();
    auto stage = create_over_stage(base);

    // Method 1: Search everything and filter out only what you need This
    // method is the "best" because it crosses composition arcs and finds
    // nested overs even if they're layered between concrete Prims
    //
    for (auto const &prim : stage->TraverseAll()) {
        if (!prim.IsDefined()) {
            std::cout << prim.GetPath() << std::endl;
        }
    }

    // Method 2: Search all Layers in the stage, recursively (follows
    // payloads and other composition arcs but does not follow all Prims)
    //
    for (auto const &prim : stage->Traverse(!pxr::UsdPrimIsDefined)) {
        std::cout << prim.GetPath() << std::endl;
    }

    // Method 3: Search the opened stage Layer
    for (auto const &prim: pxr::UsdPrimRange::Stage(stage, !pxr::UsdPrimIsDefined)) {
        std::cout << prim.GetPath() << std::endl;
    }

    return 0;
}
