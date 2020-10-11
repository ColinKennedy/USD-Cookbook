#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""All camera utility-related functions."""

import re

from pxr import Sdf

_NUMBERED_NAME = re.compile(r"(?P<prefix>.*)(?P<number>\d+)$")


def _guess_unique_path(text, paths):
    """Make sure `text` is a unique, according to the Prims in `stage`.

    Args:
        text (str):
            Some text to make unique.
        paths (container[:usd:`SdfPath`]):
            The Prim paths which `text` will check itself against.

    Returns:
        str: The new, unique path. If `text` is already unique, it is directly returned.

    """

    def _increment(text):
        match = _NUMBERED_NAME.match(text)

        if not match:
            return text + "_copy"

        value = int(match.group("number")) + 1

        return match.group("prefix") + str(value)

    path = Sdf.Path(text)

    for path_ in paths:
        if path == path_:
            text = _increment(text)

            return _guess_unique_path(text, paths)

    return text


def set_unique_path(widget, paths):
    """Update the current text in `widget` to be unique, according to `paths`.

    Args:
        widget (:class:`PySide.QtGui.QLineEdit`):
            A widget to modify.
        paths (container[:usd:`SdfPath`]):
            The Prim paths which `widget` will be compared against.

    """
    text = widget.text()
    text = _guess_unique_path(text, paths)
    widget.setText(text)
