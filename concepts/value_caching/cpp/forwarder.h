#pragma once

// IMPORT STANDARD LIBRARIES
#include <vector>

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/usd/usd/attribute.h>
#include <pxr/usd/usd/attributeQuery.h>


namespace forwarder {
    void forward(pxr::UsdAttribute const &attribute) {
        double value;
        attribute.Get(&value);
    }

    void forward_time_samples(pxr::UsdAttribute const &attribute) {
        std::vector<double> times;
        attribute.GetTimeSamples(&times);
    }

    void forward_query(pxr::UsdAttributeQuery const &attribute) {
        double value;
        attribute.Get(&value);
    }

    void forward_unioned_time_samples(std::vector<pxr::UsdAttributeQuery> queries) {
        std::vector<double> times;
        pxr::UsdAttributeQuery::GetUnionedTimeSamples(queries, &times);
    }
}
