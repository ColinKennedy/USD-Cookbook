The USD extentsHint attribute is a bit special compared to others. You
can author them easily and on most Prims but, to author it well, there
are certain rules which USD expects you to follow.

As always, we'll start with the conclusion first if you're just looking
for the key take-aways. Read the full page if you want the nitty-gritty
details.


## Writing extentsHint Values
### Writing extentsHint Values For Bounding Boxes

A big reason why people like extentsHint is so that they can be used to
display pre-computed bounding boxes.

Technically, you can author an extentsHint on any
[UsdGeomBoundable](https://graphics.pixar.com/usd/docs/api/class_usd_geom_boundable.html)
Prim. But if you want extentsHint specifically for bounding boxes, you
must follow these rules:

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
    - To learn more about that, [Valid Model Hierarchies](../../concepts/valid_model_hierarchies)
2. You need an extentsHint authored on the Prim

These 2 points must be authored on the **same** Prim.

More or less, that's what you'd want to do when authoring extentsHint data.


### Other Key Things To Mention

The USD documentation recommends to author extentsHint **above**
payloads and only directly on the Prim of payloaded data. It recommends
this because extentsHint expects all Prims and child Prims to be fully
encapsulated. If a Prim in a Layer changes, extentsHint values in
stronger Layers will need to be recalculated or they become out of date.

In practice though, if your pipeline has locks in place to prevent that
from happening, it's fine (in my experience).

Also, use timeSamples on extentsHint for animated geometry / animated
rigged assets. That way, when a character's extentsHint is not in
view of the camera, hydra can cull the character without calculating
skinning.


## extentsHint Definition Details

To expand a bit on the previous section, specifically, you can't split
it up the information across Prims, like this:

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

For more information on how to set up good Model kinds, see:
[Valid Model Hierarchies](../../concepts/valid_model_hierarchies)


## How Do I Know extentsHint Is Properly Authored?

**Important** - If you don't see bounding boxes in your usdview, make sure you
have the bounding box setting enabled.

![usdview_bounding_box_settings](https://user-images.githubusercontent.com/10103049/105656137-6a72ea80-5e76-11eb-8d6c-b22f9da85f43.png)

The easiest way to know if you wrote extentsHint properly is to open
your stage in `usdview`.

```sh
usdview simple.usda
```

![usdview_extexts_hint_loaded](https://user-images.githubusercontent.com/10103049/105655989-1962f680-5e76-11eb-91c9-2358be730bb2.png)

The effect is even more obvious when you load without payloads

```sh
usdview simple.usda --unloaded
```

![usdview_extexts_hint_unloaded](https://user-images.githubusercontent.com/10103049/105655966-0d773480-5e76-11eb-8abd-ab15fc691e69.png)

Note: The extentsHint in this file is intentionally too large for the
sake of demonstration. Normally, you'd want it to hug the geometry as
tightly as possible.


## extents, extentsHint, and USD Purposes

extentsHint is an array attribute. Many people assume it defines 2
points of a bounding box. That explanation is half right. It actually
defines 2 local positions per-purpose!

This extentsHint will define bounds for the default purpose (and all
other purposes) of a Prim.

```usda
float3[] extentsHint = [(-1, -1, -1), (1, 2.5, 1)]
```

This extentsHint defines separate values for each USD purpose
guide purposes.

```usda
float3[] extentsHint = [
    (3.4028235e38, 3.4028235e38, 3.4028235e38), (-3.4028235e38, -3.4028235e38, -3.4028235e38),  # default
    (-2.5, -3, -2.5), (-1.5, -1, -1.5),  # render
    (-5.5, -5.5, -5.5), (-4.5, -4.5, -4.5),  # proxy
    (4, 5.5, 4), (8, 6.5, 8)  # guide
]
```

You can see the results of this in usdview

```sh
usdview multiple_purposes.usda --unloaded
```

When you switch between each purpose, you'll see each authored box. When
you have multiple purposes on at once, an aggregate extentsHint is drawn
on-screen.

See the GIF below for a demonstration

![extents_hint_demonstration](https://user-images.githubusercontent.com/10103049/105666062-45d63d00-5e8d-11eb-8fd1-05d7f846ea56.gif)


## See Also

[Valid Model Hierarchies](../../concepts/valid_model_hierarchies)
