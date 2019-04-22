// IMPORT STANDARD LIBRARIES
#include <cstdio>
#include <string>

// IMPORT THIRD-PARTY LIBRARIES
#include "pxr/usd/sdf/layer.h"
#include "pxr/usd/usd/stage.h"
#include "pxr/usd/usdGeom/sphere.h"


constexpr char TEMPORARY_BASIC_STAGE[] = "/tmp/mytemp.usda";


void create_basic_stage(std::string const &path) {
    auto stage = pxr::UsdStage::CreateNew(path);
    auto sphere = pxr::UsdGeomSphere::Define(stage, pxr::SdfPath("/SomeSphere"));


    stage->Save();
}

int main() {
    std::string path {TEMPORARY_BASIC_STAGE};
    create_basic_stage(path);
    // pxr::UsdStage::Create
    return 0;
}
