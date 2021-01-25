#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os

from pxr import Usd


_CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))


def _print_invalids():
    stage = Usd.Stage.Open(os.path.join(_CURRENT_DIRECTORY, "invalid_1.usda"))
    model = Usd.ModelAPI(stage.GetPrimAtPath("/root"))
    print("invalid_1 is False", model.IsModel())

    stage = Usd.Stage.Open(os.path.join(_CURRENT_DIRECTORY, "invalid_2.usda"))
    model = Usd.ModelAPI(stage.GetPrimAtPath("/root"))
    print("invalid_2 </root> is True", model.IsModel())
    model = Usd.ModelAPI(stage.GetPrimAtPath("/root/some_group"))
    print("invalid_2 </root/some_group> is True", model.IsModel())
    model = Usd.ModelAPI(stage.GetPrimAtPath("/root/some_group/child"))
    print("invalid_2 </root/some_group/child> is False", model.IsModel())

    stage = Usd.Stage.Open(os.path.join(_CURRENT_DIRECTORY, "invalid_2b.usda"))
    model = Usd.ModelAPI(stage.GetPrimAtPath("/root/inner"))
    print("invalid_2b </root> is False", model.IsModel())
    model = Usd.ModelAPI(stage.GetPrimAtPath("/root/inner/some_group"))
    print("invalid_2b </root/inner/some_group> is False", model.IsModel())
    model = Usd.ModelAPI(stage.GetPrimAtPath("/root/inner/some_group/last_one"))
    print("invalid_2b </root/inner/some_group/last_one> is False", model.IsModel())

    stage = Usd.Stage.Open(os.path.join(_CURRENT_DIRECTORY, "invalid_2c.usda"))
    model = Usd.ModelAPI(stage.GetPrimAtPath("/root"))
    print("invalid_2c </root> is True", model.IsModel())
    model = Usd.ModelAPI(stage.GetPrimAtPath("/root/inner"))
    print("invalid_2c </root/inner> is False", model.IsModel())
    model = Usd.ModelAPI(stage.GetPrimAtPath("/root/inner/some_group"))
    print("invalid_2c </root/inner/some_group> is False", model.IsModel())
    model = Usd.ModelAPI(stage.GetPrimAtPath("/root/inner/some_group/last_one"))
    print("invalid_2c </root/inner/some_group/last_one> is False", model.IsModel())

    stage = Usd.Stage.Open(os.path.join(_CURRENT_DIRECTORY, "invalid_2d.usda"))
    model = Usd.ModelAPI(stage.GetPrimAtPath("/root"))
    print("invalid_2d </root> is True", model.IsModel())
    model = Usd.ModelAPI(stage.GetPrimAtPath("/root/some_group"))
    print("invalid_2d </root/some_group> is True", model.IsModel())
    model = Usd.ModelAPI(stage.GetPrimAtPath("/root/some_group/some_component"))
    print("invalid_2d </root/some_group/some_component> is True", model.IsModel())
    model = Usd.ModelAPI(stage.GetPrimAtPath("/root/some_group/some_component/inner_invalid_group"))
    print("invalid_2d </root/some_group/some_component/inner_invalid_group> is False", model.IsModel())


def _print_valids():
    stage = Usd.Stage.Open(os.path.join(_CURRENT_DIRECTORY, "valid_1.usda"))
    model = Usd.ModelAPI(stage.GetPrimAtPath("/root"))
    print("valid_1 is True", model.IsModel())

    stage = Usd.Stage.Open(os.path.join(_CURRENT_DIRECTORY, "valid_2.usda"))
    model = Usd.ModelAPI(stage.GetPrimAtPath("/root"))
    print("valid_2 </root> is True", model.IsModel())
    model = Usd.ModelAPI(stage.GetPrimAtPath("/root/some_group"))
    print("valid_2 </root/some_group> is True", model.IsModel())
    model = Usd.ModelAPI(stage.GetPrimAtPath("/root/some_group/last_one"))
    print("valid_2 </root/some_group/last_one> is True", model.IsModel())

    stage = Usd.Stage.Open(os.path.join(_CURRENT_DIRECTORY, "valid_3.usda"))
    model = Usd.ModelAPI(stage.GetPrimAtPath("/root"))
    print("valid_3 </root> is True", model.IsModel())
    model = Usd.ModelAPI(stage.GetPrimAtPath("/root/some_group"))
    print("valid_3 </root/some_group> is True", model.IsModel())
    model = Usd.ModelAPI(stage.GetPrimAtPath("/root/some_group/another_assembly"))
    print("valid_3 </root/some_group/another_assembly> is True", model.IsModel())
    model = Usd.ModelAPI(stage.GetPrimAtPath("/root/some_group/another_assembly/last_one"))
    print("valid_3 </root/some_group/another_assembly/last_one> is True", model.IsModel())

    stage = Usd.Stage.Open(os.path.join(_CURRENT_DIRECTORY, "valid_4.usda"))
    model = Usd.ModelAPI(stage.GetPrimAtPath("/root"))
    print("valid_4 </root> is True", model.IsModel())
    model = Usd.ModelAPI(stage.GetPrimAtPath("/root/child"))
    print("valid_4 </root/child> is False", model.IsModel())

    stage = Usd.Stage.Open(os.path.join(_CURRENT_DIRECTORY, "valid_5.usda"))
    model = Usd.ModelAPI(stage.GetPrimAtPath("/root1"))
    print("valid_5 </root1> is True", model.IsModel())
    model = Usd.ModelAPI(stage.GetPrimAtPath("/root2"))
    print("valid_5 </root2> is True", model.IsModel())


def main():
    """Run the main execution of the current script."""
    _print_valids()

    _print_invalids()


if __name__ == "__main__":
    main()
