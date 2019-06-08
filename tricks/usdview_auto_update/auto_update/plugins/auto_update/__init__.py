#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import datetime
import functools
import logging
import sys

from pxr import Tf
from pxr.Usdviewq import plugin

LOGGER = logging.getLogger(__name__)
_HANDLER = logging.StreamHandler(sys.stdout)
_FORMATTER = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(module)s: %(message)s", datefmt="%m/%d/%Y %H:%M:%S"
)
_HANDLER.setFormatter(_FORMATTER)
LOGGER.addHandler(_HANDLER)
LOGGER.setLevel(logging.INFO)

WAS_INITIALIZED = False
IS_ENABLED = False


class AutoUpdateContainer(plugin.PluginContainer):
    def _toggle_reload_and_setup_reload(self, viewer):
        global WAS_INITIALIZED
        global IS_ENABLED

        from PySide import QtCore

        IS_ENABLED = not IS_ENABLED

        if WAS_INITIALIZED:
            LOGGER.debug("The timer was already created. Nothing left to do here.")
            return

        # Add `timer` to this instance to keep it from going out of scope
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(functools.partial(reload_layers, viewer))
        self.timer.start(1000)

        WAS_INITIALIZED = True

    def registerPlugins(self, registry, _):
        self._toggle_auto_reload_command = registry.registerCommandPlugin(
            "AutoUpdateContainer.printMessage",
            "Toggle Auto-Reload USD Stage",
            self._toggle_reload_and_setup_reload,
        )

    def configureView(self, registry, builder):
        menu = builder.findOrCreateMenu("Reloader")
        menu.addItem(self._toggle_auto_reload_command)


def reload_layers(viewer):
    if not IS_ENABLED:
        LOGGER.debug("Layer auto-reload is disabled.")
        return

    layers = viewer.stage.GetUsedLayers()
    reloaded = [layer.Reload() for layer in layers if not layer.anonymous]

    if not any(reloaded):
        return

    LOGGER.info('Layers reloaded at "%s"', datetime.datetime.now())
    for layer, reloaded in zip(layers, reloaded):
        if reloaded:
            LOGGER.info('    "%s"', layer.identifier)


Tf.Type.Define(AutoUpdateContainer)
