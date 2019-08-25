#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A set of generic Maya/USD helper functions."""

from maya import cmds


class UndoChunk(object):
    """A Python context that undoes any Maya command that is run inside of it.

    with UndoChunk():
        cmds.polySphere()  # This will get undone, later.

    """

    def __enter__(self):
        """Start recording commands to undo."""
        cmds.undoInfo(openChunk=True)

        return self

    def __exit__(self, exec_type, exec_value, traceback):
        """Undo any commands that were done while this context was left open."""
        needs_undo = not cmds.undoInfo(undoQueueEmpty=True, q=True)
        cmds.undoInfo(closeChunk=True)

        if needs_undo:
            # Only undo if there are any commands to undo. If you try
            # to run undo when there's nothing that can be undone, Maya
            # will raise a RuntimeError.
            #
            cmds.undo()


def _get_root(node, predicate=None):
    """Find the top-most DAG node.

    Args:
        node (str): A Maya node to get the root node of.

    Returns:
        str: The found Maya node. If `node` is the root then it is returned.

    """
    parents = cmds.listRelatives(node, fullPath=True, parent=True) or []
    parents = [parent for parent in parents if predicate(parent)]

    if parents:
        return _get_root(parents[0], predicate=predicate)

    return node


def _convert_to_usd_joint_syntax(joints):
    """Change an entire Maya joint hierarchy into a valid USD hierarchy.

    Args:
        joints (iter[str]):
            The absolute path to a Maya joint hierarchy to convert.
            It's recommended to give all joints in a joint hierarchy
            to this function, to make sure the joints will have the
            right topology order.

    Returns:
        tuple[list[str], list[str]]:
            The converted USD joint paths and the re-ordered Maya joint paths.

    """
    return [convert_maya_path_to_usd(joint).lstrip("/") for joint in joints]


def _get_relative_joint_path(joint, root):
    """Get a Maya node path that is relative to some root Maya node.

    This function is mainly so that we can convert an absolute Maya joint path
    into a relative path rooted as a UsdSkelRoot.

    Args:
        joint (str):
            Some absolute joint path.
            e.g. "|group1|root_joint|foo|bar|some_joint".
        root (str):
            The absolute path to the first joint in a joint hierarchy.
            e.g. "|group1|root_joint"

    Returns:
        str: The UsdSkelRoot-relative path to a Maya joint. This path
             is not meant to be a valid Maya DAG path but a path that can later be
             converted to a USD-joint path.
             e.g. "root_joint|foo|bar|some_joint".

    """
    root_node_name = cmds.ls(root, shortNames=True)[0]

    if joint == root:
        return root_node_name

    return root_node_name + "|" + joint[len(root) + 1 :]


def convert_maya_path_to_usd(path):
    """Change an absolute Maya node path into a USD SdfPath-style path.

    Args:
        path (str): Some path like "|group1|pSphere1|pSphereShape1".

    Returns:
        str: The converted USD path. e.g. "/group1/pSphere1/pSphereShape1".

    """
    path = path.replace("|", "/")

    return path


def get_all_joints(joint):
    """Get the full joint hierarchy that `joint` is a part of.

    Note:
        This function will include the top-level root joint that `joint` is
        usually a part of.

    Args:
        joint (str): The path to a Maya node.

    Returns:
        list[str]: Every joint in the entire joint hierarchy. This list
            also includes the root joint node.

    """

    def _is_joint(node):
        return cmds.nodeType(node) == "joint"

    root = cmds.ls(_get_root(joint, predicate=_is_joint), long=True)[0]
    joints = cmds.listRelatives(root, allDescendents=True, fullPath=True) or []

    root_node_name = cmds.ls(root, shortNames=True)[0]

    # The UsdSkel documentation requires that joints are written parents
    # first, then children. This is easy to do in Maya - just sort the
    # joints and then it will be in the correct order.
    #
    topology = sorted(joints)

    usd_topology = _convert_to_usd_joint_syntax(
        [root_node_name] + [_get_relative_joint_path(joint, root) for joint in topology]
    )

    return (usd_topology, [root] + topology)
