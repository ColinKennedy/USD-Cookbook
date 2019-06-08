#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import datetime
import functools
import logging

from pxr import Tf
from pxr.Usdviewq import plugin


LOGGER = logging.getLogger(__name__)
WAS_INITIALIZED = False
IS_ENABLED = False


class AutoUpdateContainer(plugin.PluginContainer):
    def _toggle_reload_and_setup_reload(self, viewer):
        global WAS_INITIALIZED
        global IS_ENABLED

        from PySide import QtCore

        IS_ENABLED = not IS_ENABLED

        if WAS_INITIALIZED:
            LOGGER.debug('The timer was already created. Nothing left to do here.')
            return

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
        LOGGER.debug('Layer auto-reload is disabled.')
        return

    layers = viewer.stage.GetUsedLayers()
    reloaded = [layer.Reload() for layer in layers if not layer.anonymous]

    if not any(reloaded):
        return

    print("Layers reloaded at", datetime.datetime.now())
    for layer, reloaded in zip(layers, reloaded):
        if reloaded:
            print("    ", layer.identifier)


Tf.Type.Define(AutoUpdateContainer)
