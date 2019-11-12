# Quick Reference

This section shows how to define and display a custom Gprim in Hydra.
In DCC terminology, like Houdini, this process means creating a
"procedural".

The basic steps are as follows.

- Create a new Gprim type.
- Create an adapter so Hydra knows how to display that type.

This section will create a "star" Gprim, based on Houdini's "SOP_Star" HDK example file.
[Basic (scarse) documentation for SOP_Star here](https://www.sidefx.com/docs/hdk/_h_d_k__intro__creating_plugins.html#HDK_Intro_CreatingPlugins_Building)


## Create A New GPrim Type
The steps for this are identical to the 
[custom_schemas_with_python_bindings](../../plugins/custom_schemas_with_python_bindings)
project. The only main difference is that the Star Schema inherits from
Gprim, not Typed.

[star_gprim](star_gprim) is the C++ project that must be compiled before
continuing.


## Create An Adapter
(This section assumes that you've completed "Create A New Gprim Type")

The last step is to explain how to display your Prim.

[star_adapter](star_adapter) sets this up. Follow its steps to complete
this section.
