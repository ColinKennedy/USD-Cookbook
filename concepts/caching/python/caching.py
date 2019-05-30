#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT FUTURE LIBRARIES
from __future__ import print_function

# IMPORT STANDARD LIBRARIES
import functools
import threading
import time

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Usd


class StageTraversalWatcher(threading.Thread):
    def __init__(self, event, cache, stage_ids):
        super(StageTraversalWatcher, self).__init__()
        self.stop_event = event
        self.cache = cache
        self.stage_ids = stage_ids

    def run(self):
        stages = [self.cache.Find(stage_id) for stage_id in self.stage_ids]
        while not self.stop_event.wait(0.1):
            for stage in stages:
                for prim in stage.TraverseAll():
                    print('Found prim:', prim.GetPath(), stage)


def using_contexts():
    stage = Usd.Stage.CreateInMemory()
    cache = Usd.StageCache()
    print('Should be False (the cache was just created)', cache.Contains(stage))

    with Usd.StageCacheContext(cache):
        innerStage = Usd.Stage.CreateInMemory()
        print('Has stage?', cache.Contains(innerStage))

        with Usd.StageCacheContext(Usd.BlockStageCachePopulation):
            newStage = Usd.Stage.CreateInMemory()
            print('Has stage?', cache.Contains(innerStage))
            print('Has new stage?', cache.Contains(newStage))

        print('Still has stage?', cache.Contains(innerStage))
        stage_id = cache.GetId(innerStage)
        print('The key that refers to the cached, opened USD stage', stage_id.ToString())
        print('Found stage in cache', cache.Find(stage_id) == innerStage)

    print("Still has it??", cache.Contains(innerStage))
    cache.Clear()
    print("This value should be False now", cache.Contains(innerStage))


def using_explicit_inserts():
    stage = Usd.Stage.CreateInMemory()
    cache = Usd.StageCache()
    cache.Insert(stage)

    print('Should be True (the stage was added to the cache)', cache.Contains(stage))
    print('Still has stage?', cache.Contains(stage))
    stage_id = cache.GetId(stage)
    print('The key that refers to the cached, opened USD stage', stage_id.ToString())
    print('Found stage in cache', cache.Find(stage_id) == stage)

    print("Still has it??", cache.Contains(stage))
    cache.Clear()
    print("This value should be False now", cache.Contains(stage))


def threading_example():
    # """ Strongly typed? Lets test that.
    #
    # Reference:
    #     https://graphics.pixar.com/usd/docs/api/class_usd_stage_cache.html#af6d4a9d580fe05510b1a35087332166c
    #
    # """
    def create_prims(cache, stage_ids, index):
        for stage_id in stage_ids:
            stage = cache.Find(stage_id)
            stage.DefinePrim('/SomeSphere{index}'.format(index=index), 'Sphere')
            time.sleep(0.003)

    stage1 = Usd.Stage.CreateInMemory()
    stage2 = Usd.Stage.CreateInMemory()
    cache = Usd.StageCache()
    cache.Insert(stage1)
    cache.Insert(stage2)

    # Create a watcher that will repeatedly read Stage objects from the StageCache
    stop = threading.Event()
    stage_ids = [cache.GetId(stage1), cache.GetId(stage2)]
    watcher = StageTraversalWatcher(stop, cache, stage_ids)
    watcher.start()

    # XXX : The watcher is checking `stage1` as we continually write to
    #       it on the main thread
    #
    for index in range(1000):
        stage1.DefinePrim('/SomeCube{index}'.format(index=index), 'Cube')
        time.sleep(0.002)

    # XXX : Now we're writing to two USD stages on 2 threads at once.
    #       While this is happening, the `watcher` is still reading and
    #       printing from both stages
    #
    for index in range(1000):
        creator = threading.Thread(target=functools.partial(
            create_prims, cache, stage_ids, index))
        creator.start()
        creator.join()

    stop.set()  # Stop watching for changes

    print('Done')


def main():
    """Run the main execution of the current script."""
    using_contexts()
    using_explicit_inserts()
    threading_example()


if __name__ == "__main__":
    main()
