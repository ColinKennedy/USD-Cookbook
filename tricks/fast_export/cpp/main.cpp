// IMPORT STANDARD LIBRARIES
#include <iostream>
#include <iterator>
#include <map>
#include <string>
#include <vector>

// IMPORT THIRD-PARTY LIBRARIES
#include "pxr/usd/pcp/primIndex.h"
#include "pxr/usd/sdf/layer.h"
#include "pxr/usd/sdf/primSpec.h"
#include "pxr/usd/sdf/types.h"
#include "pxr/usd/usd/stage.h"
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/join.hpp>


using Leaf = std::vector<std::string>;
using Names = std::map<std::string, Leaf>;
using PrimPaths = std::vector<std::string>;


static int const ITERATIONS = 1000;
static Names const PATHS = {
    {
        "BasePrim", {
            "InnerPrim", {"SiblingPrim"},
        },
    },
    {
        "SomePrim", {
            "AnotherInnerPrim",
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


void _create_prim_specs(pxr::SdfPrimSpecHandle root, Leaf const &leaf) {
    for (auto const &item : leaf) {
        pxr::SdfPrimSpec::New(root, item, pxr::SdfSpecifierDef);
    }
}


void _create_prim_specs(pxr::SdfPrimSpecHandle root, Names const &names) {
    for (auto const &item : names) {
        auto base = item.first;
        auto inner_names = item.second;

        auto base_prim_spec = pxr::SdfPrimSpec::New(root, base, pxr::SdfSpecifierDef);
        _create_prim_specs(base_prim_spec, inner_names);
    }
}


void _prepare_prim_specs_with_sdf(pxr::SdfLayerRefPtr &layer, Names const &paths) {
    _create_prim_specs(layer->GetPseudoRoot(), paths);
    auto parent = layer->GetPrimAtPath(pxr::SdfPath {"SomePrim/AnotherInnerPrim"});

    for (int index = 0; index < ITERATIONS; ++index) {
        pxr::SdfPrimSpec::New(parent, "IndexedPrim" + std::to_string(index), pxr::SdfSpecifierDef);
    }
}


void _prepare_prims_with_stage(pxr::UsdStageRefPtr const &stage) {
    for (auto const &path : _create_prims(PATHS)) {
        stage->DefinePrim(pxr::SdfPath {path});
    }

    auto indexed_template = "/SomePrim/AnotherInnerPrim/IndexedPrim";
    for (int index = 0; index < ITERATIONS; ++index) {
        stage->DefinePrim(pxr::SdfPath {indexed_template + std::to_string(index)});
    }
}


std::string create_using_sdf() {
    auto layer = pxr::SdfLayer::CreateAnonymous();

    // TODO : Adding / Removing this ChangeBlock doesn't change the time
    // much. Is a change block only useful when authoring opinions?
    //
    {
        pxr::SdfChangeBlock block;
        _prepare_prim_specs_with_sdf(layer, PATHS);
    }

    auto* result = new std::string();
    layer->ExportToString(result);
    // Assign the string to the stack so we can delete it off the heap and still return it
    auto value = *result;
    delete result;
    result = nullptr;

    return value;
}


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
    auto layer_export = create_using_sdf();

    std::vector<std::string> stage_export_lines;
    boost::split(stage_export_lines, stage_export, [](char character){return character == '\n';});
    stage_export_lines.erase(std::begin(stage_export_lines), std::begin(stage_export_lines) + 5);
    stage_export = boost::algorithm::join(stage_export_lines, "\n");

    std::vector<std::string> layer_export_lines;
    boost::split(layer_export_lines, layer_export, [](char character){return character == '\n';});
    layer_export_lines.erase(std::begin(layer_export_lines));
    layer_export = boost::algorithm::join(layer_export_lines, "\n");

    std::cout << "These exports should be exactly the same " << (stage_export == layer_export) << '\n';
    return 0;
}
