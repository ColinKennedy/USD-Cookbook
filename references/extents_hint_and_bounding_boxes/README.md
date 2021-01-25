extentsHint and how they relate to bounding boxes in USD is a somewhat
misunderstood concept. As always, we'll start with the conclusion and
explain, in detail, how each part works if you want a more thorough
explanation.


## Writing extentsHint Values
### Writing extentsHint Values For Bounding Boxes

A big reason why people like extentsHint is so that they can be used to
display pre-computed bounding boxes.

Technically, you can author an extentsHint on any [UsdGeomBoundable](https://graphics.pixar.com/usd/docs/api/class_usd_geom_boundable.html) Prim.
But if you want extentsHint specifically for bounding boxes, you must follow these rules:

all_in_one.usda
```usda
#usda 1.0

def Cube "bounding_box_here" (
    kind = "component"
    payload = @something.usda@
)
{
    float3[] extentsHint = [(-1, -1, -1), (1, 2.5, 1)]
}
```

These are the rules - On a single Prim:

1. You need a valid model kind hierarchy
    - To learn more about that, [read this page](../model_hierarchy_validity)
2. You need a composition arc
3. You need an extentsHint authored on the Prim

All 3 points must be authored on the **same** Prim. In other words, you
can't split it up across Prims, like this

does_not_work.usda
```usda
#usda 1.0

def Cube "bounding_box_here" (
    kind = "group"
    payload = @something.usda@
)
{
    def Scope "inner" (
		doc = "The extentsHint is authored on a child, but that's not good!"
        kind = "component"
    )
    {
        float3[] extentsHint = [(-1, -1, -1), (1, 2.5, 1)]
    }
}
```

Also this doesn't work


all_in_one_broken.usda
```usda
#usda 1.0

def Scope "root"
{
	def Cube "bounding_box_here" (
		kind = "component"
		payload = @something.usda@
	)
	{
		float3[] extentsHint = [(-1, -1, -1), (1, 2.5, 1)]
	}
}
```

The reason: All of the values are on one Prim, which is great, but
</root/bounding_box_here> isn't a valid "component" kind because </root>
needs to define a "group" or "assembly" kind.

One last note about rule #2 (composition arcs)
Sublayers won't work since they are authored on a Layer, not a Prim. But
any other L**IVRPS** arcs are okay. 99.99%, you'll want to use **payload**.


### How Do I Know extentsHint Is Properly Authored?

**Important** - If you don't see bounding boxes in your usdview, make sure you
have the bounding box setting enabled.

TODO image here

The easiest way to know if you wrote extentsHint properly is to open your stage in `usdview`.

```sh
usdview simple.usda
```

TODO image here

The effect is even more obvious when you load without payloads

```sh
usdview simple.usda --unloaded
```

TODO image here


### Concluding This Summary

If all you want is to know how to write extentsHint, no need to read further. The rest of this page is for people who want to know extentsHint as **extents**-ively as possible.
