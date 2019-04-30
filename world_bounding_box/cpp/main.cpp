// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/base/tf/token.h>
#include <pxr/usd/sdf/path.h>
#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usdGeom/sphere.h>
#include <pxr/usd/usdGeom/bboxCache.h>


int main() {
    auto stage = pxr::UsdStage::CreateInMemory();
    auto sphere = pxr::UsdGeomSphere::Define(stage, pxr::SdfPath("/SomeSphere"));
    sphere.AddTranslateOp().Set(pxr::GfVec3d(20, 30, 40));

    auto bounds = pxr::UsdGeomImageable(sphere).ComputeWorldBound(
        pxr::UsdTimeCode(1),
        pxr::TfToken("default")
    );
    std::cout << bounds << std::endl;

    auto cache = pxr::UsdGeomBBoxCache(
        pxr::UsdTimeCode().Default(),
        pxr::UsdGeomImageable::GetOrderedPurposeTokens()
    );

    std::cout << cache.ComputeWorldBound(sphere.GetPrim()) << std::endl;

    return 0;
}
