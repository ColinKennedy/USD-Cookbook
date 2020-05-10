// IMPORT STANDARD LIBRARIES
#include <iostream>
#include <string>

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/base/vt/array.h>
#include <pxr/base/vt/dictionary.h>
#include <pxr/usd/sdf/assetPath.h>
#include <pxr/usd/sdf/path.h>
#include <pxr/usd/usd/modelAPI.h>
#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usdGeom/sphere.h>


int main() {
    auto stage = pxr::UsdStage::CreateInMemory();
    auto some_sphere = pxr::UsdGeomSphere::Define(stage, pxr::SdfPath("/SomeSphere"));

    // Method A: Set using methods
    auto model = pxr::UsdModelAPI(some_sphere.GetPrim());
    model.SetAssetName("some_asset");
    model.SetAssetVersion("v1");
    model.SetAssetIdentifier(pxr::SdfAssetPath("some/path/to/file.usda"));
    model.SetPayloadAssetDependencies(pxr::VtArray<pxr::SdfAssetPath> {
        pxr::SdfAssetPath("something.usd"),
        pxr::SdfAssetPath("another/thing.usd"),
    });

    // Method B: Set-by-key
    auto another_sphere = pxr::UsdGeomSphere::Define(stage, pxr::SdfPath("/AnotherSphere"));
    auto another_prim = another_sphere.GetPrim();
    another_prim.SetAssetInfoByKey(
        pxr::UsdModelAPIAssetInfoKeys->version,
        pxr::VtValue("v1")
    );
    another_prim.SetAssetInfoByKey(
        pxr::UsdModelAPIAssetInfoKeys->name,
        pxr::VtValue("some_asset")
    );
    another_prim.SetAssetInfoByKey(
        pxr::UsdModelAPIAssetInfoKeys->identifier,
        pxr::VtValue("some/path/to/file.usda")
    );
    another_prim.SetAssetInfoByKey(
        pxr::UsdModelAPIAssetInfoKeys->payloadAssetDependencies,
        pxr::VtValue{pxr::VtArray<pxr::SdfAssetPath> {
            pxr::SdfAssetPath("something.usd"),
            pxr::SdfAssetPath("another/thing.usd"),
        }}
    );

    // Method C: Set-by-dict
    auto last_sphere = pxr::UsdGeomSphere::Define(stage, pxr::SdfPath("/LastSphere"));
    last_sphere.GetPrim().SetAssetInfo(pxr::VtDictionary {
            {pxr::TfToken("identifier"), pxr::VtValue("some/path/to/file.usda")},
            {pxr::TfToken("name"), pxr::VtValue("some_asset")},
            {pxr::TfToken("version"), pxr::VtValue("v1")},
            {pxr::TfToken("payloadAssetDependencies"), pxr::VtValue{pxr::VtArray<pxr::SdfAssetPath> {
                pxr::SdfAssetPath("something.usd"),
                pxr::SdfAssetPath("another/thing.usd"),
            }}}
        }
    );

    auto* result = new std::string();
    stage->GetRootLayer()->ExportToString(result);
    std::cout << *result << std::endl;
    delete result;
    result = nullptr;

    return 0;
}
