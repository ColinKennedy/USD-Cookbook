import functools
import os
import tempfile
import textwrap

from pxr import Sdf, Usd


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


def create_basic_stage():
    code = textwrap.dedent(
        """\
        #usda 1.0
        (
            defaultPrim = "/Foo/Bar"
        )

        def "Foo"
        {
            def Xform "Bar" (
                "some comment"
            )
            {
                custom float some_property = 1
            }
        }
        """
    )

    with tempfile.NamedTemporaryFile(suffix=".usda", delete=False) as handler:
        handler.write(code)

    stage = Usd.Stage.Open(handler.name)

    return stage


def main():
    """Run the main execution of the current script."""
    base = create_basic_stage()
    stage = Usd.Stage.CreateInMemory()
    add_prim_from_target(stage, base)

    os.remove(base.GetRootLayer().identifier)

    print(stage.ExportToString())


if __name__ == "__main__":
    main()
