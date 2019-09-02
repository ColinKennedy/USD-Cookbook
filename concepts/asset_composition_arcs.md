# Asset Composition Arcs - The `</root>` of all evil

USD has 3 composition arcs that read files from disk: SubLayers,
References, and Payloads. Between the 3, SubLayers is the simplest and
readest for USD to read.

SubLayers is great but strict about what you can and can't do with it.
- you can't sublayer 50% of another layer.
- you can't rename any Prim that the layer includes. 
- you can't list-edit sublayers. Which means if you have a 3-chain list
  of sublayers, you cannot remove and replace a nested sublayer.

The good news though is that references can fix all 3 issues, with a
little bit of engineering.

The solution is to take every root Prim that would be in a layer and put
them in a single root Prim (for the sake of this article, we'll
call it `</root>`).


## Why `</root>` works
USD doesn't allow you to reference the root (pseudo-root) of another
layer. But if your target layer has a Prim in it called `</root>` and
that `</root>` Prim contains every other Prim in it, you __can__ target
`</root>` and make that a reference. And that'd effectively be the same
as if you __could__ target the pseudoRoot as a sublayer!

For example, say you have 3 layers, like this:


`model_v1.usda`
```usda
#usda 1.0

def Sphere "SomePrim"
{
}

```

`surfacing.usda`
```usda
#usda 1.0
(
    subLayers = [
        @./model_v1.usda@
    ]
)
```

`rigging.usda`
```usda
#usda 1.0
(
    subLayers = [
        @./surfacing.usda@
    ]
)
```

If you're a rigger, you may want to update `model_v1.usda` to
`model_v2.usda` to do your work. But you can't, because you'd have to
reach through `surfacing.usda` to do it. And, as mentioned before,
sublayers will not let you do that.

Now consider the same layers, but with `</root>`

`model_v1.usda`
```usda
#usda 1.0
(
    defaultPrim = "root"
)

def Scope "root"
{
    def Sphere "SomePrim"
    {
    }
}
```

`model_v2.usda`
```usda
#usda 1.0
(
    defaultPrim = "root"
)

def Scope "root"
{
    def Sphere "SomePrim"
    {
        double radius = 3.0
    }
}
```

`surfacing.usda`
```usda
#usda 1.0
(
    defaultPrim = "root"
)

def Scope "root" (
    add references = @./model_v1.usda@
)
{
}
```

```usda
#usda 1.0

def Scope "root" (
    delete references = @model_v1.usda@
    add references = @./surfacing.usda@
    prepend references = @/tmp/model_v2.usda@
)
{
}
```

The value of `</root/SomePrim.radius>`, in this case, is 3. Because we removed
`model_v1.usda` and replaced it with `model_v2.usda`!

This works because USD's reference composition arc has unlimited
referencing. That said, avoid using references as a replacement for
sublayers if you can help it. Keeping track of nested layers makes
references much slower than sublayers. But if you can't avoid needing
this feature then the `</root>` technique will no doubt be helpful.

There's one more use-case for `</root>` which will be explained, below.


## `</root>` As A Composition Arc Manager
Pretend you have a layer that looks like this:


```usda
#usda 1.0
(
    subLayers = [
        @./sublayer.usda@
    ]
)

over "Prim" (
    add references = @./final_reference.usda@</Another>
)
{
}
```

</Prim> in this case is a Sphere. "sublayer.usda" contains a defintion
of sphere and "final_refererence.usda" also has a Sphere, which we
reference.

If both layers author an opinion for the `radius` Attribute, which
opinion in which layer will be used?

The answer is "it depends on the contents of sublayer.usda". If
"sublayer.usda" and "final_refererence.usda" both offer direct
opinions on a `radius`, the reference's `radius` is ignored. Because
a local opinion in a sublayer is stronger than a reference. (See
[LIVRPS](https://graphics.pixar.com/usd/docs/USD-Glossary.html#USDGlossary-LIVRPSStrengthOrdering) if you're confused).

You can try this yourself using this code:

`main.usda`
```usda
#usda 1.0
(
    subLayers = [
        @./sublayer.usda@
    ]
)

over "Prim" (
    add references = @./reference.usda@</Another>
)
{
}
```

`sublayer.usda`
```usda
#usda 1.0

def Sphere "Prim"
{
    double radius = 2
}
```

`reference.usda`
```usda
#usda 1.0

def Sphere "Another"
{
    double radius = 3
}
```

You might think that `radius` would be `3` because the "reference.usda"
is authored directly on "/Prim" but the reference composition arc is
still weaker than "sublayer.usda". Instead, `sublayer.usda` adds `2` to
the stage.

Now that the problem is well defined, what can we do about it? There's
multiple ways of dealing this problem. Again, `</root>` can be used to
address the issue.


## `</root>` Makes Layer Opinions Weaker
When you choose to reference a stage using `</root>`,

the referenced layer's local opinions are not stronger than any other
reference in `main.usda`.

Old `main.usda`
```usda
#usda 1.0
(
    subLayers = [
        @./sublayer.usda@
    ]
)

def Scope "root"
{
    over "Prim" (
        add references = @./reference.usda@</Another>
    )
    {
    }
}
```

In this example, if `reference.usda` and `sublayer.usda` both had a
local opinion for the property `</root.Prim.radius>`, `sublayer.usda`'s
opinion would win.

New `main.usda`
```usda
#usda 1.0

def Scope "root" (
    add references = @./sublayer.usda@
)
{
    over "Prim" (
        add references = @./reference.usda@</Another>
    )
    {
    }
}
```

And in this example, `reference.usda`'s opinion would win, instead.

The beauty of `</root>` is that you don't have to use references. If
your 2 layers both contain `</root>`, you can still sublayer them
normally. The difference with a USD stage that doesn't use `</root>`
and one that does is, __you now you have greater control over how value
resolution occurs.__


### Advantages Of `</root>`
#### You Can "List-Edit" Another Layer
By using a reference `</root>`, you get the effects of sublayering by
using the references composition arc. The references composition arc is
list-editable and can edit any nested layer(s). Whereas sublayers cannot
edit nested layers.

#### You Can Now Choose How Strong Another Layer Will Be
If we want to make "sublayer.usda" stronger again, all you have to do is
sublayer it into "main.usda" like you normally would.

`main.usda`
```usda
#usda 1.0
(
    subLayers = @./sublayer.usda@
)

over Scope "root"
{
    over "Prim" (
        add references = @./reference.usda@</Another>
    )
    {
    }
}
```

Since "root" is defined in "sublayer.usda" and over'ed in "main.usda",
the opinions from both layers will sublayer correctly.


#### When Referencing, You Don't Need To Add An Explicit primPath
Any layer that uses `</root>` as the container for all Prims can re-use
that Prim as the defaultPrim for the layer. Any other layer that needs
to reference a USD layer with `</root>` in it can then be referred to by
its asset path.


### Disadvantages Of `</root>`
#### Weaker Opinions
If you bring in a layer's `</root>` as a reference, that entire layer's
direct opinions will be weaker than references that are added to the
current layer. The demonstration above proves this. But when you do
this, you're making a conscious decision to make the referenced layer
weaker than if it were a sublayer. There's no such thing as a partial
sublayer so this will affect all arcs in the current layer.

This could be considered as an advantage, depending on what you're looking for.


#### References Will Be Slower Than SubLayers
The other disadvantage of using a reference `</root>` instead of a
sublayer is that sublayers are easier to understand and resolve faster.
You take a performance hit by preferring references over sublayers doing
this.


Keep these pros and cons in mind so that you can choose the right arc
for the right situation.
