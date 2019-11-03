# Quick Explanation
If your background is from a C or C-like background, this next tip may
come as a bit of a surprise.

```usda
#usda 1.0

def Xform "root" (
    prepend variantSets = "something"
)
{
    variantSet "something" = {
		# ...
    }
}
```

The "something" `variantSet` is **not** inside of `</root>`. It **wraps**
`</root>`. This means that you can change metadata depending on the
selected variant.


```usda
#usda 1.0

def Xform "root" (
    prepend variantSets = "something"
)
{
    variantSet "something" = {
        "option_a" (
            some_metadata = "foo"
        ) {

        }
        "option_b" {

        }
    }
}
```

## Example

- Open [metadata_swap.usda](metadata_swap.usda) in usdview to see the above example, live.
- Open [arcs.usda](arcs.usda) to see an example of how to use variants to control composition arcs.


When there's no variant selection, `</root>` has no "some_metadata"
authored. Metadata is missing for "option_b", too. But if it's '"option_a",
"some_metadata" is authored with a value of "foo".


### VariantSets As Composition Arc Managers
As mentioned in the
[relationship_forwarding](../../concepts/relationship_forwarding)
article, you can use VariantSet as multiplexer and de-multiplexer.

Since we can modify opinions inside a Prim's ()s, that also means that
we can modify its composition arcs, using variant selections.


```usda
#usda 1.0
(
	startTimeCode = 0
	endTimeCode = 10
)

def Xform "transform" (
    add references = [
        @model.usda@,
        @surfacing.usda@,
    ]
    prepend variantSets = "state"
)
{
    variantSet "state" = {
        "blue" (
            add references = @surfacing_blue.usda@
        ) {
        }
        "motion" (
            add references = @animation.usda@
        ) {

        }
        "sphere" (
            add references = @sphere.usda@
        ) {

        }
    }
}
```

In conclusion, variantSets aren't strictly "inside" of a Prim. They are
that Prim.


### Limitations
From basic experimentation, it looks like you cannot

- Delete a reference within a variantSet of the same Prim
- Cannot dynamically change the type of a Prim using a variant
- Cannot change the name of the Prim

Everything else though, metadata, attributes, whatever, is all up for grabs.
