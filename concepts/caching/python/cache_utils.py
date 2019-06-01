#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT THIRD-PARTY LIBRARIES
from pxr import UsdUtils
from pxr import Usd


def add_to_cache_from_external_function():
    stage = Usd.Stage.CreateInMemory()
    cache = UsdUtils.StageCache.Get()
    cache.Insert(stage)


def get_stage_from_id(stage_id):
    cache = UsdUtils.StageCache.Get()
    print('Found stage', cache.Find(stage_id))


def main():
    """Run the main execution of the current script."""
    stage = Usd.Stage.CreateInMemory()
    cache = UsdUtils.StageCache.Get()

    with Usd.StageCacheContext(cache):
        print('This should be False', cache.Contains(stage))
        auto_added_stage = Usd.Stage.CreateInMemory()
        print('This should be True', cache.Contains(auto_added_stage))
        get_stage_from_id(cache.GetId(auto_added_stage))

    print('We will add a stage to the cache in a separate function (1)', len(cache.GetAllStages()))
    add_to_cache_from_external_function()
    print('Cache was added (now it should be (2))', len(cache.GetAllStages()))


if __name__ == "__main__":
    main()
