// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/usd/usd/clipsAPI.h>
#include <pxr/usd/usd/stage.h>


int main() {
    auto stage = pxr::UsdStage::CreateInMemory();
    stage->SetStartTimeCode(0);
    stage->SetEndTimeCode(12);

    auto prim = stage->DefinePrim(pxr::SdfPath("/Prim"));
    auto model = pxr::UsdClipsAPI(prim);
    model.SetClipActive({{0, 0}, {2, 1}});
    model.SetClipAssetPaths(
        {pxr::SdfAssetPath{"./clip_1.usda"}, pxr::SdfAssetPath{"./clip_2.usda"}}
    );
    model.SetClipPrimPath("/Clip");
    model.SetClipTimes({{0, 0}, {1, 1}, {2, 0}, {3, 1}});
    model.SetClipManifestAssetPath(pxr::SdfAssetPath{"./clip_manifest.usda"});

    prim.GetReferences().AddReference(
        "./ref.usda",
        pxr::SdfPath{"/Ref"}
    );

    auto* result = new std::string();
    stage->GetRootLayer()->ExportToString(result);
    std::cout << *result << std::endl;
    delete result;
    result = nullptr;

    return 0;
}
