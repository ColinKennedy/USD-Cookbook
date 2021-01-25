## Summary

According to the [USD
Glossary](https://graphics.pixar.com/usd/docs/USD-Glossary.html#USDGloss
ary-ModelHierarchy), USD kinds make up a "model hierarchy". Contracy
to the name, "model" in this case just means a "table of contents of
important Prims". "model" doesn't mean "only geometry Prims". The Prims
can be anything.

So what does that actually mean in practice though?

It means your model hierarchy must look like this and only this

{assembly|group}(/{component/(subcomponent)})

That syntax is a bit weird so let's list out the rules

- The top-level Prim must start with a Model kind
- All child Prims in the Model hierarchy, starting from that point, must also be Model kinds
- You're allowed to nest and mix any number of assembly or group Model kinds
- The only kind that is allowed below a component kind is subcomponent
- Subcomponent kinds are not "real" Model kinds


## Valid Model Hierarchies

Here's some examples of valid Model hierarchies

- valid_1.usda
- valid_2.usda
- valid_3.usda

valid_1.usda
```usda
#usda 1.0

def Scope "root" (
    kind = "component"
)
{
}
```

valid_2.usda
```usda
#usda 1.0

def Scope "root" (
    kind = "assembly"
)
{
    def Scope "some_group" (
        kind = "group"
    )
    {
        def Scope "last_one" (
            kind = "component"
        )
        {
        }
    }
}
```

valid_3.usda

## Invalid Model Hierarchies
