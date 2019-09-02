Do you want to learn USD but you don't know where to look?

Here are some common questions / things you'd want to learn and how to
find information about it.


## References
[A thorough reference of different USD tools, libraries, and repositories](https://github.com/vfxpro99/usd-resources)
[A community of USD-users](https://groups.google.com/forum/#!forum/usd-interest)


## Questions
### Where can I look to learn about the attributes/relationships/properties that a USD type supports?
If you look at [the USD source
code](https://github.com/PixarAnimationStudios/USD), there is a file
called "schema.usda" that generates most (all?) USD type classes.

Say you want to find the schema for "Sphere" and look up all of its
properties. Clone that repository, cd into it, and run this:

```bash
find . -name "*.usda" | grep -e schema.usda | xargs grep "class Sphere"
```

This will give you the line where that class is defined and you can open
it up in your editor and read all about it.

If you don't find what you need immediately, vary the search terms a bit
and it should be easily findable.


### How do I learn about USDSkel?
[Shows UsdSkel in-use](https://github.com/meshula/usdskelutil)
