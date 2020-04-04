#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This is a module docstring.

Let's try linking to the USD API documentation's stage class.

:usd:`pxr::UsdStage`.

^^^ That link should be clickable

Also you can alias links. e.g.

:usd:`A method of some class <pxr::SdfPath::GetParentPath>`.

"""


# This docstring is an optional style for those using Google Style.
def get_prim_path1(prim):
    """Send Prim variant set information to the terminal.

    Note:
        This docstring is written in Google Style. It requires the
        napoleon plugin to render correctly.

    Args:
        prim (:usd:`pxr::UsdPrim`): Some USD object.

    Returns:
        :usd:`pxr::SdfPath`: The namespace where `prim` lives.

    """
    return prim.GetPath()


# This docstring doesn't require any external Sphinx extensions to work.
def get_prim_path2(prim):
    """Send Prim variant set information to the terminal.

    .. note ::
        This docstring does not require any plugins to render with Sphinx.

    :param prim: Some USD object.
    :type prim: :usd:`pxr::UsdPrim`

    :return: The namespace where `prim` lives.
    :rtype: :usd:`pxr::SdfPath`

    """
    return prim.GetPath()
