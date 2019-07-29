#include <algorithm>
#include <iostream>
#include <vector>

#include <pxr/base/tf/token.h>
#include <pxr/usd/usd/attribute.h>
#include <pxr/usd/usd/prim.h>
#include <pxr/usd/usd/primRange.h>
#include <pxr/usd/usd/references.h>
#include <pxr/usd/usd/stage.h>


auto create_basic_instance_stage() {
    auto stage = pxr::UsdStage::CreateInMemory();

    auto car = stage->CreateClassPrim(pxr::SdfPath {"/Car"});
    car.CreateAttribute(pxr::TfToken {"color"}, pxr::SdfValueTypeNames->Color3f).Set(pxr::GfVec3f {0, 0, 0});
    auto body = stage->DefinePrim(pxr::SdfPath {"/Car/Body"});
    body.CreateAttribute(pxr::TfToken {"color"}, pxr::SdfValueTypeNames->Color3f).Set(pxr::GfVec3f {0, 0, 0});
    stage->DefinePrim(pxr::SdfPath {"/Car/Door"});

    std::vector<pxr::SdfPath> paths {
        pxr::SdfPath {"/ParkingLot/Car_1"},
        pxr::SdfPath {"/ParkingLot/Car_2"},
        pxr::SdfPath {"/ParkingLot/Car_n"},
    };

    for (auto const &path : paths) {
        auto prim = stage->DefinePrim(path);
        prim.SetInstanceable(true);
        prim.GetReferences().AddReference("", car.GetPath());
    }

    return stage;
}


std::vector<pxr::UsdPrim> traverse_instanced_children(pxr::UsdPrim const &prim) {
    std::vector<pxr::UsdPrim> prims;

    auto range = prim.GetFilteredChildren(pxr::UsdTraverseInstanceProxies());
    prims.insert(std::end(prims), std::begin(range), std::end(range));

    for (auto const &child : range) {
        auto subchild_range = traverse_instanced_children(child);
        prims.reserve(subchild_range.size());
        prims.insert(std::end(prims), std::begin(subchild_range), std::end(subchild_range));
    }

    return prims;
}


int main() {
    auto stage = create_basic_instance_stage();

    auto traverse = stage->TraverseAll();
    std::vector<pxr::UsdPrim> all_uninstanced_prims;
    all_uninstanced_prims.insert(std::end(all_uninstanced_prims), std::begin(traverse), std::end(traverse));

    auto all_prims_including_child_prims = traverse_instanced_children(stage->GetPseudoRoot());

    std::sort(std::begin(all_prims_including_child_prims), std::end(all_prims_including_child_prims));

    // XXX : This print statement should say "3", because `TraverseAll`
    // includes class Prims whereas `traverse_instanced_children`
    // currently does not. But `traverse_instanced_children` also finds
    // all of the instanced children, which is why there's still more
    //
    std::cout << "The instanced Prims list found \"" << all_prims_including_child_prims.size() - all_uninstanced_prims.size() << "\" more Prims than TraverseAll.\n";

    for (auto const &prim : all_uninstanced_prims) {
        std::cout << prim.GetPath() << std::endl;
    }


    return 0;
}
