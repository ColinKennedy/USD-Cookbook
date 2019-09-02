#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A usdview plugin that replaces the "Load" and "Unload" buttons in usdview."""

# IMPORT STANDARD LIBRARIES
import functools
import logging
import sys

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Sdf, Tf, Usd
from pxr.Usdviewq import plugin

LOGGER = logging.getLogger("root_loader")
_HANDLER = logging.StreamHandler(sys.stdout)
_FORMATTER = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(module)s: %(message)s", datefmt="%m/%d/%Y %H:%M:%S"
)
_HANDLER.setFormatter(_FORMATTER)
LOGGER.addHandler(_HANDLER)
LOGGER.setLevel(logging.INFO)


class RootLoaderContainer(plugin.PluginContainer):
    """The main registry class that initializes and runs the Root-Loader plugin."""

    def registerPlugins(self, registry, _):
        """Add this Root-Loader plugin to usdview on-startup.

        Args:
            registry (`pxr.Usdviewq.plugin.PluginRegistry`):
                The USD-provided object that this plugin will be added to.

        """
        self._toggle_root_load_command = registry.registerCommandPlugin(
            "RootLoaderContainer.Load",
            "Root Load",
            functools.partial(load_gui, load=True),
        )
        self._toggle_root_unload_command = registry.registerCommandPlugin(
            "RootLoaderContainer.Unload",
            "Root Unload",
            functools.partial(load_gui, load=False),
        )

    def configureView(self, _, builder):
        """Add a new menu item for the Root-Loader function."""
        menu = builder.findOrCreateMenu("Root Loader")
        menu.addItem(self._toggle_root_load_command)
        menu.addItem(self._toggle_root_unload_command)


def _load(paths, stage, load):
    """Load or unload the given Prim paths.

    Args:
        paths (set[`pxr.Sdf.Path`]): The paths that will be loaded or unloaded.
        stage (`pxr.Usd.Stage`): The user's current stage that contains `paths` as Prims.
        load (bool): A value that controls if selected Prims are loaded or unloaded.

    """
    for root in Sdf.Path.RemoveDescendentPaths(paths):
        root = stage.GetPrimAtPath(root)

        if load:
            root.Load()
        else:
            root.Unload()


def load_gui(viewer, load):
    """Load or Unload the user's selected Prims.

    Args:
        viewer (`pxr.Usdviewq.usdviewApi.UsdviewApi`): usdview's current state.
        load (bool): A value that controls if selected Prims are loaded or unloaded.

    """
    _load(set(viewer.dataModel.selection.getPrimPaths()), viewer.stage, load)


Tf.Type.Define(RootLoaderContainer)
