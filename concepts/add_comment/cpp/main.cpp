// IMPORT STANDARD LIBRARIES
#include <iostream>
#include <string>

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usdGeom/sphere.h>


int main() {
    auto stage = pxr::UsdStage::CreateInMemory();
    stage->GetRootLayer()->SetDocumentation("This is an example of adding a comment. You can add comments inside any pair of ()s");

    auto sphere = pxr::UsdGeomSphere::Define(stage, pxr::SdfPath("/SomeSphere"));
    sphere.GetPrim().SetMetadata(
        pxr::SdfFieldKeys->Comment,
        "I am a comment"
    );

    auto* result = new std::string();
    stage->GetRootLayer()->ExportToString(result);
    std::cout << *result << std::endl;
    delete result;
    result = nullptr;

    return 0;
}
