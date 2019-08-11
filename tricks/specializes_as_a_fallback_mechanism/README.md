## Quick Explanation

The USD Schema registry has fallback values assigned for USD Prim
types. Those values are used when no opinion is authored when a Prim is
created.

```usda
def Sphere "MySphere" (
    "This Prim will have a radius of 1, even though we don't write that down, here."
)
{
}
```

But what if you basically need a `Sphere` but with a fallback radius of
4? The proper answer is to "define a new type, add it to USD's Schema
Registry, and then use that type to define a default radius value of 4."
And 99% of the time, this is the best way to work. It's the best way for
several reasons:

- Using USD's Schema Registry means that, if one day you want to change
  the default value of a type across all definitions everywhere, you only
  have to change it in the Registry and every USD file will immediately
  get the change.
- It keeps USD files lightweight and reduces the amount of Composition
  Arcs that you need to write.
- It's the simplest way to do it, once you know how.

There's a couple problems with using the Schema Registry though.

- It's a pretty heavy-handed to create a new Type for a single fallback value.
- In complex pipelines, not everyone that would need to make their own
default values will also be able to make a new Type and add it to the
pipeline's environment variables.

Luckily, there's still a way to do it. It's admittedly hacky but it does work.
The answer: Use the `specializes` Composition Arc.


### Why it works
The `specializes` Composition Arc is the weakest Composition Arc.
This makes it the best Arc to use as a fallback mechanism. If another
Composition Arc like `references` or `payload` are added to the same
Prim, their values will always be preferred over any values that are
written in `specializes`.

This solution requires no Types to be authored/registered and works for
temporary or "one-off" scenarios where you just need something for a
simple use-case.


#### Disadvantages to using specializes as a fallback mechanism
I won't lie, the disadvantages are many. Like mentioned earlier, 
it's almost always better to define your own type and use that. 
Otherwise if you use `specializes`, you'll run into these issues:

- You'll need to have the `specializes` Composition Arc anywhere in
your code where you need a fallback value. And since `specializes` has
unlimited levels of referencing, that will have more memory overhead
than a regular Prim type.
- In general, the `specializes` Composition Arc complicates pipelines
because it means stronger Layers cannot override values of the
base-class of specialized Prims. If that kind of editting restriction
is desired though, this may actually be seen as an advantage. But in my
opinion, it's an anti-pattern to prevent users from changing settings
from Prims defined in weaker Layers.
    - If you're reading this item and don't know what it's talking about, check out
	[specializes_a_practical_example](../specializes_a_practical_example).


## See Also
https://graphics.pixar.com/usd/docs/USD-Glossary.html#USDGlossary-LIVRPSStrengthOrdering
