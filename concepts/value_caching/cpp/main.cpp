// IMPORT STANDARD LIBRARIES
#include <chrono>
#include <functional>
#include <iostream>
#include <vector>

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/usd/usd/attribute.h>
#include <pxr/usd/usd/attributeQuery.h>
#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usdGeom/sphere.h>

// IMPORT LOCAL LIBRARIES
#include "./forwarder.h"

static unsigned int const REPEATS = 1000;


pxr::UsdStageRefPtr _create_basic_scene() {
    auto stage = pxr::UsdStage::CreateInMemory();
    auto sphere = pxr::UsdGeomSphere::Define(stage, pxr::SdfPath{"/Some/Prim"});
    sphere.GetRadiusAttr().Set(10.0);

    auto another = pxr::UsdStage::CreateInMemory();
    another->GetRootLayer()->GetSubLayerPaths().push_back(
        stage->GetRootLayer()->GetIdentifier()
    );
    auto override_sphere = pxr::UsdGeomSphere(another->OverridePrim(pxr::SdfPath{"/Some/Prim"}));
    override_sphere.GetRadiusAttr().Set(20.0);

    return stage;
}


pxr::UsdStageRefPtr _create_basic_scene_with_more_values() {
    auto stage = _create_basic_scene();
    auto override_sphere = pxr::UsdGeomSphere(stage->OverridePrim(pxr::SdfPath{"/Some/Prim"}));

    for (int sample = 0; sample < 10000; ++sample) {
        override_sphere.GetRadiusAttr().Set(sample + 30.0, sample);
    }

    return stage;
}


void _get_time_samples(std::vector<pxr::UsdAttribute> const &attributes) {
    for (auto const &attribute : attributes) {
        std::vector<double> times;
        attribute.GetTimeSamples(&times);
    }
}


void timeit(std::function<void ()> function, unsigned int repeats) {
    using namespace std::chrono;

    auto start = high_resolution_clock::now();

    for (unsigned int index = 0; index < repeats; ++index) {
        function();
    }

    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stop - start);
    std::cout
        << "Function was called \"" << repeats
        << "\" times and took " << duration.count() << " "
        << "microseconds \n";
}


int main() {
    std::cout << "Simple Stage:\n";
    auto stage = _create_basic_scene();
    auto sphere = pxr::UsdGeomSphere(stage->GetPrimAtPath(pxr::SdfPath{"/Some/Prim"}));

    auto radius = sphere.GetRadiusAttr();
    std::cout << "Testing Get(), normally\n";
    timeit(std::bind(forwarder::forward, radius), REPEATS);

    auto query = pxr::UsdAttributeQuery(radius);
    std::cout << "Testing Get(), using UsdAttributeQuery\n";
    timeit(std::bind(forwarder::forward_query, query), REPEATS);
    std::cout << '\n';

    std::cout << "Testing GetTimeSamples(), normally\n";
    timeit(std::bind(forwarder::forward_time_samples, radius), REPEATS);

    std::vector<pxr::UsdAttributeQuery> queries {query};
    std::cout << "Testing GetTimeSamples(), using a union\n";
    timeit(std::bind(forwarder::forward_unioned_time_samples, queries), REPEATS);
    std::cout << '\n';

    auto visibility = sphere.GetVisibilityAttr();

    std::vector<pxr::UsdAttribute> attributes = {radius, visibility};
    std::cout << "Testing GetTimeSamples(), for multiple attributes, normally\n";
    timeit(std::bind(_get_time_samples, attributes), REPEATS);

    queries = {query, pxr::UsdAttributeQuery(visibility)};
    std::cout << "Testing GetTimeSamples() for multiple attributes, using a union\n";
    timeit(std::bind(forwarder::forward_unioned_time_samples, queries), REPEATS);
    std::cout << '\n';

    std::cout << "Heavy Stage:\n";
    auto heavier_stage = _create_basic_scene_with_more_values();
    sphere = pxr::UsdGeomSphere(heavier_stage->GetPrimAtPath(pxr::SdfPath{"/Some/Prim"}));
    radius = sphere.GetRadiusAttr();
    visibility = sphere.GetVisibilityAttr();
    query = pxr::UsdAttributeQuery(radius);
    attributes = {radius, visibility};

    std::cout << "Testing GetTimeSamples(), normally\n";
    timeit(std::bind(_get_time_samples, attributes), REPEATS);

    std::cout << "Testing GetTimeSamples(), using a union\n";
    queries = {query, pxr::UsdAttributeQuery(visibility)};
    timeit(std::bind(forwarder::forward_unioned_time_samples, queries), REPEATS);

    return 0;
}
