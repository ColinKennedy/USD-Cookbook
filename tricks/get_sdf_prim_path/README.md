# Quick Reference
Sometimes, you just need to select a Prim. If you have no variant
sets, you can normally just do `stage.GetPrimAtPath("/foo/bar")` and
you're done. But what if "bar" is defined behind a variant set and that
variant set isn't selected in the current stage? Then GetPrimAtPath
returns an invalid Prim.

The basic steps goes like this
- Have a description of the entire path (including variants + their selections)
- Iterate overy every variant set and forcibly set the selections, one by one
- Then you can get your path


# See Also
TODO
