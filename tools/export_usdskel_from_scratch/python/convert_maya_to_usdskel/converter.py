#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The main module that is responsible for writing a Maya scene as a USD skeleton.

Example:
    >>> from convert_maya_to_usdskel import converter
    >>> node = 'root_joint'
    >>> converter.write_rig_as_usdskel(
    ...     node,
    ...     "/SkeletonRoot",
    ...     "/SkeletonAnimation",
    ...     "/tmp/test_export",
    ... )

"""

import functools
import logging
import os

from maya import cmds
from pxr import Gf, Sdf, Usd, UsdGeom, UsdSkel, Vt

from . import animator, common, helper, mesher, skinner

LOGGER = logging.getLogger(__name__)


def _setup_animation_range_from_nodes(stage, nodes):
    """Set the start/end times for a USD stage using the keys of some Maya nodes.

    Args:
        stage (`pxr.Usd.Stage`):
            The composed stage that will be modified by this function.
        nodes (list[str]):
            Some Maya transform nodes (joint nodes, for example) that
            have some animation applied to them.

    Returns:
        tuple[float or int, float or int]:
            The lowest and highest keyframe of all nodes. If none of the
            nodes have any animation, this function will exit early.

    """
    times = animator.get_animation_range(nodes)

    start, end = times
    stage.SetStartTimeCode(start)
    stage.SetEndTimeCode(end)
    stage.SetMetadata(
        "comment",
        "This Layer's start/end time codes were found using the "
        "start/end animations of a list of Maya nodes.",
    )

    return (start, end)


def _setup_animation_range_from_times(stage, times):
    """Set the start/end times for a USD stage using a provided start/end time.

    Args:
        stage (`pxr.Usd.Stage`):
            The composed stage that will be modified by this function.
        times (tuple[float or int, float or int]):
            The start and end time that will be set onto `stage`.

    Returns:
        tuple[float or int, float or int]: Return the original start/end times.

    """
    start, end = times

    stage.SetStartTimeCode(start)
    stage.SetEndTimeCode(end)
    stage.SetMetadata(
        "comment",
        "This Layer's start/end time codes were set using an explicit start/end time.",
    )

    return (start, end)


def _setup_animation(
    animation, time_codes, joints, joints_transforms, topology, joint_count
):
    """Write joint animation to USD and bind the animation to a skeleton.

    Reference:
        https://graphics.pixar.com/usd/docs/api/_usd_skel__a_p_i__intro.html#UsdSkel_API_WritingSkels

    Args:
        animation (`pxr.UsdSkel.Animation`):
            The object that will get all of the animation data applied
            to it in this function.
        time_codes (iter[tuple[float or int]):
            The time-codes that will be used to calculate local joint transforms.
        joints (list[str]):
            The ordered-list of parent<->child joints that will be used
            to compute the local-space joint transformations. This
            parameter is the base of `topology`.
        joints_transforms (dict[float or int, list[`pxr.Gf.Matrix4d`]]):
            The world-space transforms of every joint in `joints`
            for-each time-code in `time_codes`. The length of each
            value in this parameter must match `joint_count`.
        topology (`pxr.UsdSkel.Topology`):
            A description of the joint hierarchy that was created using
            `joints` as its input.
        joint_count (int):
            The required transforms-per-time-code. This parameter is used
            to check that each world-space joint transform is correct
            before it is used to compute a local-space joint transform.

    """
    animation.GetPrim().SetMetadata(
        "comment",
        "local-space joint transformations that match the `joints` attribute.",
    )

    joints_attribute = animation.CreateJointsAttr(joints)
    joints_attribute.SetMetadata(
        "comment",
        "This list of joints contains every joint plus the original Maya root joint.",
    )

    for time_code in time_codes:
        joint_world_space_transforms = Vt.Matrix4dArray(joints_transforms[time_code])

        if len(joint_world_space_transforms) != joint_count:
            LOGGER.warning(
                'Found transforms "%s" don\'t match the number of joints',
                joint_world_space_transforms,
            )

            continue

        joint_local_space_transforms = UsdSkel.ComputeJointLocalTransforms(
            topology, joint_world_space_transforms
        )

        if joint_local_space_transforms:
            animation.SetTransforms(joint_local_space_transforms, time_code)
        else:
            LOGGER.warning(
                'World space transforms "%s" could not be computed as local transforms. Skipping.',
                joint_world_space_transforms,
            )


def _setup_cached_extents_hints(stage, root_path, meshes, times):
    """Add bounding box information to the a UsdSkelRoot Prim.

    Adding an extentsHint onto the root skeleton is an optional part of
    exporting a USD skeleton. But if USD has these values pre-cached,
    it can be used to cull out-of-frame meshes without computing their
    skeleton animation/skinning. This makes interactive viewports much
    faster.

    Note:
        If `root_path` doesn't point to an existing Prim, it will be created.

    Args:
        stage (`pxr.Usd.Stage`):
            The USD object that will be used to get/create the
            `root_path` Prim.
        root_path (str):
            The absolute USD namespace location to the UsdSkelRoot Prim
            that we will add an extents hint to.
        meshes (tuple[str]):
            The paths to each Maya mesh that must be written to-disk.
            e.g. ["|some|pSphere1|pSphereShape1"].
        times (list[float or int]):
            Each distinct time that this function will query and cache
            bounding box information for.

    """
    override = stage.GetPrimAtPath(root_path)

    if not override.IsValid():
        override = stage.OverridePrim(root_path)

    for time_code in times:
        bounding_box = [
            Gf.Vec3f(*point)
            for point in mesher.get_overall_bounding_box(meshes, time_code)
        ]
        UsdGeom.ModelAPI(override).SetExtentsHint(bounding_box, time_code)


def _setup_animation_connections(stage, root_path, animation_path):
    """Connect an existing SkeletonAnimation Prim to a Prim on a stage.

    If `root_path` doesn't point to an existing Prim, it will be created.

    Args:
        stage (`pxr.Usd.Stage`):
            The object that will be used to get or create an override
            Prim at `root_path`.
        root_path (str):
            The absolute path to the location of the UsdSkelRoot to
            override.
        animation_path (str):
            The relative or absolute path to the UsdSkeletonAnimation
            Prim which will be used to animate the skeleton in `root_path`.

    """
    # Tell the Sublayer'ed UsdSkelRoot to use the animation that this function creates
    override = stage.GetPrimAtPath(root_path)

    if not override.IsValid():
        override = stage.OverridePrim(root_path)

    binding = UsdSkel.BindingAPI.Apply(override)
    binding.CreateAnimationSourceRel().SetTargets([animation_path])


def _setup_bind_transforms(nodes, skeleton, time_code):
    """Create the world-space bind transforms for all every joint in a skeleton.

    Args:
        nodes (list[str]):
            Every Maya node, listed in "topology-order". This list must
            match the order of USD's `skel:joints` relationship.
        skeleton (`pxr.UsdSkel.Skeleton`):
            The skeleton that the created `skel:bindTransforms` Property
            will be added onto.
        time_code (float or int):
            The time which is used to sample the transform for each node
            in `nodes`.

    """
    transforms = animator.get_node_transforms_at_time(nodes, time_code, "world")
    attribute = skeleton.CreateBindTransformsAttr(transforms)
    attribute.SetMetadata(
        "comment",
        "This is an array of all world-space transforms for every "
        "joint in the skeleton. It defines the location of "
        'each joint at "bind-time".',
    )


def _setup_joints(joints, skeleton):
    """Add the given USD joints to a Skeleton.

    This function defines the `joints` USD Property onto `skeleton`.

    Args:
        joints (list[str]):
            The Maya joints, in "topology-order" that will be applied to
            `skeleton`. These paths must work with USD's SdfPath syntax.
            e.g. ["some_joint", "some_joint/some_child"].
        skeleton (`pxr.UsdSkel.Skeleton`):
            A USD node that `joints` will be added directly into.

    """
    attribute = skeleton.GetJointsAttr()
    attribute.Set(joints)
    attribute.SetMetadata(
        "comment",
        "These joint paths are generated automatically by converting "
        'the absolute paths of Maya joint nodes to "SdfPath-style" syntax. '
        'Note, these paths are relative (they don\'t contain a leading "/").',
    )


def _setup_meshes(meshes, skeleton, path):
    """Export `meshes` and then bind their USD Prims to a skeleton.

    Args:
        meshes (iter[str]):
            The paths to each Maya mesh that must be written to-disk.
            e.g. ["|some|pSphere1|pSphereShape1"].
        skeleton (`pxr.UsdSkel.Skeleton`):
            The USD Skeleton that the exported meshes will be paired with.
        path (str):
            The location on-disk where the USD meshes are stored. is
            Thpath is added as a reference into `skeleton`.

    Raises:
        RuntimeError: If `skeleton` has no ancestor UsdSkelRoot Prim.

    Returns:
        list[tuple[str, `pxr.UsdSkel.BindingAPI`]]:
            The Maya mesh which represents some USD mesh and the binding
            schema that is used to bind that mesh to the skeleton. We
            return these two values as pairs so that they don't have any
            chance of getting mixed up when other functions use them.

    """
    def _get_default_prim_path(path):
        """`pxr.Sdf.Path`: Get the path of the defaultPrim of some USD file."""
        stage = Usd.Stage.Open(path)
        prim = stage.GetDefaultPrim()

        return prim.GetPath()

    def _add_mesh_group_reference(stage, path, root):
        """Add the meshes in some USD `path` file onto the given `stage` starting at `root`.

        Important:
            `default_added_to_root` must exist on stage before this function is called.

        """
        # Example:
        #     default = Sdf.Path("/group1")
        #     root = Sdf.Path("/Something/SkeletonRoot")
        #     default_added_to_root = Sdf.Path("/Something/SkeletonRoot/group1")
        #
        default = _get_default_prim_path(path)
        default_added_to_root = root.GetPath().AppendChild(
            str(default.MakeRelativePath("/"))
        )
        stage.GetPrimAtPath(default_added_to_root).GetReferences().AddReference(
            os.path.relpath(path, os.path.dirname(stage.GetRootLayer().identifier))
        )

    def _create_mesh_bindings(paths):
        bindings = []

        comment = "The values in this attribute were sorted by elementSize."

        for usd_path in paths:
            # `usd_path` is referenced under the UsdSkelRoot so we need to add
            # its name to the path
            #
            override = stage.OverridePrim(usd_path)
            override.SetMetadata("comment", comment)
            binding = UsdSkel.BindingAPI.Apply(override)
            binding.CreateSkeletonRel().SetTargets([skeleton.GetPath()])
            bindings.append(binding)

        return bindings

    def _get_expected_mesh_paths(meshes, new_root):
        """Make each mesh path relative to the given `new_root` UsdSkelRoot Prim path."""
        relative_paths = [
            Sdf.Path(helper.convert_maya_path_to_usd(mesh).lstrip("/"))
            for mesh in meshes
        ]

        return [path_.MakeAbsolutePath(new_root) for path_ in relative_paths]

    # Note: This is a hacky trick but works well. We include
    # `exportSkin="auto"` to make USD export export joint influences
    # with our meshes. It also will try to link skinning to the mesh but
    # we will override those connections later.
    #
    # Basically, we use `cmds.usdExport` just for the joint influence
    # information and blow away the rest of the data it outputs in
    # other, stronger layers.
    #
    # Reference: https://graphics.pixar.com/usd/docs/Maya-USD-Plugins.html
    #
    cmds.usdExport(meshes, file=path, exportSkin="auto")

    root = UsdSkel.Root.Find(skeleton)

    if not root:
        raise RuntimeError(
            'Skeleton "{skeleton}" has no UsdSkelRoot.'.format(
                skeleton=skeleton.GetPath()
            )
        )

    root = root.GetPrim()
    stage = root.GetStage()
    bindings = _create_mesh_bindings(
        _get_expected_mesh_paths(meshes, root.GetPath())
    )
    # Note: We add the mesh into an explicit `over` Prim instead of
    # adding it directly onto `root` as a reference. This is so that we
    # can have better control over what kind of meshes are loaded. e.g.
    # In the future, we can switch this part to use a variant set to
    # load different mesh LODs, for example.
    #
    _add_mesh_group_reference(stage, path, root)

    return list(zip(meshes, bindings))


def _setup_root_transforms(skeleton, transforms):
    """Add transformations for the first joint in a Skeleton's hierarchy.

    USD authors joint animations in "joint local space". To physically
    position a skeleton in-space, we need to also add transforms onto
    the root transform of the skeleton. This function basically adds
    transforms that will become our "skeleton space transformations".

    Args:
        skeleton (`pxr.UsdSkel.Skeleton`):
            The Skeleton in some USD stage that will have `transforms`
            applied to it.
        transforms (iter[float or int, `pxr.Gf.Matrix4d`]):
            The time-code / transform pairs that describe the root
            transform.

    """
    attribute = skeleton.MakeMatrixXform()

    for time_code, transform in transforms:
        attribute.Set(transform, time_code)


def _setup_rest_transforms(nodes, skeleton, time_code):
    """Describe the position for every joint in a Skeleton when it is not animated.

    The UsdSkel documentation states that animation can be authored
    sparsely. If a joint has no transform information, it falls back to
    the transform that's authored on its restTransforms Property.

    That means that every transform in restTransform must be in
    local-space, because joint animations are also in local-space (they
    have to match in order to be a valid fallback value).

    Important:
        The order of `nodes` has to match the order of the joints
        Property that is authored on `skeleton`. (You can author the
        Property before or have running this function, as long as it's
        the same).

    Args:
        nodes (list[str]):
            The Maya joints that will be used to get local-space rest
            transforms.
        skeleton (`pxr.UsdSkel.Skeleton`):
            The USD skeleton that the new restTransforms Property will
            be applied onto.
        time_code (float or int):
            The time which is used to sample the transform for each node
            in `nodes`.

    """
    transforms = animator.get_node_transforms_at_time(nodes, time_code, "local")

    attribute = skeleton.CreateRestTransformsAttr(transforms)
    attribute.SetMetadata(
        "comment", "Every value in this attribute is a local-space transform."
    )


def _setup_skeleton(root, path):
    """Create a skeleton and place it under some skeleton root.

    Args:
        root (`pxr.Usd.SkelRoot`):
            The start of a USD skeleton / mesh definition.
        path (str):
            The path in USD namespace where the created skeleton will be
            written to.

    Returns:
        `pxr.Usd.Skeleton`: The created skeleton.

    """
    if not path.startswith(str(root.GetPath())):
        raise ValueError('Path "{path}" must be a child of "{root}".'.format(path=path, root=root))

    skeleton = UsdSkel.Skeleton.Define(root.GetStage(), path)

    return skeleton


def _validate_topology(paths):
    """Check if the order of `paths` will create a correct UsdSkelSkeleton.

    Args:
        paths (list[str]):
            The USD joint paths to check.
            e.g. ["some_joint", "some_joint/another_joint", ...].

    Raises:
        RuntimeError: If `paths` is in an incorrect order.

    Returns:
        `pxr.UsdSkel.Topology`:
            The topology description that was used to validate `paths`.

    """
    topology = UsdSkel.Topology(paths)
    valid, reason = topology.Validate()

    if not valid:
        raise RuntimeError(
            'Topology failed because of reason "{reason}".'.format(reason=reason)
        )

    return topology


def write_rig_as_usdskel(node, root_path, animation_path, folder, times=None):
    """Write an animated USD Skeleton to-disk.

    If no time range is given then a start/end range is found by looking
    at the earliest start and the latest end animation keys from the
    given nodes.

    Args:
        node (str):
            The path to a joint on the Maya skeleton which will be the
            basis of the USD Skeleton. Any joint is fine but the root
            joint of the skeleton is preferred.
        root_path (str):
            The absolute USD namespace path that will be used to start
            the Skeleton definition. e.g. "/SkeletonRoot".
        animation_path (str):
            The absolute USD namespace path that will be used store
            the recorded Skeleton animation. Usually, this path is
            located outside of the `root_path` SkeletonRoot. e.g.
            "/SkeletonAnimation".
        folder (str):
            The directory on-disk where all of the different USD layers
            will be written.
        times (tuple[float or int, float or int]):
            The start and end frames of animation to record. If no
            start/end is given then the times will be automatically
            found using animation on the Skeleton.

    """
    if not os.path.isdir(folder):
        os.makedirs(folder)

    skeleton_stage = Usd.Stage.CreateNew(os.path.join(folder, "skeleton.usda"))

    root = UsdSkel.Root.Define(skeleton_stage, root_path)
    root.GetPrim().SetMetadata(
        "comment",
        "This is the start of any skeleton definition. Skeleton USD objects "
        "and mesh data go inside of here.",
    )
    skeleton = _setup_skeleton(root.GetPrim(), root_path + "/Skeleton")
    joints, nodes = helper.get_all_joints(node)

    topology = _validate_topology(joints)

    # Note: This file contains the skeleton, meshes, and animation
    main_stage = Usd.Stage.CreateNew(os.path.join(folder, "main.usda"))
    main_stage.SetMetadata(
        "comment",
        "This stage describes some animation and combines it with the "
        "meshes and the skeleton that will drive them. The meshes happen to be "
        "nested underneath the SkelRoot definition already but this is not actually "
        "required (as long as they get merged back in, later).",
    )

    if times:
        start, end = _setup_animation_range_from_times(main_stage, times)
    else:
        start, end = _setup_animation_range_from_nodes(main_stage, nodes)

    times = list(common.frange(start, end))

    _setup_joints(joints, skeleton)
    _setup_bind_transforms(nodes, skeleton, start)
    # XXX : Normally, you would want to add transformations onto the skeleton here.
    # but because this script __includes the root joint in `skel:joints`, that
    # root transformation is actually already being applied to the skeleton.
    #
    # That means that if we were to uncomment the line below, the skeleton's
    # will be double-transformed in world-space.
    #
    # _setup_root_transforms(skeleton, root_transforms)
    _setup_rest_transforms(nodes, skeleton, start)
    joint_world_space_transforms = animator.get_joint_world_space_transforms(
        nodes, times
    )

    animation_stage = Usd.Stage.CreateNew(os.path.join(folder, "animation.usda"))
    animation_stage.SetMetadata(
        "comment",
        "This Layer only describes an animation for our skeleton. "
        "It should not try to form any connections back to the skeleton "
        "that it's based from. (To keep things as decoupled as possible).",
    )

    animation = UsdSkel.Animation.Define(animation_stage, animation_path)
    _setup_animation(
        animation,
        times,
        joints,
        joint_world_space_transforms,
        topology,
        len(joints),
    )
    _setup_animation_connections(
        main_stage, root.GetPrim().GetPath(), animation.GetPrim().GetPath()
    )

    animation_stage.Save()

    meshes = set(mesh for joint in nodes for mesh in mesher.get_connected_meshes(joint))
    data = _setup_meshes(
        meshes, skeleton.GetPrim(), os.path.join(folder, "meshes.usda")
    )
    _setup_cached_extents_hints(main_stage, root.GetPrim().GetPath(), meshes, times)
    skinner.setup_skinning(data, nodes)

    skeleton_stage.GetRootLayer().Save()

    for stage_ in (skeleton_stage, animation_stage):
        main_stage.GetRootLayer().subLayerPaths.append(
            os.path.relpath(stage_.GetRootLayer().identifier, folder)
        )

    main_stage.Save()
