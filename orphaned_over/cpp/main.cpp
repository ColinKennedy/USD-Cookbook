// IMPORT STANDARD LIBRARIES
#include <iostream>
#include <string>

// IMPORT THIRD-PARTY LIBRARIES
#include "pxr/usd/usd/primRange.h"
#include "pxr/usd/usd/stage.h"
#include "pxr/usd/usdGeom/sphere.h"


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

    auto over1 = stage->OverridePrim(pxr::SdfPath("/SomethingNameThatIsNotSomeSphere"));
    auto sphere1 = pxr::UsdGeomSphere(over1);
    sphere1.GetRadiusAttr().Set(4.0);

    auto over2 = stage->OverridePrim(pxr::SdfPath("/AnotherOne"));
    auto sphere2 = pxr::UsdGeomSphere(over2);
    sphere2.GetRadiusAttr().Set(5.0);

    auto over3 = stage->OverridePrim(pxr::SdfPath("/AnotherOne/AndAnotherOne"));
    auto sphere3 = pxr::UsdGeomSphere(over3);
    sphere3.GetRadiusAttr().Set(10.0);

    auto over4 = stage->OverridePrim(pxr::SdfPath("SomeSphere"));
    auto sphere4 = pxr::UsdGeomSphere(over4);
    sphere4.GetRadiusAttr().Set(10.0);

    return stage;
}


int main() {
    auto base = create_basic_stage();
    auto stage = create_over_stage(base);

    for (auto foo: pxr::UsdPrimRange::Stage(stage, !pxr::UsdPrimIsDefined)) {
        std::cout << foo.GetPath() << std::endl;
    }

    return 0;
}
