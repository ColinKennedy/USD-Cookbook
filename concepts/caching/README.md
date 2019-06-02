# Quick Reference
## Auto-Add Stages To Cache

```cpp
auto cache = pxr::UsdStageCache {};

{
    pxr::UsdStageCacheContext context(cache);
    auto stage = pxr::UsdStage::CreateInMemory();
}
```

```python
cache = Usd.StageCache()

with Usd.StageCacheContext(cache):
    stage = Usd.Stage.CreateInMemory()
```

## Explicitly-Add Stages To Cache

```cpp
auto stage = pxr::UsdStage::CreateInMemory();
auto cache = pxr::UsdStageCache {};
cache.Insert(stage);
```

```python
stage = Usd.Stage.CreateInMemory()
cache = Usd.StageCache()
cache.Insert(stage)
```

## Get Stage From Singleton Cache

```python
def get_stage_from_id(stage_id):
    """Refer to the singleton UsdUtils cache to find a stage by-ID."""
    cache = UsdUtils.StageCache.Get()
    print('Found stage', cache.Find(stage_id))
```
