// IMPORT STANDARD LIBRARIES
#include <iostream>
#include <string>

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/base/vt/types.h>
#include <pxr/usd/sdf/layer.h>
#include <pxr/usd/sdf/primSpec.h>


int main() {
    auto layer = pxr::SdfLayer::CreateAnonymous();

    auto primspec = pxr::SdfCreatePrimInLayer(layer, pxr::SdfPath {"/SomePrim"});
    auto fallback = pxr::SdfSchema::GetInstance().GetFallback(pxr::TfToken {"my_custom_double"});

    assert(fallback == 12.0 && "Plugin Metadata was not sourced correctly");
    assert(layer->GetPseudoRoot()->GetFallbackForInfo(pxr::TfToken {"another_metadata"}) == pxr::VtDoubleArray({5.0, 13.0}) && "Plugin Metadata was not sourced correctly");

    std::cout << "The Plugin Metadata file is included correctly\n";

    return 0;
}
