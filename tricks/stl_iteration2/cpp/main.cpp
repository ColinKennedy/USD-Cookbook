// IMPORT STANDARD LIBRARIES
#include <iostream>
#include <iterator>
#include <numeric>
#include <string>

// IMPORT THIRD-PARTY LIBRARIES
#include <boost/range/adaptors.hpp>
#include <pxr/usd/kind/registry.h>
#include <pxr/usd/sdf/path.h>
#include <pxr/usd/usd/modelAPI.h>
#include <pxr/usd/usd/primRange.h>
#include <pxr/usd/usd/stage.h>

class is_positive_number {
    public:
          bool operator()(pxr::UsdPrim const &prim) { return true; }
};


int main() {
    using FilterIter = boost::filter_iterator<is_positive_number, pxr::UsdPrimRange>;

    auto stage = pxr::UsdStage::CreateInMemory();
    stage->DefinePrim(pxr::SdfPath {"/SomeSphere"});
    stage->DefinePrim(pxr::SdfPath {"/AnotherSphere"});
    stage->DefinePrim(pxr::SdfPath {"/AnotherSphere/Here"});
    auto range = pxr::UsdPrimRange::Stage(stage);

    for (auto const &prim : range | boost::adaptors::filtered([](pxr::UsdPrim const &prim) {
        return prim.GetPath().GetName() == "AnotherSphere";
    })) {
        pxr::UsdModelAPI(prim).SetKind(pxr::KindTokens->component);
    }

    auto* result = new std::string();
    stage->GetRootLayer()->ExportToString(result);
    std::cout << *result << std::endl;
    delete result;
    result = nullptr;

    return 0;
}
