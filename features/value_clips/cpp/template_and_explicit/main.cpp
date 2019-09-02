// IMPORT STANDARD LIBRARIES
#include <iostream>
#include <string>

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/usd/usd/clipsAPI.h>
#include <pxr/usd/sdf/types.h>
#include <pxr/usd/usd/stage.h>


int main() {
    auto stage = pxr::UsdStage::CreateInMemory();
    stage->SetStartTimeCode(0);
    stage->SetEndTimeCode(2);

    auto prim = stage->DefinePrim(pxr::SdfPath("/Set"));
    std::string non_template_set_name {"non_template_clips"};
    auto model = pxr::UsdClipsAPI(prim);
    model.SetClipActive({{0.0, 0}}, non_template_set_name);
    model.SetClipAssetPaths(
        {pxr::SdfAssetPath{"./non_template_clip.usda"}},
        non_template_set_name
    );
    model.SetClipPrimPath("/NonTemplate", non_template_set_name);

    std::string template_set_name {"template_clips"};
    model.SetClipTemplateAssetPath("./template_clip.##.usda", template_set_name);
    model.SetClipTemplateEndTime(2);
    model.SetClipTemplateStartTime(0);
    model.SetClipTemplateStride(1, template_set_name);
    model.SetClipPrimPath("/Template", template_set_name);

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
