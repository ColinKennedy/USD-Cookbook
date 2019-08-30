## Custom Schemas
Pixar has a tutorial for [Generating New Schema Classes](https://graphics.pixar.com/usd/docs/Generating-New-Schema-Classes.html).
The tutorial goes into great detail about the formatting and specifics
about the schema.usda but the tutorial fails to mention 2 important points:

- Its instructions assume that you are building into the USD source
tree. Pipelines rarely do this. The tutorial probably did this for
simplicity but it leaves a lot to be desired.
- The tutorial doesn't cover how Python bindings are created (spoiler:
You need to manually write a couple files that usdGenSchema doesn't create for you!)

This project implements a "real-world setup" using Pixar's tutorial as its base.


## How To Read Through This Project's Folders
First, compile the plugin with the
[compiling_the_schema](compiling_the_schema).
[compiling_the_schema](compiling_the_schema) creates the SimplePrim,
ComplexPrim, and ParamsAPI schemas. Technically this is all you really
need to do but it's a good idea to run your compiled code against
a C++ / Python project to make sure everything is working okay.

The other folders,
[testing_the_compiled_schema_cpp](testing_the_compiled_schema_cpp) and
[testing_the_compiled_schema_python](testing_the_compiled_schema_python)
, are test projects that include the custom schemas that you would have
just built. These can be used to show how to include the schemas and
also check to make sure nothing broke in the process.


## References
[RodeoFX's Replace Resolver Plugin](https://github.com/rodeofx/rdo_replace_resolver)

[USD's Custom Schema Class Tutorial](https://graphics.pixar.com/usd/docs/Generating-New-Schema-Classes.html)

[A helpful hint that usdGenSchema doesn't make every required file (module.cpp / moduleDeps.cpp)](https://groups.google.com/d/msg/usd-interest/r0j0l-aJ5Ok/hAdy-ZkWGQAJ)

[USDResearch Repository](https://github.com/SFukuoka1227/USDResearch/tree/master/schema). It's written in Japanese but was still useful
