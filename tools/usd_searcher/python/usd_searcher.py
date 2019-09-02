#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A module that can be used to search any text in USD files, recursively.

Attributes:
    Match (`collections.namedtuple`):
        A container that represents a matched file / line. It has 3 members:
        "path" (str): The absolute path on-disk where a match was found.
        "row" (int): The 0-based line number where the match was found.
        "text" (str): The line that matched a search phrase.

"""

# IMPORT FUTURE LIBRARIES
from __future__ import division

# IMPORT STANDARD LIBRARIES
import collections
import functools
import mimetypes
import os
import re
import string

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Sdf, UsdUtils

_EXTENSIONS = tuple(
    ("." + extension for extension in Sdf.FileFormat.FindAllFileFormatExtensions())
)

Match = collections.namedtuple("Match", "path row text")


class UnresolvedFound(Exception):
    """An exception class for when an Asset path cannot resolved to a path on-disk."""

    def __init__(self, message, paths):
        """Store an error message and the unresolved paths.

        Args:
            message (str): A message to the user about what went wrong.
            paths (set[str]): The Asset paths/URIs that could not be resolved.

        """
        super(UnresolvedFound, self).__init__(message)

        self.paths = paths


def _search_assets(assets, matcher):
    """set[`usd_searcher.Match`]: Find every match for every given Asset."""
    matches = set()

    for asset in assets:
        with open(asset, "r") as handler:
            for index, line in enumerate(handler.readlines()):
                if matcher(line):
                    matches.add(Match(asset, index, line))

    return matches


def _search_layers(layers, matcher):
    """set[`usd_searcher.Match`]: Find every match for every given USD Layer."""
    matches = set()

    for layer in layers:
        for index, line in enumerate(layer.ExportToString().splitlines()):
            if matcher(line):
                matches.add(Match(layer.realPath, index, line))

    return matches


def istext(filename):
    """Check if the given path is an ASCII-based text file.

    References:
        https://stackoverflow.com/a/1446870/3626104

    Args:
        filename (str): The path to a file on-disk.

    Returns:
        bool: If the file is not binary.

    """
    s = open(filename).read(512)
    text_characters = "".join(map(chr, range(32, 127)) + list("\n\r\t\b"))
    _null_trans = string.maketrans("", "")

    if not s:
        # Empty files are considered text
        return True

    if "\0" in s:
        # Files with null bytes are likely binary
        return False
    # Get the non-text characters (maps a character to itself then
    # use the 'remove' option to get rid of the text characters.)
    t = s.translate(_null_trans, text_characters)

    # If more than 30% non-text characters, then
    # this is considered a binary file
    if float(len(t)) / float(len(s)) > 0.30:
        return False

    return True


def search(
    phrase,
    path,
    regex=False,
    include_layers=True,
    include_assets=False,
    ignore_binary=True,
    ignore_unresolved=True,
):
    """Search for some phrase recursively, starting at some USD Layer.

    Args:
        phrase (str): The text to search for.
        path (str): The absolute path to USD file to search for.
        regex (bool, optional):
            If True then `phrase` is treated as a regular expression.
            If False then `phrase` is treated as a substring of each line
            and searched that way, instead. Default is False.
        include_layers (bool, optional):
            If True, search for the phrase in USD Layers. If False,
            exclude USD Layers from search results. Default is True.
        include_assets (bool, optional):
            If True, search for the phrase in all Asset paths. If False,
            don't search any Asset paths. Default is False.
        ignore_binary (bool, optional):
            If True then USD crate files and any other binary Asset
            resource will not be included in results. If False then
            binary files will be searched for, instead. Default is True.
        ignore_unresolved (bool, optional):
            If False and this function cannot resolve a USD Layer
            path to a file on-disk then this function will raise an
            exception. If True then this function will continue even if
            there are unresolved paths. Default is True.

    Raises:
        ValueError: If `include_layers` and `include_assets` are both false.
        UnresolvedFound: If `ignore_unresolved` is False and 1+ unresolved paths are found.

    Returns:
        set[`usd_searcher.Match`]:
            Every match that was found, the line it was found in, its
            line number, and the full path to the file where the match
            was found.

    """

    def _default_matcher(phrase, line):
        return phrase in line

    if not include_layers and not include_assets:
        raise ValueError("`include_layers` and `include_assets` cannot both be False.")

    if not os.path.isfile(path):
        raise ValueError('"{path}" does not exist.'.format(path=path))

    if not path.endswith(_EXTENSIONS):
        raise ValueError('"{path}" is not a valid USD file.'.format(path=path))

    if regex:
        matcher = re.compile(phrase).search
    else:
        matcher = functools.partial(_default_matcher, phrase)

    layers, assets, unresolved = UsdUtils.ComputeAllDependencies(path)

    if not ignore_unresolved and unresolved:
        raise UnresolvedFound(
            'Unresolved paths "{unresolved}" were found. Re-run with ignore_unresolved '
            "set to True or fix the unresolved paths.".format(unresolved=unresolved),
            unresolved,
        )

    matches = set()

    if ignore_binary:
        layers = [layer for layer in layers if istext(layer.realPath)]

    assets = [asset for asset in assets if istext(asset)]

    if include_layers:
        matches.update(_search_layers(layers, matcher))

    if include_assets:
        matches.update(_search_assets(assets, matcher))

    return matches
