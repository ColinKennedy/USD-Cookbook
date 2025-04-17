// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/usd/ar/defaultResolver.h>
#include <pxr/usd/ar/defineResolver.h>

// IMPORT LOCAL LIBRARIES
#include "resolver.h"

PXR_NAMESPACE_OPEN_SCOPE

AR_DEFINE_RESOLVER(URIResolver, ArResolver)


URIResolver::URIResolver() : ArDefaultResolver() {}

URIResolver::~URIResolver() = default;


ArResolvedPath URIResolver::_Resolve(const std::string& path) {
    if (path == "/foo") {
        return ArResolvedPath("/bar");
    }

    return {};
}

PXR_NAMESPACE_CLOSE_SCOPE
