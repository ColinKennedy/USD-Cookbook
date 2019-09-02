#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A module that skins meshes to their linked skeleton(s)."""

# IMPORT STANDARD LIBRARIES
import functools

# IMPORT THIRD-PARTY LIBRARIES
from maya import cmds
from pxr import Gf, UsdSkel, Vt


def _get_skin_cluster(meshes):
    clusters = set()

    for mesh in meshes:
        for history_node in cmds.listHistory(mesh, allConnections=True):
            if cmds.nodeType(history_node) == "skinCluster":
                clusters.add(history_node)

        if len(clusters) > 1:
            raise NotImplementedError(
                "This function doesn't support multiple skin clusters yet"
            )

    try:
        return next(iter(clusters))
    except StopIteration:
        return None


def _get_vertices(mesh):
    return [
        mesh + ".vtx[{}]".format(index)
        for index in range(cmds.polyEvaluate(mesh, vertex=True))
    ]


def _get_weighted_joints(vertex, cluster, influences):
    joints = []

    for joint in influences:
        if cmds.skinPercent(cluster, vertex, transform=joint, q=True):
            joints.append(joint)

    return joints


def _calculate_influences(
    mesh, cluster, binding_joints, maximum_influences, weights_getter
):
    indices = []
    weights = []

    for vertex in _get_vertices(mesh):
        vertex_influence_joints = weights_getter(vertex, cluster)
        influences = len(vertex_influence_joints)

        if influences != maximum_influences:
            raise RuntimeError(
                'Vertex "{vertex}" has "{influences}". It needs to have "{maximum_influences}" influences.'.format(
                    vertex=vertex,
                    influences=influences,
                    maximum_influences=maximum_influences,
                )
            )

        for joint in vertex_influence_joints:
            indices.append(binding_joints.index(joint))

            weights.append(
                cmds.skinPercent(
                    cluster, vertex, transform=joint, normalize=True, q=True
                )
            )

    return indices, weights


def _write_influence_data(
    binding, mesh, cluster, binding_joints, maximum_influences, weights_getter
):
    matrix = cmds.xform(mesh, matrix=True, worldSpace=True, q=True)
    binding.CreateGeomBindTransformAttr().Set(Gf.Matrix4d(*matrix))

    indices, weights = _calculate_influences(
        mesh, cluster, binding_joints, maximum_influences, weights_getter
    )
    indices = Vt.IntArray(indices)
    weights = Vt.FloatArray(weights)

    # Reference: https://graphics.pixar.com/usd/docs/api/_usd_skel__schemas.html#UsdSkel_BindingAPI_StoringInfluences
    # Keep weights sorted and normalized for best performance
    #
    UsdSkel.NormalizeWeights(weights, len(binding_joints))
    UsdSkel.SortInfluences(indices, weights, maximum_influences)

    indices_attribute = binding.CreateJointIndicesPrimvar(
        constant=False, elementSize=maximum_influences
    )
    indices_attribute.Set(indices)

    weights_attribute = binding.CreateJointWeightsPrimvar(
        constant=False, elementSize=maximum_influences
    )
    weights_attribute.Set(weights)


def setup_skinning(data, joints):
    """Apply skeleton skinning to some Maya meshes that are exported to USD.

    Args:
        data (list[tuple[str, `pxr.Usd.BindingAPI`]]):
            The Maya node the represents a mesh that needs to be skinned
            and its binding which points back to the skeleton that the
            mesh will be bound to.
        joints (list[str]):
            The absolute paths to a Maya joint nodes.
            These nodes must be listed in USD topology-order (their
            indices matter).

    Raises:
        RuntimeError:
            If the influences of a joint in the found skin cluster
            doesn't match the total influences for the joint. Or if no
            skin cluster for a mesh could be found.

    """
    meshes, _ = zip(*data)
    cluster = _get_skin_cluster(meshes)

    if not cluster:
        raise RuntimeError(
            'No skin cluster could be found from data "{data}".'.format(data=data)
        )

    all_influence_joints = cmds.skinCluster(cluster, query=True, weightedInfluence=True)
    all_influence_joints = [
        cmds.ls(joint, long=True)[0] for joint in all_influence_joints
    ]
    _get_weighted_joints_cached = functools.partial(
        _get_weighted_joints, influences=all_influence_joints
    )

    maximum_influences = min(cmds.getAttr(cluster + ".maxInfluences"), len(joints))

    for mesh, binding in data:
        _write_influence_data(
            binding,
            mesh,
            cluster,
            joints,
            maximum_influences,
            _get_weighted_joints_cached,
        )
