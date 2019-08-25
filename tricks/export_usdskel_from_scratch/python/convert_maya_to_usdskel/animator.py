#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A set of helper functions related to animation and keys in Maya."""

import collections
import sys

from maya import cmds
from pxr import Gf

from . import helper


def get_animation_range(nodes):
    """Find the earliest and latest animation keyframe times from some animated nodes.

    Args:
        nodes (list[str]): The animated Maya nodes that will be checked for keys.

    Raises:
        RuntimeError: If no start/end range could be found.

    Returns:
        tuple[float or int, float or int]: The found start/end times.

    """

    def _get_maximum_key(node, default):
        try:
            return max(cmds.keyframe(node, q=True) or [])
        except ValueError:
            return default

    def _get_minimum_key(node, default):
        try:
            return min(cmds.keyframe(node, q=True) or [])
        except ValueError:
            return default

    _start_default = sys.maxsize
    _end_default = -1 * sys.maxsize
    start = _start_default
    end = _end_default

    for node in nodes:
        start_ = _get_minimum_key(node, _start_default)

        if start_ < start:
            start = start_

        end_ = _get_maximum_key(node, _end_default)

        if end_ > end:
            end = end_

    if start == _start_default or end == _end_default:
        raise RuntimeError(
            'No start/end time could be found from nodes, "{nodes}".'.format(
                nodes=sorted(nodes)
            )
        )

    return (start, end)


def get_joint_world_space_transforms(joints, times):
    """Get the world-space matrices for every given joint at every given time.

    Args:
        joints (list[str]):
            The paths to every Maya node to get world-space matrices for.
        times (iter[float or int]):
            The time code values that will be used to query the
            transforms for each joint in `joints`.

    Returns:
        dict[int or float, list[int]]:
            The matrices for every joint in `joints` for each time in
            `times`. The return values is a **flat** matrix. (It's not a
            4x4 matrix, it's a list of 16 elements.)

    """
    output = collections.defaultdict(list)

    for node_time_transforms in get_node_transforms_at_times(joints, times, "world"):
        for time_code, time_transform in zip(times, node_time_transforms):
            output[time_code].append(time_transform)

    return dict(output)


def get_node_transforms_at_times(nodes, times, space):
    """Get the transform matrices of every node at the given times.

    Args:
        nodes (iter[str]):
            The Maya nodes to get transformation data from.
        times (iter[float or int]):
            The values that will be queried for each node-transform.
        space (str):
            The possible transformations that can be queried.
            Options: ["local", "world"].

    Raises:
        ValueError: If the given `space` is not "local" or "world".

    Returns:
        list[list[`pxr.Gf.Matrix4d`]]:
            The transforms for each node in `nodes` for each time in `times`.
            In other words, the list is stored like this
            - node1
                - time1 transform
                - time2 transform
                - time3 transform
            - node2
                - time1 transform
                - time2 transform
                - time3 transform

    """
    spaces = {"local": ".matrix", "world": ".worldMatrix"}

    try:
        attribute_name = spaces[space]
    except KeyError:
        raise ValueError(
            'Space "{space}" is invalid. Options were, "{spaces}".'.format(
                space=space, spaces=sorted(spaces)
            )
        )

    transforms = []

    with helper.UndoChunk():
        matrix_node = cmds.createNode("multMatrix")
        matrix_input = matrix_node + ".matrixIn[0]"

        for node in nodes:
            cmds.connectAttr(node + attribute_name, matrix_input, force=True)
            time_transforms = []

            for time_code in times:
                time_transforms.append(
                    Gf.Matrix4d(*cmds.getAttr(matrix_input, time=time_code))
                )

            transforms.append(time_transforms)

    return transforms


def get_node_transforms_at_time(nodes, time_code, space):
    """Get the transform matrices of every node at the given times.

    Args:
        nodes (iter[str]):
            The Maya nodes to get transformation data from.
        time_code (float or int):
            The value that will be queried for each node.
        space (str):
            The possible transformations that can be queried.
            Options: ["local", "world"].

    Raises:
        ValueError: If the given `space` is not "local" or "world".

    Returns:
        list[`pxr.Gf.Matrix4d`]:
            The transform of each node in `nodes` for the given time.

    """
    transforms_per_time = get_node_transforms_at_times(nodes, [time_code], space)

    return [transform[0] for transform in transforms_per_time]
