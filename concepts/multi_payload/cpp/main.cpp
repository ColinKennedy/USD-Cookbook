/* This module shows how to load 2+ Payloads on a single Prim.
 *
 * The short answer is - add a Payload to 2+ Prims and then Reference
 * those Prims onto a single Prim. Then that container Prim with all the
 * references will get each Payload.
 *
 * Also note: This module isn't going to run directly in usdview because
 * we're using anonymous layers. So see an actual example, look at the
 * nearby "usda" folder.
 *
 */

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/usd/sdf/path.h>
#include <pxr/usd/usd/payloads.h>
#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usdGeom/cube.h>
#include <pxr/usd/usdGeom/sphere.h>
#include <pxr/usd/usdGeom/xform.h>


std::string _create_cube_payload() {
    auto stage = pxr::UsdStage::CreateInMemory();
    pxr::UsdGeomCube::Define(stage, pxr::SdfPath {"/PayloadCubeThing"});
    pxr::UsdGeomCube::Define(stage, pxr::SdfPath {"/PaylodaCubeThing/PayloadCube"});

    return stage->GetRootLayer()->GetIdentifier();
}


pxr::UsdGeomXform create_cube_base_stage(pxr::UsdStagePtr const &stage) {
    auto payload = _create_cube_payload();
    auto xform = pxr::UsdGeomXform::Define(stage, pxr::SdfPath {"/SomeXformSphere"});
    xform.GetPrim().GetPayloads().AddPayload(payload, pxr::SdfPath {"/PayloadSphereThing"});

    return xform;
}


std::string _create_sphere_payload() {
    auto stage = pxr::UsdStage::CreateInMemory();
    pxr::UsdGeomSphere::Define(stage, pxr::SdfPath {"/PayloadSphereThing"});
    pxr::UsdGeomSphere::Define(stage, pxr::SdfPath {"/PaylodaSphereThing/PayloadSphere"});

    return stage->GetRootLayer()->GetIdentifier();
}


pxr::UsdGeomXform create_sphere_base_stage(pxr::UsdStagePtr const &stage) {
    auto payload = _create_sphere_payload();
    auto xform = pxr::UsdGeomXform::Define(stage, pxr::SdfPath {"/SomeXformSphere"});
    xform.GetPrim().GetPayloads().AddPayload(payload, pxr::SdfPath {"/PayloadSphereThing"});

    return xform;
}


int main() {
    auto stage = pxr::UsdStage::CreateInMemory();
    auto cube = create_cube_base_stage(stage);
    auto sphere = create_sphere_base_stage(stage);
    auto xform = pxr::UsdGeomXform::Define(stage, pxr::SdfPath {"/SomeTransform"});
    xform.GetPrim().GetReferences().AddReference(
        "", pxr::SdfPath {"/SomeXformCube"}
    );

    xform.GetPrim().GetReferences().AddReference(
        "", pxr::SdfPath {"/SomeXformSphere"}
    );

    auto* result = new std::string();
    stage->GetRootLayer()->ExportToString(result);
    std::cout << *result << std::endl;
    delete result;
    result = nullptr;

    return 0;
}
