// IMPORT STANDARD LIBRARIES
#include <iostream>
#include <iterator>
#include <map>
#include <string>
#include <vector>

// IMPORT THIRD-PARTY LIBRARIES
#include "pxr/usd/sdf/layer.h"
#include "pxr/usd/usd/stage.h"


using Leaf = std::vector<std::string>;
using Names = std::map<std::string, Leaf>;
using PrimPaths = std::vector<std::string>;


static Names const PATH = {
    {
        "BasePrim", {
            "InnerPrim", {"SiblingPrim"},
        },
    },
    {
        "SomePrim", {
            "AnnotherInnerPrim",
            "ChildPrim",
            "SiblingPrim",
        }
    },
};


PrimPaths _create_prims(Leaf const &leaf, std::string const &parent=std::string {}) {
    Leaf output;
    output.reserve(leaf.size());
    for (auto const &name : leaf) {
        output.emplace_back(parent + "/" + name) ;
    }

    return output;
}


PrimPaths _create_prims(Names const &names, std::string const &parent=std::string {}) {
    PrimPaths output;
    output.reserve(names.size());
    for (auto item : names) {
        auto base = item.first;
        auto inner_names = item.second;
        auto base_prim_spec = parent + "/" + base;
        output.push_back(base_prim_spec);

        auto inner_prims = _create_prims(inner_names, base_prim_spec);
        output.reserve(inner_prims.size());
        output.insert(std::end(output), std::begin(inner_prims), std::end(inner_prims));
    }

    return output;
}


void _prepare_prims_with_stage(pxr::UsdStageRefPtr const &stage) {
    for (auto const &path : _create_prims(PATH)) {
        stage->DefinePrim(pxr::SdfPath {path});
    }
}


// std::string create_using_sdf() {
//     auto layer = pxr::SdfLayer::CreateAnonymous();
//
//     // TODO : Adding / Removing this ChangeBlock doesn't change the time
//     // much. Is a change block only useful when authoring opinions?
//     //
//     {
//         pxr::SdfChangeBlock block;
//         _prepate_prims_with_sdf(layer, PATHS);
//     }
//
//     return layer->ExportToString();
// }


std::string create_using_stage() {
    auto stage = pxr::UsdStage::CreateInMemory();
    _prepare_prims_with_stage(stage);

    auto* result = new std::string();
    stage->ExportToString(result);
    // Assign the string to the stack so we can delete it off the heap and still return it
    auto value = *result;
    delete result;
    result = nullptr;

    return value;
}


int main() {
    auto stage_export = create_using_stage();
    // auto layer_export = create_using_sdf();
    //
    std::cout << stage_export << '\n';
    // std::cout << "These exports should be exactly the same" << (stage_export == layer_export) << '\n';
    return 0;
}
