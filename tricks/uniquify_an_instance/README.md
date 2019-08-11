# Quick Reference

USD has interesting rules about instancing. If you're authoring a USD
file from-scratch and you define a Prim inside of an Instanced Prim,
that's considered legal USD code (it won't produce an error or warning). 
But if you load it in usdview, the Prim will not exist.

Load [example.usda](python/example.usda) and you'll see what I mean.

The Prim "SomePrimThatWillNotExist" will not be in usdview but it is
defined in the .usda file.

But if you try to actually programmatically write the same code, it
will raise an exception (because it is technically wrong).

The best way to make sure that you don't raise an exception while
authoring opinions on a Prim is to make sure that you aren't writing
over an instance. The easiest way is to just check for it.

```python
if prim.IsInstance():
    prim.SetInstanceable(False)
    # ... your opinion here ...
```

Also notice that the cpp and python versions create slightly different results.
