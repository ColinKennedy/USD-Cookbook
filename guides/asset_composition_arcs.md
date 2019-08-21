# Asset Composition Arcs - The `</root>` of all evil

USD has 3 composition arcs that read files from disk: SubLayers,
References, and Payloads. Between the 3, SubLayers is the simplest and
readest for USD to read.

SubLayers is great but you can't sublayer 50% of another layer.
Or rename any Prim that the layer includes. The good news is that
references can do both of those tasks.

But there's one other problem with sublayers which is not obvious that
references cannot solve. This problem, and its consequences, will be the
subject of this article. And that is: LIVRPS value resolution.

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
opinion in which layer will win?

The answer is "it depends on sublayer.usda". If "sublayer.usda" and
"final_refererence.usda" both offer direct opinions on a `radius`, the
reference's `radius` is ignored. Instead, USD will prefer the `radius`
opinion on the sublayer. Because in LIVRPS, local opinions in sublayers
are treated as if the opinion was authored in the current layer.

You can try this yourself easily, with this code:

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

You might thing that `radius` would be `3` because the "reference.usda"
is authored directly on "/Prim" but that reference is still weaker than
"sublayer.usda". Instead, `sublayer.usda` adds `2` to the stage.

So now that the problem is well defined, what can we do about it?
There's multiple ways of dealing this problem. Here's one simple
solution: Use a `</root>` Prim.


## `</root>` As A Composition Arc Manager
Here's the idea. USD doesn't allow you to reference the root
(pseudo-root) of another layer. But if your target layer has a prim in
it called `</root>` and that `</root>` Prim contains every other Prim in it,
you __can__ target `</root>` and make that a reference.

So instead of this:

```usda
def ""
```
If you have two layers that look like this:

`sublayer.usda`
```usda
#usda 1.0

def Sphere "Prim"
{
	double radius = 2
}
```

You do this:

`sublayer.usda`
```usda
#usda 1.0
(
    defaultPrim = "root"
)

def Scope "root" {
	def Sphere "Prim"
	{
		double radius = 2
	}
}
```

And then in the `main.usda`, instead of using a sublayer, you reference
instead.

`main.usda`
```usda
#usda 1.0

def Scope "root" (
	add references = @./sublayer.usda@
)
{
	# ...
}
```

Because the "sublayer.usda" is brought in as a reference, its local
opinions are not stronger than any other reference in `main.usda`.


`main.usda`
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

Now, instead of getting `2` from "sublayer.usda", </root/Prim> will get
`3` from "reference.usda"!


### Advantages Of `</root>`
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
to reference it in can just point to the file on-disk because we know
that the layer already has the proper defaultPrim assigned.


### Disadvantages Of `</root>`
If you bring in a layer's `</root>` as a reference, that entire layer's
direct opinions will be weaker than references that are added to the
current layer. The demonstration above proves this. But when you do
this, you're making a conscious decision to make the referenced layer
weaker than if it were a sublayer. There's no such thing as a partial
sublayer so this will affect all arcs in the current layer.

This could be considered as an advantage, depending on what you're looking for.

The other disadvantage of using a reference `</root>` instead of a
sublayer is that sublayers are easier to understand and resolve faster.
You take a performance hit by preferring references over sublayers doing
this.


Keep these pros and cons in mind so that you can choose the right arc
for the right situation.
