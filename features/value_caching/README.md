# Quick Summary

When you query a value in USD, that value's the correct opinion that
will lead to the composed value has to be calculated each time over and
over again, each time. (Usually, it's strongest-opinion-wins, for value
resolution).

But if your situation is simple and you know that the stage isn't
changing, which is frequently the case for non-interactive scripts, then
this process is overkill.

A much faster way to query attributes is to use
[UsdAttributeQuery](https://graphics.pixar.com/usd/docs/api/class_usd_attribute_query.html)

UsdAttributeQuery is simple. It re-uses composition-related calculations
so that you can repeatedly request the value of an attribute,
repeatedly.

UsdAttributeQuery works differently from a regular memoized cache
though. You can even set an attribute's value pre & post creating a
UsdAttributeQuery and the value that UsdAttributeQuery creates will be
updated, correctly.

There are limits though to what you can do. So consult USD's documentation.

## C++

```cpp
auto query = pxr::UsdAttributeQuery(radius);
query.Get();

std::vector<pxr::UsdAttributeQuery> queries {query1, query2, ...};
std::vector<double> times;
pxr::UsdAttributeQuery::GetUnionedTimeSamples(queries, &times);
```


## Python

```python
query = Usd.AttributeQuery(radius)
query.Get()

Usd.AttributeQuery.GetUnionedTimeSamples([query1, query2, ...])
```


## How Much Faster Is It?
There are the results from 2 basic stages, from the C++ project.

```
Simple Stage:
Testing Get(), normally
Function was called "1000" times and took 772 microseconds
Testing Get(), using UsdAttributeQuery
Function was called "1000" times and took 613 microseconds

Testing GetTimeSamples(), normally
Function was called "1000" times and took 1016 microseconds
Testing GetTimeSamples(), using a union
Function was called "1000" times and took 895 microseconds

Testing GetTimeSamples(), for multiple attributes, normally
Function was called "1000" times and took 1907 microseconds
Testing GetTimeSamples() for multiple attributes, using a union
Function was called "1000" times and took 1264 microseconds

Heavy Stage:
Testing GetTimeSamples(), normally
Function was called "1000" times and took 1875546 microseconds
Testing GetTimeSamples(), using a union
Function was called "1000" times and took 1452561 microseconds
```

For both stages, it's about a 20% savings. That's pretty high,
considering it took almost no effort to add in.

From personal tests, the savings get close to 50% when a scene of
reasonable complexity (with many layers) is loaded, as well!


## References

[UsdAttributeQuery](https://graphics.pixar.com/usd/docs/api/class_usd_attribute_query.html)
