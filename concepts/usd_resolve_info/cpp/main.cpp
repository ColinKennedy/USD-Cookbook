// IMPORT STANDARD LIBRARIES
#include <iostream>

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/base/tf/token.h>
#include <pxr/usd/sdf/path.h>
#include <pxr/usd/usd/attribute.h>
#include <pxr/usd/usd/stage.h>


int main() {
    auto stage = pxr::UsdStage::Open("../usd_resolve_info.usda");
    auto prim = stage->GetPrimAtPath(pxr::SdfPath{"/SomePrim"});

    std::cout << std::boolalpha;

    std::cout <<
        "value_clipped_property - Is value clip \"" <<
            (stage->GetPrimAtPath(pxr::SdfPath{"/PrimWithValueClips"})
            .GetAttribute(pxr::TfToken{"value_clipped_property"})
            .GetResolveInfo(1)
            .GetSource()
            == pxr::UsdResolveInfoSourceValueClips)
        << "\".\n";

    std::cout <<
        "time_samples_property - Is time samples \"" <<
        (
            prim.GetAttribute(pxr::TfToken{"time_samples_property"}).GetResolveInfo().GetSource()
            == pxr::UsdResolveInfoSourceTimeSamples
        )
        << "\".\n";

    std::cout <<
        "default_property - Is a default value \"" << (
            prim.GetAttribute(pxr::TfToken{"default_property"}).GetResolveInfo().GetSource()
            == pxr::UsdResolveInfoSourceDefault
        )
        << "\".\n";

    auto sphere = stage->GetPrimAtPath(pxr::SdfPath{"/SomeSphere"});

    std::cout <<
        "radius - Is a type fallback value \"" << (
            sphere.GetAttribute(pxr::TfToken{"radius"}).GetResolveInfo().GetSource()
            == pxr::UsdResolveInfoSourceFallback
        )
    << "\".\n";

    std::cout <<
        "xformOpOrder - Is empty value \"" << (
            prim.GetAttribute(pxr::TfToken{"xformOpOrder"}).GetResolveInfo().GetSource()
            == pxr::UsdResolveInfoSourceNone
        )
    << "\".\n";

    return 0;
}
