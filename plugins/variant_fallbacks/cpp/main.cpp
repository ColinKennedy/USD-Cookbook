// IMPORT STANDARD LIBRARIES
#include <iostream>

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usd/variantSets.h>


// Run the main execution of the current script.
//
// Important:
//     As mentioned in the `variant_fallbacks/README.md` file, variant
//     fallbacks are determined per-stage exactly when the stage is first
//     created.
//
//     Most projects in this repository use stages that only exist in
//     memory but, in this case, it's easier to provide Prims up-front by
//     reading and existing USD file instead of creating one, from scratch.
//
int main() {
    auto stage = pxr::UsdStage::Open("../example_file/variant_set_with_no_authored_selection.usda");

    auto prim = stage->DefinePrim(pxr::SdfPath {"/SomePrim"});
    auto variant_set = prim.GetVariantSets().GetVariantSet("some_variant_set_name");

    std::cout
        << "The currently-selected variant (which should be \"foo\"): \""
        << variant_set.GetVariantSelection()
        << "\"\n";

    return 0;
}
