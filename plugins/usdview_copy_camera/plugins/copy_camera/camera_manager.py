#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from pxr import Sdf

_NUMBERED_NAME = re.compile("(?P<prefix>.*)(?P<number>\d+)$")


def _guess_unique_path(text, stage):
    def _increment(text):
        match = _NUMBERED_NAME.match(text)

        if not match:
            return text + "_copy"

        value = int(match.group("number")) + 1

        return match.group("prefix") + str(value)

    path = Sdf.Path(text)

    for prim in stage.TraverseAll():
        if path == prim.GetPath():
            text = _increment(text)

            return _guess_unique_path(text, stage)

    return text


def set_unique_camera_path(window, stage):
    text = window.get_text()
    text = _guess_unique_path(text, stage)
    window.set_text(text)
