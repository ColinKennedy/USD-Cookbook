#include <iostream>
#include <string>

#include <pxr/usd/sdf/path.h>
#include <pxr/usd/usd/editContext.h>
#include <pxr/usd/usd/editTarget.h>
#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usdGeom/sphere.h>


pxr::UsdStageRefPtr _make_target()
{
    auto stage = pxr::UsdStage::CreateInMemory();
    auto root = pxr::UsdGeomSphere::Define(stage, pxr::SdfPath{"/root"});
    pxr::UsdGeomSphere::Define(stage, pxr::SdfPath{"/root/sphere"});
    stage->SetDefaultPrim(root.GetPrim());

    return stage;
}

int main() {
    auto inner_stage = _make_target();
    auto main_stage = pxr::UsdStage::CreateInMemory();

    // XXX : In order to use `inner_stage` in an EditContext, it must be
    // in `main_stage`'s local LayerStack (e.g. it must be a sublayer)
    //
    main_stage->GetRootLayer()->GetSubLayerPaths().push_back(
        inner_stage->GetRootLayer()->GetIdentifier()
    );

    auto* result = new std::string();
    main_stage->GetRootLayer()->ExportToString(result);
    std::cout << *result << std::endl;

    std::cout << "Inner stage before context\n";
    inner_stage->GetRootLayer()->ExportToString(result);
    std::cout << *result << std::endl;

    {
        pxr::UsdEditContext context {main_stage, inner_stage->GetRootLayer()};
        auto sphere = pxr::UsdGeomSphere(main_stage->GetPrimAtPath(pxr::SdfPath{"/root/sphere"}));
        sphere.GetRadiusAttr().Set(10.0);
    }

    std::cout << "Inner stage after context\n";
    inner_stage->GetRootLayer()->ExportToString(result);
    std::cout << *result << std::endl;

    main_stage->SetEditTarget(pxr::UsdEditTarget(inner_stage->GetRootLayer()));
    auto sphere = pxr::UsdGeomSphere(main_stage->GetPrimAtPath(pxr::SdfPath{"/root/sphere"}));
    sphere.GetRadiusAttr().Set(5.0);

    std::cout << "Inner stage after setting\n";
    inner_stage->GetRootLayer()->ExportToString(result);
    std::cout << *result << std::endl;

    delete result;
    result = nullptr;

    return 0;
}
