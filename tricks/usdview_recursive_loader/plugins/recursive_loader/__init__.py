#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A usdview plugin that can auto-reload the stage whenever there are layer changes."""

# IMPORT FUTURE LIBRARIES
from __future__ import print_function

# IMPORT STANDARD LIBRARIES
import datetime
import functools
import logging
import sys

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Tf
from pxr.Usdviewq import plugin

LOGGER = logging.getLogger("recursive_loader")
_HANDLER = logging.StreamHandler(sys.stdout)
_FORMATTER = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(module)s: %(message)s", datefmt="%m/%d/%Y %H:%M:%S"
)
_HANDLER.setFormatter(_FORMATTER)
LOGGER.addHandler(_HANDLER)
LOGGER.setLevel(logging.INFO)

WAS_INITIALIZED = False
IS_ENABLED = False


class RecursiveLoaderContainer(plugin.PluginContainer):
    """The main registry class that initializes and runs the Auto-Reloader plugin."""

    def _toggle_reload_and_setup_reload(self, viewer):
        """Create the Auto-Reloader and set it to enabled.

        If the Auto-Reloader already exists then disable it.

        Args:
            viewer (`pxr.Usdviewq.usdviewApi.UsdviewApi`):
                The USD API object that is used to communicate with usdview.

        """
        global WAS_INITIALIZED
        global IS_ENABLED

        try:
            from PySide2 import QtCore
        except ImportError:
            from PySide import QtCore

        IS_ENABLED = not IS_ENABLED

        if WAS_INITIALIZED:
            LOGGER.debug("The timer was already created. Nothing left to do here.")
            return

        # Add `timer` to this instance to keep it from going out of scope
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(functools.partial(reload_layers, viewer))
        self.timer.start(500)

        WAS_INITIALIZED = True

    def registerPlugins(self, registry, _):
        """Add this Auto-Reloader plugin to usdview on-startup.

        Args:
            registry (`pxr.Usdviewq.plugin.PluginRegistry`):
                The USD-provided object that this plugin will be added to.

        """
        self._toggle_auto_reload_command = registry.registerCommandPlugin(
            "RecursiveLoaderContainer.printMessage",
            "Toggle Auto-Reload USD Stage",
            self._toggle_reload_and_setup_reload,
        )

    def configureView(self, _, builder):
        """Add a new menu item for the Auto-Reload function."""
        menu = builder.findOrCreateMenu("Reloader")
        menu.addItem(self._toggle_auto_reload_command)


Tf.Type.Define(RecursiveLoaderContainer)
