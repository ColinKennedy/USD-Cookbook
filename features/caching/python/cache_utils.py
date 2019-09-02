#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module is a variant of `caching.py` that explores uses of `pxr.UsdUtils.StageCache`.

Unlike `pxr.Usd.StageCache` which is not a singleton,
`pxr.UsdUtils.StageCache` is. This lets us use USD's stage cache without
passing a cache object around to every function. It's very useful for
applications.

"""

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Usd, UsdUtils


def add_to_cache_from_external_function():
    """Refer to the singleton UsdUtils cache to insert a stage."""
    stage = Usd.Stage.CreateInMemory()
    cache = UsdUtils.StageCache.Get()
    cache.Insert(stage)


def get_stage_from_id(stage_id):
    """Refer to the singleton UsdUtils cache to find a stage by-ID."""
    cache = UsdUtils.StageCache.Get()
    print("Found stage", cache.Find(stage_id))


def main():
    """Run the main execution of the current script."""
    stage = Usd.Stage.CreateInMemory()
    cache = UsdUtils.StageCache.Get()

    with Usd.StageCacheContext(cache):
        print("This should be False", cache.Contains(stage))
        auto_added_stage = Usd.Stage.CreateInMemory()
        print("This should be True", cache.Contains(auto_added_stage))
        get_stage_from_id(cache.GetId(auto_added_stage))

    print(
        "We will add a stage to the cache in a separate function (1)",
        len(cache.GetAllStages()),
    )
    add_to_cache_from_external_function()
    print("Cache was added (now it should be (2))", len(cache.GetAllStages()))


if __name__ == "__main__":
    main()
