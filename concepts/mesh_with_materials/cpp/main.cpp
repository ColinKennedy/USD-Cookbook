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

    billboard.CreatePointsAttr(pxr::VtValue());
    billboard.CreateFaceVertexCountsAttr(pxr::VtValue());
    billboard.CreateFaceVertexIndicesAttr(pxr::VtValue());
    billboard.CreateExtentAttr(pxr::VtValue());

    auto coordinates = billboard.CreatePrimvar(
        pxr::TfToken("st"), pxr::SdfValueTypeNames->TexCoord2fArray,
        pxr::UsdGeomTokens->varying);

    // coordinates.Set();

    return billboard;
}

pxr::UsdShadeShader attach_surface_shader(pxr::UsdStageRefPtr &stage,
                                          pxr::UsdShadeMaterial material,
                                          pxr::SdfPath const &path) {
    auto shader = pxr::UsdShadeShader::Define(stage, path);
    shader.CreateIdAttr(pxr::VtValue("UsdPreviewSurface"));
    shader.CreateInput(pxr::TfToken("roughness"), pxr::SdfValueTypeNames->Float)
        .Set(0.4f);
    shader.CreateInput(pxr::TfToken("metallic"), pxr::SdfValueTypeNames->Float)
        .Set(0.0f);
    material.CreateSurfaceOutput().ConnectToSource(shader,
                                                   pxr::TfToken("surface"));

    return shader;
}

int attach_texture(pxr::UsdStageRefPtr &stage, pxr::UsdShadeShader shader,
                   std::string const &material_path,
                   std::string const reader_name = "stdReader",
                   std::string const shader_name = "diffuseTexture") {
    auto reader = pxr::UsdShadeShader::Define(
        stage, pxr::SdfPath(material_path + "/" + reader_name));
    reader.CreateIdAttr(pxr::VtValue("UsdPrimvarReader_float2"));

    auto sampler = pxr::UsdShadeShader::Define(
        stage, pxr::SdfPath(material_path + "/" + shader_name));

    return -1;
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
        stage, material,
        static_cast<pxr::SdfPath>(material_path + "/" + "PBRShader"));

    auto reader = attach_texture(stage, shader, material_path);

    return 0;
}
