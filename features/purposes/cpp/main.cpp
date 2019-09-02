// IMPORT STANDARD LIBRARIES
#include <string>

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/usd/sdf/path.h>
#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usdGeom/cone.h>
#include <pxr/usd/usdGeom/cube.h>
#include <pxr/usd/usdGeom/cylinder.h>
#include <pxr/usd/usdGeom/sphere.h>
#include <pxr/usd/usdGeom/xform.h>


int main() {
    auto stage = pxr::UsdStage::CreateInMemory();
    auto xform = pxr::UsdGeomXform::Define(stage, pxr::SdfPath("/Xform"));

    auto cube = pxr::UsdGeomCube::Define(stage, pxr::SdfPath("/Xform/SomeGuide"));
    auto purpose = cube.CreatePurposeAttr();
    purpose.Set(pxr::UsdGeomTokens->guide);

    auto sphere = pxr::UsdGeomSphere::Define(stage, pxr::SdfPath("/Xform/SomeRender"));
    purpose = sphere.CreatePurposeAttr();
    purpose.Set(pxr::UsdGeomTokens->render);

    auto cone = pxr::UsdGeomCone::Define(stage, pxr::SdfPath("/Xform/SomeProxy"));
    purpose = cone.CreatePurposeAttr();
    purpose.Set(pxr::UsdGeomTokens->proxy);

    auto cylinder = pxr::UsdGeomCylinder::Define(stage, pxr::SdfPath("/Xform/SomeDefault"));
    purpose = cylinder.CreatePurposeAttr();
    purpose.Set(pxr::UsdGeomTokens->default_);

    auto* result = new std::string();
    stage->GetRootLayer()->ExportToString(result);
    std::cout << *result << std::endl;
    delete result;
    result = nullptr;

    return 0;
}
