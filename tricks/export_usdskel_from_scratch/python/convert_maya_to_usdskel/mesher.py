#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A set of functions that are focused on getting Maya meshes and writing meshes to USD."""

# IMPORT THIRD-PARTY LIBRARIES
from maya import cmds
from pxr import UsdGeom

# IMPORT LOCAL LIBRARIES
from . import helper


def get_overall_bounding_box(meshes, time_code):
    """Find a bounding box that surrounds every given Maya mesh.

    Args:
        meshes (list[str]): The paths to Maya meshes that each have bounding box data.
        time_code (float or int): The time to get bounding box data for.

    Raises:
        ValueError: If `meshes` is empty.

    Returns:
        tuple[tuple[float, float, float], tuple[float, float, float]]:
            The two 3D points that surround the bounding boxes of every given mesh.

    """
    if not meshes:
        return ValueError('Meshes "{meshes}" cannot be empty.'.format(meshes=meshes))

    minimum_x_values = set()
    minimum_y_values = set()
    minimum_z_values = set()
    maximum_x_values = set()
    maximum_y_values = set()
    maximum_z_values = set()

    for mesh in meshes:
        minimum_x_values.add(cmds.getAttr(mesh + ".boundingBoxMinX", time=time_code))
        minimum_y_values.add(cmds.getAttr(mesh + ".boundingBoxMinY", time=time_code))
        minimum_z_values.add(cmds.getAttr(mesh + ".boundingBoxMinZ", time=time_code))

        maximum_x_values.add(cmds.getAttr(mesh + ".boundingBoxMaxX", time=time_code))
        maximum_y_values.add(cmds.getAttr(mesh + ".boundingBoxMaxY", time=time_code))
        maximum_z_values.add(cmds.getAttr(mesh + ".boundingBoxMaxZ", time=time_code))

    minimum_x = sorted(minimum_x_values)[0]
    minimum_y = sorted(minimum_y_values)[0]
    minimum_z = sorted(minimum_z_values)[0]
    maximum_x = sorted(maximum_x_values)[0]
    maximum_y = sorted(maximum_y_values)[0]
    maximum_z = sorted(maximum_z_values)[0]

    return (
        (minimum_x, minimum_y, minimum_z),
        (maximum_x, maximum_y, maximum_z),
    )


def get_connected_meshes(joint):
    """Find every mesh that is skinned for some joint.

    Note:
        This function only works for Maya skin clusters.

    Args:
        str (str): The name of some Maya joint that is skinned to 1+ Maya mesh.

    Returns:
        set[str]: The Maya meshes that `joint` affects.

    """
    clusters = set(
        node
        for node in cmds.listConnections(joint, destination=True) or []
        if cmds.nodeType(node) == "skinCluster"
    )

    meshes = set()

    for cluster in clusters:
        for node in cmds.listConnections(cluster + ".outputGeometry", destination=True):
            node = cmds.ls(node, long=True)[0]  # Force the full path to the node
            meshes.add(node)

    return meshes
