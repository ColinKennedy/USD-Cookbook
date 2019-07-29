// IMPORT STANDARD LIBRARIES
#include <iostream>
#include <iterator>
#include <numeric>
#include <string>

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/usd/kind/registry.h>
#include <pxr/usd/sdf/path.h>
#include <pxr/usd/usd/modelAPI.h>
#include <pxr/usd/usd/primRange.h>
#include <pxr/usd/usd/stage.h>


int main() {
    auto stage = pxr::UsdStage::CreateInMemory();
    stage->DefinePrim(pxr::SdfPath {"/SomeSphere"});
    stage->DefinePrim(pxr::SdfPath {"/AnotherSphere"});
    auto range = pxr::UsdPrimRange::Stage(stage);

    // Get every prim using accumulate
    auto text = std::accumulate(
        std::begin(range),
        std::end(range),
        std::string {"Prims:"},
        [](std::string text, pxr::UsdPrim const &prim) {
            return std::move(text) + "\n" + pxr::TfStringify(prim.GetPath());
        }
    );

    std::cout << text << "\n\n";

    // XXX : This is a bit strange but `prim` must be `pxr::UsdPrim
    // const` on my machine, even though we immediately wrap it in
    // UsdModelAPI and change the Prim's Kind.
    //
    std::for_each(std::begin(range), std::end(range), [](pxr::UsdPrim const &prim){
        pxr::UsdModelAPI(prim).SetKind(pxr::KindTokens->component);
    });
    auto* result = new std::string();
    stage->GetRootLayer()->ExportToString(result);
    std::cout << *result << std::endl;
    delete result;
    result = nullptr;

    return 0;
}
