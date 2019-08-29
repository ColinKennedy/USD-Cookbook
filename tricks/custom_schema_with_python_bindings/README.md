## Custom Schemas
Pixar has a tutorial for [Generating New Schema Classes](https://graphics.pixar.com/usd/docs/Generating-New-Schema-Classes.html).
The tutorial goes into great detail about the formatting and specifics
about the schema.usda but the tutorial fails to mention 2 things:

- Its instructions assume that you are building into the USD source
tree. Pipelines rarely do this. The tutorial probably did this for
simplicity but it leaves a lot to be desired.
- The tutorial doesn't cover how Python bindings are created (spoiler:
You need more than just the files that usdGenSchema creates)

This project implements a "real-world setup" using Pixar's tutorial as its base.

# TODO
- Add the Python test project
- Add the C++ test project
- Link the documentation to every other documentation else


### What's Inside
[compiling_the_schema](compiling_the_schema) creates the SimplePrim,
ComplexPrim, and ParamsAPI schemas.

[testing_the_compiled_schema_cpp](testing_the_compiled_schema_cpp) is an
example C++ project that uses the created schemas.

[testing_the_compiled_schema_python](testing_the_compiled_schema_python)
is an example Python project that also uses the created schemas.


## References
[RodeoFX's Replace Resolver Plugin](https://github.com/rodeofx/rdo_replace_resolver)

[USD's Custom Schema Class Tutorial](https://graphics.pixar.com/usd/docs/Generating-New-Schema-Classes.html)

[A helpful hint that usdGenSchema doesn't make every required file (module.cpp / moduleDeps.cpp)](https://groups.google.com/d/msg/usd-interest/r0j0l-aJ5Ok/hAdy-ZkWGQAJ)

[USDResearch Repository](https://github.com/SFukuoka1227/USDResearch/tree/master/schema). It's in Japanese but was still useful
