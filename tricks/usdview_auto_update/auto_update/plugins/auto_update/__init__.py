#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import datetime
import functools
import logging

from pxr import Tf
from pxr.Usdviewq import plugin


LOGGER = logging.getLogger(__name__)


class AutoUpdateContainer(plugin.PluginContainer):
    def _exec(self, viewer):
        from PySide import QtCore

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(functools.partial(reload_layers, viewer))
        self.timer.start(1000)

    def registerPlugins(self, registry, _):
        from . import reloader

        self._enable_auto_reload = registry.registerCommandPlugin(
            "AutoUpdateContainer.printMessage",
            "Enable Auto-Reload USD Stage",
            self._exec,
        )

    def configureView(self, registry, builder):
        menu = builder.findOrCreateMenu("Reloader")
        menu.addItem(self._enable_auto_reload)


def reload_layers(viewer):
    layers = viewer.stage.GetUsedLayers()
    reloaded = [layer.Reload() for layer in layers if not layer.anonymous]

    if not any(reloaded):
        return

    print("Layers reloaded at", datetime.datetime.now())
    for layer, reloaded in zip(layers, reloaded):
        if reloaded:
            print("    ", layer.identifier)


Tf.Type.Define(AutoUpdateContainer)
