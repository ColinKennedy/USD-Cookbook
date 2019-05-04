// IMPORT STANDARD LIBRARIES
#include <string>

// IMPORT THIRD-PARTY LIBRARIES
#include "pxr/usd/usdShade/material.h"
#include <pxr/base/tf/token.h>
#include <pxr/usd/kind/registry.h>
#include <pxr/usd/sdf/types.h>
#include <pxr/usd/usd/modelAPI.h>
#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usdGeom/mesh.h>
#include <pxr/usd/usdGeom/metrics.h>
#include <pxr/usd/usdGeom/tokens.h>
#include <pxr/usd/usdGeom/xform.h>


pxr::UsdGeomMesh attach_billboard(pxr::UsdStageRefPtr &stage,
                                  std::string const &root,
                                  std::string const &name = "card") {
    auto billboard =
        pxr::UsdGeomMesh::Define(stage, pxr::SdfPath(root + "/" + name));

    // billboard.CreatePointsAttr(pxr::VtValue());
    // billboard.CreateFaceVertexCountsAttr(pxr::VtValue());
    // billboard.CreateFaceVertexIndicesAttr(pxr::VtValue());
    // billboard.CreateExtentAttr(pxr::VtValue());
    //
    // auto coordinates = billboard.CreatePrimvar(
    //     pxr::TfToken("st"),
    //     pxr::SdfValueTypeNames->TexCoord2fArray,
    //     pxr::UsdGeomTokens->varying
    // );

    // coordinates.Set();

    return billboard;
}


int attach_surface_shader(
        pxr::UsdStageRefPtr &stage,
        pxr::UsdShadeMaterial material,
        std::string const &root,
)
{
    // shader = UsdShade.Shader.Define(stage, path)
    // shader.CreateIdAttr("UsdPreviewSurface")
    // shader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.4)
    // shader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)
    //
    // material.CreateSurfaceOutput().ConnectToSource(shader, "surface")
    //
    // return shader

    return 0;
}


int attach_texture(
        pxr::UsdStageRefPtr &stage,
        pxr::UsdShadeMaterial material,
        std::string const &root,
        std::string const reader_name="stdReader",
        std::string const shader_name="diffuseTexture",
)
{
    auto reader = pxr::UsdShadeShader::Define(stage, pxr::SdfPath(root + "/" + reader_name));
    reader.CreateIdAttr("UsdPrimvarReader_float2");

    auto sampler = pxr::UsdShadeShader::Define(stage,)
}


int main() {
    auto stage = pxr::UsdStage::CreateInMemory("/tmp/simpleShading.usd");
    pxr::UsdGeomSetStageUpAxis(stage, pxr::TfToken("Y"));

    auto root = pxr::UsdGeomXform::Define(stage, pxr::SdfPath("/TexModel"));
    pxr::UsdModelAPI(root).SetKind(pxr::KindTokens->component);

    auto billboard = attach_billboard(stage, root.GetPath().GetString());
    auto material = pxr::UsdShadeMaterial::Define(
        stage,
        pxr::SdfPath(billboard.GetPath().GetString() + "/" + "boardMat"));

    auto material_path = material.GetPath().GetString();
    auto shader = attach_surface_shader(
        stage,
        material,
        material_path + "/" + "PBRShader"
    );
    auto reader = attach_texture(stage, shader, material_path);


    return 0;
}
