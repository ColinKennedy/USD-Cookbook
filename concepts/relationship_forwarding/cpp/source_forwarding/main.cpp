// IMPORT STANDARD LIBRARIES
#include <iostream>
#include <iterator>
#include <numeric>

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/usd/sdf/path.h>
#include <pxr/usd/usd/relationship.h>
#include <pxr/usd/usd/variantSets.h>
#include <pxr/usd/usd/stage.h>


std::ostream& operator<<(std::ostream &stream, pxr::SdfPathVector const &paths) {
    auto body_text = std::accumulate(
        std::begin(paths),
        std::end(paths),
        std::string {""},
        [](std::string text, pxr::SdfPath const &path) {
            std::string suffix;
            if (text.empty()) {
                suffix = "\"" + pxr::TfStringify(path) + "\"";
            } else {
                suffix = " \"" + pxr::TfStringify(path) + "\"";
            }
            return std::move(text) + suffix;
        }
    );
    return stream << "[" << body_text << "]";
}


int main() {
    auto stage = pxr::UsdStage::Open("../../../usda/source_forwarding.usda");
    auto prim = stage->GetPrimAtPath(pxr::SdfPath {"/SomePrim"});

    auto relationship = prim.GetRelationship(pxr::TfToken {"another"});
    pxr::SdfPathVector raw_targets;
    relationship.GetTargets(&raw_targets);
    std::cout << "This is the raw target value \"" << raw_targets << "\"\n";
    pxr::SdfPathVector forwarded_targets;
    relationship.GetForwardedTargets(&forwarded_targets);
    std::cout << "But this is the true location \"" << forwarded_targets << "\"\n";

    auto variant_sets = prim.GetVariantSets();
    auto variant_set = variant_sets.GetVariantSet("forwarding_variant_set");

    for (auto const &variant : variant_set.GetVariantNames()) {
        variant_set.SetVariantSelection(variant);
        pxr::SdfPathVector relationship_raw_targets;
        pxr::SdfPathVector relationship_forwarded_targets;
        relationship.GetTargets(&relationship_raw_targets);
        relationship.GetForwardedTargets(&relationship_forwarded_targets);

        std::cout << "This is the raw target value " << relationship_raw_targets << '\n';
        std::cout << "But this is the true location " << relationship_forwarded_targets << '\n';
    }

    return 0;
}
