## Quick Explanation

USD Relationships can point to any valid path in a USD stage's
namespace. But can a Relationship point to another Relationship? Well,
a Relationship is just a Property on a Prim. So the answer is: yes, of
course!

In the USD documentation, the process of having one Relationship point
to another Relationship which points to another is called "Relationship
Forwarding". If you combine Relationships with VariantSets, you can create
more complicated forwarding schemes, like a multiplexer or a a de-multiplexer.

In this folder,
[destination_forwarding](usda/destination_forwarding.usda) is
an example of a multiplexer because it shows how to make a
single Relationship input point to one of multiple targets. And
[source_forwarding](usda/source_forwarding.usda) is an example of a
de-multiplexer because it shows how the user can narrow multiple target
inputs into a single output target.

### C++

```cpp
pxr::SdfPathVector targets;
stage.GetPrimAtPath("/SomePrim").GetRelationship("some_relationship").GetForwardedTargets(&targets);
```


### Python
```python
stage.GetPrimAtPath("/SomePrim").GetRelationship("some_relationship").GetForwardedTargets()
```


## Motivation
While reading through the USD documentation, it makes several mentions
of a "Composition Compendium" and even says "We will work through this
example in the USD reference manual."

To my knowledge, neither references exist. So for now, I figured I'd
make my own reference.


### See Also
https://graphics.pixar.com/usd/docs/api/class_usd_relationship.html
https://graphics.pixar.com/usd/docs/api/class_usd_relationship.html#aebfc7f75593e419ff680ca3ed3d7c433
