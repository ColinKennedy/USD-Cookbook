#pragma once

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/usd/ar/defaultResolver.h>

PXR_NAMESPACE_OPEN_SCOPE

class URIResolver : public ArDefaultResolver {
public:
    URIResolver();
    ~URIResolver();

    bool IsRelativePath(const std::string& path) override;

    std::string Resolve(const std::string& path) override;

    // std::string ResolveWithAssetInfo(
    //     const std::string& path, ArAssetInfo* assetInfo) override;
    //
    // void UpdateAssetInfo(
    //     const std::string& identifier, const std::string& filePath,
    //     const std::string& fileVersion, ArAssetInfo* assetInfo) override;
    //
    // // Quick workaround for a bug in USD 0.8.4.
    // std::string AnchorRelativePath(
    //     const std::string& anchorPath, const std::string& path) override;
    //
    // VtValue GetModificationTimestamp(
    //     const std::string& path, const std::string& resolvedPath) override;
    //
    // bool FetchToLocalResolvedPath(
    //     const std::string& path, const std::string& resolvedPath) override;
};

PXR_NAMESPACE_CLOSE_SCOPE
