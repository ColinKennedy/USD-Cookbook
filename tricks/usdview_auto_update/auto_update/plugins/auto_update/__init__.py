#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Tf
from pxr.Usdviewq import plugin


class AutoUpdateContainer(plugin.PluginContainer):
    def registerPlugins(self, registry, _):
        from . import reloader

        self._enable_auto_reload = registry.registerCommandPlugin(
            "AutoUpdateContainer.printMessage",
            "Enable Auto-Reload USD Stage",
            reloader.enable_auto_reload,
        )

    def configureView(self, registry, builder):
        menu = builder.findOrCreateMenu("Reloader")
        menu.addItem(self._enable_auto_reload)


Tf.Type.Define(AutoUpdateContainer)
