// IMPORT STANDARD LIBRARIES
#include <iostream>
#include <iterator>
#include <map>
#include <string>
#include <vector>

// IMPORT THIRD-PARTY LIBRARIES
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/join.hpp>
#include <pxr/base/tf/debug.h>
#include <pxr/base/tf/diagnostic.h>
#include <pxr/usd/pcp/primIndex.h>
#include <pxr/usd/sdf/layer.h>
#include <pxr/usd/sdf/primSpec.h>
#include <pxr/usd/sdf/types.h>
#include <pxr/usd/usd/stage.h>


PXR_NAMESPACE_OPEN_SCOPE
TF_DEBUG_CODES(
    PRIMSPEC_CREATED
);

TF_REGISTRY_FUNCTION(TfDebug)
{
    TF_DEBUG_ENVIRONMENT_SYMBOL(PRIMSPEC_CREATED, "Time functions that create Prims/PrimSpecs");
}
PXR_NAMESPACE_CLOSE_SCOPE

static int const ITERATIONS = 1000;
static pxr::SdfPathSet const PATHS {
    pxr::SdfPath {"/BasePrim"},
    pxr::SdfPath {"/BasePrim/InnerPrim"},
    pxr::SdfPath {"/BasePrim/InnerPrim/SiblingPrim"},
    pxr::SdfPath {"/SomePrim"},
    pxr::SdfPath {"/SomePrim/AnotherInnerPrim"},
    pxr::SdfPath {"/SomePrim/ChildPrim"},
    pxr::SdfPath {"/SomePrim/SiblingPrim"},
};


PXR_NAMESPACE_OPEN_SCOPE
void _prepare_prim_specs_with_sdf(pxr::SdfLayerRefPtr &layer, pxr::SdfPathSet const &paths) {
    {
        TF_DEBUG_TIMED_SCOPE(
            PRIMSPEC_CREATED,
            "The time it took to create layers with the Sdf API"
        );

        for (auto const &path : paths) {
            auto prim_spec = pxr::SdfCreatePrimInLayer(layer, path);
            prim_spec->SetSpecifier(pxr::SdfSpecifierDef);
        }

        auto parent = layer->GetPrimAtPath(pxr::SdfPath {"SomePrim/AnotherInnerPrim"});
        for (int index = 0; index < ITERATIONS; ++index) {
            pxr::SdfPrimSpec::New(parent, "IndexedPrim" + std::to_string(index), pxr::SdfSpecifierDef);
        }
    }
}


void _prepare_prims_with_stage(pxr::UsdStageRefPtr const &stage) {
    {
        TF_DEBUG_TIMED_SCOPE(
            PRIMSPEC_CREATED,
            "The time it took to create layers with the Usd API"
        );

        for (auto const &path : PATHS) {
            stage->DefinePrim(path);
        }

        auto indexed_template = "/SomePrim/AnotherInnerPrim/IndexedPrim";
        for (int index = 0; index < ITERATIONS; ++index) {
            stage->DefinePrim(pxr::SdfPath {indexed_template + std::to_string(index)});
        }
    }
}
PXR_NAMESPACE_CLOSE_SCOPE


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
    stage->GetRootLayer()->ExportToString(result);
    // Assign the string to the stack so we can delete it off the heap and still return it
    auto value = *result;
    delete result;
    result = nullptr;

    return value;
}


int main() {
    pxr::TfDebug::SetDebugSymbolsByName("PRIMSPEC_CREATED", true);
    auto stage_export = create_using_stage();
    auto layer_export = create_using_sdf();
    pxr::TfDebug::SetDebugSymbolsByName("PRIMSPEC_CREATED", false);

    std::vector<std::string> stage_export_lines;
    boost::split(stage_export_lines, stage_export, [](char character){return character == '\n';});
    stage_export_lines.erase(std::begin(stage_export_lines), std::begin(stage_export_lines) + 1);
    stage_export = boost::algorithm::join(stage_export_lines, "\n");

    std::vector<std::string> layer_export_lines;
    boost::split(layer_export_lines, layer_export, [](char character){return character == '\n';});
    layer_export_lines.erase(std::begin(layer_export_lines));
    layer_export = boost::algorithm::join(layer_export_lines, "\n");

    std::cout << std::boolalpha;
    std::cout << "These exports should be exactly the same " << (stage_export == layer_export) << '\n';
    return 0;
}
