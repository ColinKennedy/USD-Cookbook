// IMPORT STANDARD LIBRARIES
#include <chrono>
#include <cstdio>
#include <future>
#include <iostream>
#include <thread>
#include <vector>

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/base/tf/stringUtils.h>
#include <pxr/base/tf/token.h>
#include <pxr/usd/usd/primRange.h>
#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usd/stageCache.h>
#include <pxr/usd/usd/stageCacheContext.h>


using StageIds = std::vector<pxr::UsdStageCache::Id>;


void watch_for_changes(
    std::future<void> future_object,
    pxr::UsdStageCache const &cache,
    StageIds const &stage_ids
)
{
    std::vector<pxr::UsdStageRefPtr > stages;
    stages.reserve(stage_ids.size());

    for (auto const &stage_id : stage_ids) {
        stages.push_back(cache.Find(stage_id));
    }

    std::cout << "Thread Start" << std::endl;
    while (future_object.wait_for(std::chrono::milliseconds(1)) == std::future_status::timeout)
    {
        for (auto const &stage : stages) {
            for (auto const &prim : stage->TraverseAll()) {
                std::cout
                    << "Found prim: "
                    << prim.GetPath()
                    << '\n'
                ;
            }
        }

        std::this_thread::sleep_for(std::chrono::milliseconds {100});
    }

    std::cout << "Thread End" << std::endl;
}

void create_prims(pxr::UsdStageCache const &cache, StageIds const &stage_ids, int index) {
    for (auto const &stage_id : stage_ids) {
        auto stage = cache.Find(stage_id);
        std::ostringstream stream;
        stream << "/SomeSphere" << index;
        stage->DefinePrim(pxr::SdfPath {stream.str()}, pxr::TfToken{"Sphere"});
        std::this_thread::sleep_for(std::chrono::milliseconds {3});
    }
}


void using_contexts() {
    auto stage = pxr::UsdStage::CreateInMemory();
    auto cache = pxr::UsdStageCache {};
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


void using_explicit_inserts() {
    auto stage = pxr::UsdStage::CreateInMemory();
    auto cache = pxr::UsdStageCache {};
    cache.Insert(stage);

    std::cout << std::boolalpha;
    std::cout << "Should be true (the stage was added to the cache) " << cache.Contains(stage) << '\n';
    auto stage_id = cache.GetId(stage);
    std::cout << "The key that refers to the cached, opened USD stage " << stage_id.ToString() << '\n';
    std::cout << "Found stage in cache " << (cache.Find(stage_id) == stage) << '\n';

    std::cout << "Still has it?? " << cache.Contains(stage) << '\n';
    cache.Clear();
    std::cout << "This value should be false now " << cache.Contains(stage) << '\n';
}


void threading_example() {
    auto stage1 = pxr::UsdStage::CreateInMemory();
    auto stage2 = pxr::UsdStage::CreateInMemory();
    auto cache = pxr::UsdStageCache {};
    cache.Insert(stage1);
    cache.Insert(stage2);

    StageIds stage_ids = {
        cache.GetId(stage1),
        cache.GetId(stage2),
    };

    // Reference: https://thispointer.com/c11-how-to-stop-or-terminate-a-thread/
    std::promise<void> stop;
    std::future<void> future_object = stop.get_future();
    std::thread thread {&watch_for_changes, std::move(future_object), cache, stage_ids};

    // XXX : The watcher is checking `stage1` as we continually write to
    // it on the main thread
    //
    for (int index = 0; index < 1000; ++index) {
        std::ostringstream stream;
        stream << "/SomeCube" << index;
        stage1->DefinePrim(pxr::SdfPath {stream.str()}, pxr::TfToken{"Cube"});
        std::this_thread::sleep_for(std::chrono::milliseconds {2});
    }

    // XXX : Now we're writing to two USD stages on 2 threads at once.
    // While this is happening, the `watcher` is still reading and
    // printing from both stages
    //
    for (int index = 0; index < 1000; ++index) {
        auto creator = std::thread([&](){ create_prims(cache, stage_ids, index); });
        // XXX : We can't have multiple threads writing at the same time
        // so we need to wait for the thread to finish before starting
        // another one.
        //
        creator.join();
    }

    stop.set_value();
    thread.join();

    std::cout << "Done\n";
};


int main() {
    using_contexts();
    using_explicit_inserts();
    threading_example();

    return 0;
}
