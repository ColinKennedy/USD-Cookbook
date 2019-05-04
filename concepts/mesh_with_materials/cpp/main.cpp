// IMPORT STANDARD LIBRARIES
#include <string>

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/base/tf/token.h>
#include <pxr/usd/kind/registry.h>
#include <pxr/usd/sdf/types.h>
#include <pxr/usd/usd/modelAPI.h>
#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usdGeom/mesh.h>
#include <pxr/usd/usdGeom/metrics.h>
#include <pxr/usd/usdGeom/tokens.h>
#include <pxr/usd/usdGeom/xform.h>


int attach_billboard(
    pxr::UsdStageRefPtr &stage,
    std::string const &root,
    std::string const &name="card"
) {
    auto billboard = pxr::UsdGeomMesh::Define(
        stage,
        pxr::SdfPath(root + "/" + name)
    );

    billboard.CreatePointsAttr(pxr::VtValue());
    billboard.CreateFaceVertexCountsAttr(pxr::VtValue());
    billboard.CreateFaceVertexIndicesAttr(pxr::VtValue());
    billboard.CreateExtentAttr(pxr::VtValue());
    auto coordinates = billboard.CreatePrimvar(
        "st",
        pxr::SdfValueTypeNames::TexCoord2fArray,
        pxr::UsdGeomTokens->varying

    )

    return 0;
}


int main() {
    auto stage = pxr::UsdStage::CreateInMemory("/tmp/simpleShading.usd");
    pxr::UsdGeomSetStageUpAxis(stage, pxr::TfToken("Y"));

    auto root = pxr::UsdGeomXform::Define(stage, pxr::SdfPath("/TexModel"));
    pxr::UsdModelAPI(root).SetKind(pxr::KindTokens->component);

    auto billboard = attach_billboard(stage, root.GetPath().GetString());
    return 0;
}
