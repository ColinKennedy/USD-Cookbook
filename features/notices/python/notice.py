#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT FUTURE LIBRARIES
from __future__ import print_function

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Tf, Usd


def update(notice, sender):
    """Print example data that you can get from the callback."""
    print("The triggered sender", notice.GetStage())
    print("Resynced paths", notice.GetResyncedPaths())
    print("The path Prim path that was affected", notice.GetChangedInfoOnlyPaths())
    print("Affected object", notice.AffectedObject(sender.GetPrimAtPath("/SomeSphere")))
    print("Resynced?", notice.ResyncedObject(sender.GetPrimAtPath("/SomeSphere")))
    print("Changed?", notice.ChangedInfoOnly(sender.GetPrimAtPath("/SomeSphere")))


def objects_changed(notice, sender):
    print("Objects changed", notice, sender)


def stage_changed(notice, sender):
    print("Stage changed", notice, sender)


def target_changed(notice, sender):
    print("Target changed", notice, sender)


def main():
    """Run the main execution of the current script."""
    stage = Usd.Stage.CreateInMemory()

    # XXX : You can register to a specific `pxr.Usd.Stage` Important:
    # You must assign `Register` to a variable (even if you don't run
    # `del` on it later) or the callback goes out of scope and does nothing.
    #
    updated = Tf.Notice.Register(Usd.Notice.ObjectsChanged, update, stage)
    stage.DefinePrim("/SomeSphere")
    stage.GetPrimAtPath("/SomeSphere").SetMetadata("comment", "")

    # XXX : `del` revokes the notice
    del updated
    stage.DefinePrim("/SomeSphere2")
    stage.GetPrimAtPath("/SomeSphere2").SetMetadata("comment", "")

    # XXX : You can also register notices for the session (not to any specific stage)
    # XXX : `pxr.Usd.Notice` comes with 3 types
    #
    # `Usd.Notice.ObjectsChanged`
    # `Usd.Notice.StageContentsChanged`
    # `Usd.Notice.StageEditTargetChanged`
    #
    contents = Tf.Notice.RegisterGlobally(
        Usd.Notice.StageContentsChanged, stage_changed
    )

    objects = Tf.Notice.RegisterGlobally(Usd.Notice.ObjectsChanged, objects_changed)

    targets = Tf.Notice.RegisterGlobally(
        Usd.Notice.StageEditTargetChanged, target_changed
    )

    stage.DefinePrim("/Foo")
    stage.SetEditTarget(stage.GetSessionLayer())
    stage.GetPrimAtPath("/Foo").SetMetadata("comment", "")
    stage.GetPrimAtPath("/Foo").SetMetadata("comment", "x")
    print("Done")


if __name__ == "__main__":
    main()
