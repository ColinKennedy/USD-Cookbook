#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The module which registers the "copy camera" plugin to usdview."""

import functools

from PySide import QtCore
from pxr import Sdf, Tf, UsdGeom
from pxr.Usdviewq import plugin

from . import camera_manager, prim_copier


_DEFAULT_CAMERA_PATH = "/current_camera1"
_DISPLAY_NAME = "Copy The Current Camera"


class CopyCameraContainer(plugin.PluginContainer):
    """The class which registers the "copy camera" plugin to usdview."""

    def registerPlugins(self, registry, _):
        """Add this Camera Copy to usdview on-startup.

        Args:
            registry (`pxr.Usdviewq.plugin.PluginRegistry`):
                The USD-provided object that this plugin will be added to.

        """
        self._copy_command = registry.registerCommandPlugin(
            "CopyCameraContainer",
            _DISPLAY_NAME,
            _show_copy_window,
        )

    def configureView(self, _, builder):
        """Add a menu command to `builder`.

        Args:
            builder (:class:`pxr.Usdviewq.plugin.PluginUIBuilder`):
                The object responsible for adding menus to usdview.

        """
        menu = builder.findOrCreateMenu(_DISPLAY_NAME)
        menu.addItem(self._copy_command)


def _create_camera(viewer, path):
    """Make a new camera in the user's current USD stage, using the current viewer camera.

    Args:
        viewer (:class:`pxr.Usdviewq.usdviewApi.UsdviewApi`):
            The usdview controller. If has references to both the
            current stage and the user's current view camera.
        path (str or :usd:`SdfPath`):
            The Prim path to create a camera at.

    """
    api = UsdGeom.Camera.Define(viewer.stage, path)
    api.SetFromCamera(viewer.currentGfCamera)


def _show_copy_window(viewer):
    """Create a window so the user can write add a new camera.

    Args:
        viewer (:class:`pxr.Usdviewq.usdviewApi.UsdviewApi`):
            The usdview controller. If has references to both the
            current stage and the user's current view camera.

    """
    window = prim_copier.PathWriter(
        {prim.GetPath() for prim in viewer.stage.TraverseAll()},
        parent=viewer.qMainWindow,
    )
    window.setWindowFlags(QtCore.Qt.Window)
    window.setWindowTitle("Camera Copier")
    window.setObjectName("camera_copier")

    window.setStyleSheet(
        """\
        QLineEdit[state="error"] {border-radius: 3px; border: 4px solid red;}
        QLineEdit[state="warning"] {border-radius: 3px; border: 4px solid gold;}
        QLineEdit[state="acceptable"] {border-radius: 3px; border: 4px solid green;}
        """
    )

    window.enter_pressed.connect(functools.partial(_create_camera, viewer))
    window.enter_pressed.connect(functools.partial(_repopulate_prim_paths, viewer, window))

    window.set_text(_DEFAULT_CAMERA_PATH)
    camera_manager.set_unique_camera_path(window, viewer.stage)

    window.show()


# TODO : Make this work off of Tf notices
def _repopulate_prim_paths(viewer, widget, _):
    """Update `widget` with a new list of Prim paths to be aware of.

    This function should run any time a new Prim has been added to the stage.

    Args:
        viewer (:class:`pxr.Usdviewq.usdviewApi.UsdviewApi`):
            The usdview controller. If has references to both the
            current stage and the user's current view camera.
        widget (:class:`prim_copier.PathWriter`):


    """
    paths = {prim.GetPath() for prim in viewer.stage.TraverseAll()}
    widget.populate(paths)

    camera_manager.set_unique_camera_path(widget, viewer.stage)


# XXX : Important line. usdview needs this to "see" our container, on-boot
Tf.Type.Define(CopyCameraContainer)
