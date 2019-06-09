// IMPORT STANDARD LIBRARIES
#include <iostream>
#include <string>

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/base/tf/token.h>
#include <pxr/usd/kind/registry.h>
#include <pxr/usd/usd/modelAPI.h>
#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usdGeom/sphere.h>


int main() {
    auto stage = pxr::UsdStage::CreateInMemory();
    stage->GetRootLayer()->SetDocumentation("This is an example of setting a Model Prim kind");

    auto sphere1 = pxr::UsdGeomSphere::Define(stage, pxr::SdfPath("/SomeSphere"));
    pxr::UsdModelAPI(sphere1).SetKind(pxr::KindTokens->component);
    auto sphere2 = pxr::UsdGeomSphere::Define(stage, pxr::SdfPath("/SomeSphere/SphereChild"));
    pxr::UsdModelAPI(sphere2).SetKind(pxr::KindTokens->subcomponent);
    auto sphere3 = pxr::UsdGeomSphere::Define(stage, pxr::SdfPath("/SomeSphere/Foo"));
    pxr::UsdModelAPI(sphere3).SetKind(pxr::TfToken("does_not_exist"));
    sphere3.GetPrim().SetMetadata(
        pxr::SdfFieldKeys->Comment,
        "XXX: This kind is made up. But it could be real if we added to the KindRegistry\nhttps://graphics.pixar.com/usd/docs/api/class_kind_registry.html"
    );

    auto* result = new std::string();
    stage->GetRootLayer()->ExportToString(result);
    std::cout << *result << std::endl;
    delete result;
    result = nullptr;

    return 0;
}
