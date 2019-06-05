// IMPORT THIRD-PARTY LIBRARIES
#include "pxr/usd/sdf/attributeSpec.h"
#include "pxr/usd/sdf/layer.h"
#include "pxr/usd/sdf/primSpec.h"
#include "pxr/usd/sdf/types.h"
#include "pxr/usd/usdUtils/stitch.h"


int main() {
    auto weak_layer = pxr::SdfLayer::CreateAnonymous();
    auto weak_root = weak_layer->GetPseudoRoot();
    auto weak_prim = pxr::SdfPrimSpec::New(weak_root, "SomePrim", pxr::SdfSpecifierClass);
    auto some_attribute = pxr::SdfAttributeSpec::New(
        weak_prim, "some_attribute", pxr::SdfValueTypeNames->Bool
    );
    weak_layer->SetTimeSample(some_attribute->GetPath(), 0.0, true);
    weak_layer->SetTimeSample(some_attribute->GetPath(), 2.0, false);
    weak_layer->SetStartTimeCode(4);
    weak_layer->SetEndTimeCode(10);

    auto strong_layer = pxr::SdfLayer::CreateAnonymous();
    auto strong_root = strong_layer->GetPseudoRoot();
    auto strong_prim = pxr::SdfPrimSpec::New(strong_root, "SomePrim", pxr::SdfSpecifierOver);
    auto some_attribute1 = pxr::SdfAttributeSpec::New(
        strong_prim, "some_attribute", pxr::SdfValueTypeNames->Bool
    );
    strong_layer->SetTimeSample(some_attribute1->GetPath(), 0.0, false);
    strong_layer->SetTimeSample(some_attribute1->GetPath(), 1.0, true);
    strong_layer->SetStartTimeCode(8);
    strong_layer->SetEndTimeCode(20);

    // XXX : Stitching has different rules, depending on what is being stitched.
    //
    // - time samples use the minimum and maximum values of both layers
    // - dict keys in the strong layer are always preferred and missing
    // keys fall back to the weaker layer
    // - Same with time samples
    //
    // - Interestingly though, the specifier for the PrimSpec does weird things
    // e.g.
    // Scenario 1:
    //  `weak_layer` = Over
    //  `strong_layer` = Def
    //  Result: Def (strong_layer was preferred)
    //
    // Scenario 2:
    //  `weak_layer` = Def
    //  `strong_layer` = Over
    //  Result: Def (weak_layer was preferred)
    //
    // Scenario 3:
    //  `weak_layer` = Class
    //  `strong_layer` = Over
    //  Result: Class (weak_layer was preferred)
    //
    // Scenario 4:
    //  `weak_layer` = Class
    //  `strong_layer` = Def
    //  Result: Def (strong_layer was preferred)
    //
    // Most likely, specifiers have a strength order that StitchLayers
    // is using to merge it. It probably doesn't matter which layer is
    // strong or weak.
    //
    pxr::UsdUtilsStitchLayers(strong_layer, weak_layer);

    auto* result = new std::string();
    strong_layer->ExportToString(result);
    std::cout << *result << std::endl;
    delete result;
    result = nullptr;

    return 0;
}
