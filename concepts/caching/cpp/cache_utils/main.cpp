/* This module is a variant of `caching.py` that explores uses of `pxr.UsdUtils.StageCache`.

Unlike `pxr.Usd.StageCache` which is not a singleton,
`pxr.UsdUtils.StageCache` is. This lets us use USD's stage cache without
passing a cache object around to every function. It's very useful for
applications.

*/

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usd/stageCacheContext.h>
#include <pxr/usd/usdUtils/stageCache.h>


int main() {
    auto stage = pxr::UsdStage::CreateInMemory();
    auto cache = pxr::UsdUtilsStageCache::Get();

    {
        pxr::UsdStageCacheContext context(cache);
        std::cout << std::boolalpha;
        std::cout << "This should be false: " << cache.Contains(stage) << '\n';
    }

    return 0;
}
