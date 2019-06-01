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

    pxr::UsdStageCache::Id saved_id;
    {
        pxr::UsdStageCacheContext context(cache);
        auto inner_stage = pxr::UsdStage::CreateInMemory();
        std::cout << "Has stage? " << cache.Contains(inner_stage) << '\n';

        {
            pxr::UsdStageCacheContext blocked_context(pxr::UsdBlockStageCachePopulation);
            auto new_stage = pxr::UsdStage::CreateInMemory();
            std::cout << "Has stage? (true) " << cache.Contains(inner_stage) << '\n';
            std::cout << "Has new stage? (false) " << cache.Contains(new_stage) << '\n';
        }

        std::cout << "Still has stage? (true) " << cache.Contains(inner_stage) << '\n';
        auto stage_id = cache.GetId(inner_stage);
        std::cout << "The key that refers to the cached, opened USD stage " << stage_id.ToString() << '\n';
        std::cout << "Found stage in cache " << (cache.Find(stage_id) == inner_stage) << '\n';

        saved_id = cache.GetId(inner_stage);
    }

    // XXX : A difference between C++ and Python, you cannot create a
    // stage within a StageCacheContext automatically and then still
    // retrieve it after the context exits because the scoping rules for
    // C++ and Python are different
    //
    // To reflect this, I commented out the lines that work in Python
    // but don't work here.
    //
    // std::cout << "Still has it?? " << cache.Contains(inner_stage) << '\n';
    // cache.Clear();
    // std::cout << "This value should be false now " << cache.Contains(inner_stage) << '\n';

    // XXX : You can still refer to the stage from the cache. Just not
    // with the `inner_stage` object
    //
    auto inner_stage = cache.Find(saved_id);
    std::cout << "Still has it?? " << cache.Contains(inner_stage) << '\n';
    cache.Clear();
    std::cout << "This value should be false now " << cache.Contains(inner_stage) << '\n';
}


int main() {
    using_contexts();
    return 0;
}
