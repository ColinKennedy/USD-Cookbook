# Quick Reference
Sometimes you need to reference a Prim like </Foo/Bar> into anotheer
stage but, when you do that, you want to keep the name and type of "Bar"
in the other stage.

This short snippet shows you how to do it. There's nothing much to this
trick. Just query the type / name of some Prim path or fall back to the
stage's defaultPrim to get the same information.


### Python

```python
def add_prim_from_target(stage, target, prim_path=""):
    if not prim_path:
        prim = target.GetDefaultPrim() or target.GetPrimAtPath(
            target.GetRootLayer().defaultPrim
        )
    else:
        prim = target.GetPrimAtPath(prim_path)

    if not prim.IsValid():
        raise RuntimeError(
            'Prim path "{prim_path}" could not be found and there is not '
            "default Prim to fall back on.".format(prim_path=prim_path)
        )

    creators = {
        Sdf.SpecifierClass: stage.CreateClassPrim,
        Sdf.SpecifierDef: functools.partial(
            stage.DefinePrim, typeName=prim.GetTypeName()
        ),
        Sdf.SpecifierOver: stage.OverridePrim,
    }

    creator = creators[prim.GetSpecifier()]
    created_prim = creator(prim.GetPath())

    created_prim.GetReferences().AddReference(
        assetPath=target.GetRootLayer().identifier, primPath=prim.GetPath()
    )
```
