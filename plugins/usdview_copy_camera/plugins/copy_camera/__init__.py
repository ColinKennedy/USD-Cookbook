#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The module which registers the "copy camera" plugin to usdview."""

# TODO : Make sure this works even if the user changes stage

import contextlib
import functools

from PySide import QtCore, QtGui
from pxr import Sdf, Tf, Usd, UsdGeom
from pxr.Usdviewq import plugin

from . import camera_manager, path_machine


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
            "CopyCameraContainer", _DISPLAY_NAME, _show_copy_window,
        )

    def configureView(self, _, builder):
        """Add a menu command to `builder`.

        Args:
            builder (:class:`pxr.Usdviewq.plugin.PluginUIBuilder`):
                The object responsible for adding menus to usdview.

        """
        menu = builder.findOrCreateMenu(_DISPLAY_NAME)
        menu.addItem(self._copy_command)


def _add_button_actions(window, viewer):
    """Wire the window's buttons up to usdview.

    Args:
        window (:class:`.path_machine.PathWriter`):
            The Qt window which, by itself, does nothing but this
            function will improve and make "usdview-friendly".
        viewer (:class:`pxr.Usdviewq.usdviewApi.UsdviewApi`):
            The usdview controller. If has references to both the
            current stage and the user's current view camera.

    """
    # 1. Set up the main button
    window.enter_pressed.connect(functools.partial(_create_camera, viewer))
    window.enter_pressed.connect(
        functools.partial(_repopulate_prim_paths, viewer, window)
    )

    # 2. Set up the side button menu
    menu = QtGui.QMenu()
    force = menu.addAction("Force-Add")
    force.triggered.connect(functools.partial(_force_add, window))
    session = menu.addAction("Add As A Session Override")

    session.triggered.connect(
        functools.partial(_create_camera_from_widget, window, viewer, as_session=True)
    )
    session.triggered.connect(functools.partial(_repopulate_prim_paths, viewer, window))

    window.set_side_menu(menu)
    window._enter_button._side_button.menu().actions()


def _create_camera_from_widget(widget, viewer, as_session=False):
    """A variant of `_create_camera` that queries the widget's current text.

    Args:
        widget (:class:`PySide.QtGui.QLineEdit`):
            Some user-defined Prim path to create a camera at.
        viewer (:class:`pxr.Usdviewq.usdviewApi.UsdviewApi`):
            The usdview controller. If has references to both the
            current stage and the user's current view camera.
        as_session (bool, optional):
            If False, add the camera to the stage's current edit target.
            If True, add it to the stage's session Layer instead.
            Default is False.
    """
    _create_camera(viewer, widget.text(), as_session=as_session)


def _create_camera(viewer, path, as_session=False):
    """Make a new camera in the user's current USD stage, using the current viewer camera.

    Args:
        viewer (:class:`pxr.Usdviewq.usdviewApi.UsdviewApi`):
            The usdview controller. If has references to both the
            current stage and the user's current view camera.
        path (str or :usd:`SdfPath`):
            The Prim path to create a camera at.
        as_session (bool, optional):
            If False, add the camera to the stage's current edit target.
            If True, add it to the stage's session Layer instead.
            Default is False.

    """

    @contextlib.contextmanager
    def _null_context():
        # Do nothing
        try:
            yield
        finally:
            pass

    path = Sdf.Path(path)
    path = path.GetPrimPath()  # Remove any property information, if there is any.

    context = _null_context()

    if as_session:
        context = Usd.EditContext(viewer.stage, viewer.stage.GetSessionLayer())

    with context:
        api = UsdGeom.Camera.Define(viewer.stage, path)
        api.SetFromCamera(viewer.currentGfCamera)


def _force_add(widget):
    """Forcibly press the "enter" button, even if the widget's text is invalid.

    Args:
        widget (:class:`.path_machine.PathWriter`): The Prim path text to get / emit.

    """
    widget.enter_pressed.emit(widget.text())


def _show_copy_window(viewer):
    """Create a window so the user can write add a new camera.

    Args:
        viewer (:class:`pxr.Usdviewq.usdviewApi.UsdviewApi`):
            The usdview controller. If has references to both the
            current stage and the user's current view camera.

    """
    # 1. Add the basic GUI
    window = path_machine.PathWriter(
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

    # 2. Add button click actions
    _add_button_actions(window, viewer)

    # 3. Add a reasonable, default camera name path
    window.setText(_DEFAULT_CAMERA_PATH)
    camera_manager.set_unique_path(
        window, {prim.GetPath() for prim in viewer.stage.TraverseAll()},
    )

    window.show()


def _repopulate_prim_paths(viewer, widget, *_):
    """Update `widget` with a new list of Prim paths to be aware of.

    This function should run any time a new Prim has been added to the stage.

    Args:
        viewer (:class:`pxr.Usdviewq.usdviewApi.UsdviewApi`):
            The usdview controller. If has references to both the
            current stage and the user's current view camera.
        widget (:class:`path_machine.PathWriter`):
            A GUI which users can use to write a Prim path.

    """
    paths = {prim.GetPath() for prim in viewer.stage.TraverseAll()}
    widget.populate(paths)

    camera_manager.set_unique_path(
        widget, {prim.GetPath() for prim in viewer.stage.TraverseAll()},
    )


# XXX : Important line. usdview needs this to "see" our container, on-boot
Tf.Type.Define(CopyCameraContainer)
