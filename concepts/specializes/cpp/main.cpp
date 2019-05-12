// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/usd/usd/specializes.h>
#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usdGeom/sphere.h>


int main() {
    auto stage = pxr::UsdStage::CreateInMemory();

    auto sphere = pxr::UsdGeomSphere(stage->DefinePrim(pxr::SdfPath("/thing/SomethingElse/NestedEvenMore"), pxr::TfToken("Sphere")));
    sphere.GetRadiusAttr().Set(4.0);

    auto prim = stage->DefinePrim(pxr::SdfPath("/thing/SomethingElse/SpecializedChild"));
    prim.GetSpecializes().AddSpecialize(sphere.GetPath());

    auto* result = new std::string();
    stage->ExportToString(result);
    std::cout << *result << std::endl;
    delete result;

    return 0;
}
