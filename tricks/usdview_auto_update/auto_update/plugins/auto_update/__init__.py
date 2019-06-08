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
    @staticmethod
    def _exec(viewer):
        viewer.qMainWindow.installEventFilter(viewer.qMainWindow)
        viewer.qMainWindow.eventFilter = functools.partial(event_filter, viewer)

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


def event_filter(viewer, obj, event):
    value = obj.__class__.eventFilter(
        obj, obj, event
    )  # Call the base-class `eventFilter`

    if viewer.stage is None:
        # This happens when the usdview GUI is in the process of being closed.
        # Just ignore it.
        #
        LOGGER.debug(
            "No stage was found so `event_filter` cannot update the user's Stage."
        )
        return value

    layers = viewer.stage.GetUsedLayers()
    reloaded = [layer.Reload() for layer in layers if not layer.anonymous]

    if not any(reloaded):
        return value

    print("BL_reloadLayers: Reloaded at", datetime.datetime.now())
    for layer, reloaded in zip(layers, reloaded):
        if reloaded:
            print("\t", layer.identifier)

    return True


Tf.Type.Define(AutoUpdateContainer)
