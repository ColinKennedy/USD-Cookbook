// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/usd/usd/specializes.h>
#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usdGeom/sphere.h>


int main() {
    auto stage = pxr::UsdStage::CreateInMemory();

    auto sphere = pxr::UsdGeomSphere::Define(stage, pxr::SdfPath {"/thing/SomethingElse/NestedEvenMore"});
    sphere.GetRadiusAttr().Set(4.0);

    auto prim = stage->DefinePrim(pxr::SdfPath("/thing/SomethingElse/SpecializedChild"));
    prim.GetSpecializes().AddSpecialize(sphere.GetPath());

    auto* result = new std::string();
    stage->GetRootLayer()->ExportToString(result);
    std::cout << *result << std::endl;
    delete result;
    result = nullptr;

    return 0;
}
