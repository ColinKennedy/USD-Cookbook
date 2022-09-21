## Summary

According to the
[USD Glossary](https://graphics.pixar.com/usd/docs/USD-Glossary.html#USDGlossary-ModelHierarchy)
USD kinds make up a "model hierarchy". Contrary to the name, "model" in
this case just means a "table of contents of important Prims". "model"
doesn't mean "only geometry Prims". The Prims can be anything.

So what does that actually mean in practice though?

It means your model hierarchy must look like this and only this

{assembly|group}/{component/subcomponent}

That syntax is a bit weird so let's list out the rules

- The top-level Prim must start with a Model kind
- All child Prims in the Model hierarchy, starting from that point, must also be Model kinds
- You're allowed to nest and mix any number of assembly or group Model kinds
- The only kind that is allowed below a component kind is subcomponent
- Subcomponent kinds are technically not Model kinds


## Valid/Invalid Model Hierarchies

In the sections below, we'll talk about some example Model kind hierarchies and why they are invalid.

To double-check this page, run this

```sh
python check.py
```

You should see a print out like this

```
valid_1 expects True: True
valid_2 </root> expects True: True
valid_2 </root/some_group> expects True: True
```

If any value doesn't match the expected, then something in this guide is
wrong or was changed in a later USD release.


### Examples

Here's some examples of valid Model hierarchies

- [valid_1.usda](valid_1.usda)
- [valid_2.usda](valid_2.usda)
- [valid_3.usda](valid_3.usda)
- [valid_4.usda](valid_4.usda)
- [valid_5.usda](valid_5.usda)
- [invalid_1.usda](invalid_1.usda)
- [invalid_2.usda](invalid_2.usda)
- [invalid_2a.usda](invalid_2a.usda)
- [invalid_2b.usda](invalid_2b.usda)
- [invalid_2c.usda](invalid_2c.usda)
- [invalid_2d.usda](invalid_2d.usda)


### "Invalids" Breakdown
#### invalid_1.usda

```usda
#usda 1.0

def Scope "root" (
    doc = "This has no kind defined. So it isn't a Model"
)
{
}
```

**Reason**: There's no defined kind so obviously it's not a valid Model

**Fix**: Define a kind. "assembly", "group", or "component" are all options.


#### invalid_2.usda

```usda
#usda 1.0

def Scope "root" (
    doc = "This has a valid Model kind"
    kind = "assembly"
)
{
    def Scope "some_group" (
        doc = "This has a valid Model kind"
        kind = "group"
    )
    {
        def Scope "child" (
            doc = "But don't expect this to be a valid Model kind"
        )
        {
        }
    }
}

```

**Reason**: ``</root>`` and ``</root/some_group>`` are perfectly valid. But
``</root/some_group/child>`` is not a Model because it doesn't define a
kind. The Prim being "inside" of a valid Model hierarchy doesn't make
``</root/some_group/child>`` itself valid.

**Fix**: If the intent is for ``</root/some_group/child>`` to be part of the
Model hierarchy, add "assembly", "group", or "component"


#### invalid_2b.usda

```usda
#usda 1.0

def Scope "root"
{
    def Scope "inner" (
        doc = "This whole chain of kinds are invalid because the top-level Prim has no kind"
        kind = "assembly"
    )
    {
        def Scope "some_group" (
            doc = "This whole chain of kinds are invalid because the top-level Prim has no kind"
            kind = "group"
        )
        {
            def Scope "last_one" (
                doc = "This whole chain of kinds are invalid because the top-level Prim has no kind"
                kind = "component"
            )
            {
            }
        }
    }
}
```

**Reason**: Normally this Model hierarchy would be valid but because ``</root>`` has no kind, the whole chain is not valid.

**Fix**: Add "assembly" or "group" kind to ``</root>`` or get rid of ``</root>`` completely.

#### invalid_2c.usda

```usda
#usda 1.0

def Scope "root" (
    doc = "This is a valid Model kind"
    kind = "assembly"
)
{
    def Scope "inner" (
        doc = "Because this has no kind, all child Prims are an invalid Model"
    )
    {
        def Scope "some_group" (
            doc = "This is not a Model kind"
            kind = "group"
        )
        {
            def Scope "last_one" (
                doc = "This is not a Model kind"
                kind = "component"
            )
            {
            }
        }
    }
}
```

**Reason**: The Model hierarchy is broken by ``</root/inner>``, which has no kind defined.

**Fix**: Add either "assembly" or "group" kind to ``</root/inner>``


#### invalid_2d.usda

```usda
#usda 1.0

def Scope "root" (
    doc = "This is valid"
    kind = "assembly"
)
{
    def Scope "some_group" (
        doc = "This is valid"
        kind = "group"
    )
    {
        def Scope "some_component" (
            doc = "This is valid"
            kind = "component"
        )
        {
            def Scope "inner_invalid_group" (
                doc = "This one isn't valid"
                kind = "group"
            )
            {
            }
        }
    }
}
```

**Reason**: ``</root/some_group/some_component/inner_invalid_group>`` is a
"group" but its parent Prim is "component". You cannot nest "assembly",
"group", or "component" under another "component"

**Fix**: Either make
``</root/some_group/some_component/inner_invalid_group>`` a "subcomponent"
or remove its kind entirely. Either way, that Prim is not going to be a
Model because it's underneath a "component"
