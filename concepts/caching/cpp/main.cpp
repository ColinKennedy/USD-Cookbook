// IMPORT STANDARD LIBRARIES
#include <iostream>

// IMPORT THIRD-PARTY LIBRARIES
#include "pxr/usd/usd/stage.h"
#include "pxr/usd/usd/stageCache.h"
#include "pxr/usd/usd/stageCacheContext.h"


void using_contexts() {
    auto stage = pxr::UsdStage::CreateInMemory();
    pxr::UsdStageCache cache;
    std::cout << "Should be False (the cache was just created) " << cache.Contains(stage) << '\n';

    {
        pxr::UsdStageCacheContext context(cache);
        auto inner_stage = pxr::UsdStage::CreateInMemory();
        std::cout << "Has stage? " << cache.Contains(inner_stage) << '\n';

        // {
        //     auto blocked_context = pxr::UsdStageCacheContext();
        // }
    }
}


int main() {
    using_contexts();
    return 0;
}
