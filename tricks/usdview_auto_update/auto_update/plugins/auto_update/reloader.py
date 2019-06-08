#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import os
import datetime
import functools

try:
    from PySide2 import QtCore
except ImportError:
    from PySide import QtCore


_INITITALIZED_STAGES = []


def _make_timer(viewer, interval, function):
    function(viewer)

    timer = QtCore.QTimer()
    timer.singleShot(interval, functools.partial(_make_timer, viewer, interval, function))


def reload_layers(viewer):
    layers = viewer.stage.GetUsedLayers()
    reloaded = [layer.Reload() for layer in layers if not layer.anonymous]
    if not any(reloaded):
        return

    print("reload_layers: Reloaded at " + datetime.datetime.now().strftime("%X"))

    for (layer, reloaded) in zip(layers, reloaded):
        if reloaded:
            print("    " + layer.identifier)


def enable_auto_reload(viewer):
    '''Run the main execution of the current script.

    Args:
        viewer (`pxr.Usdviewq.usdviewApi.UsdviewApi`):
            The active usdview session object.

    '''
    print('Sourcing "usdview_auto_reload.py"')

    if viewer.stage in _INITITALIZED_STAGES:
        print('Stage "{viewer.stage}" is already registered.'.format(viewer=viewer))
        return

    print('Stage "{viewer.stage}" will now auto-load'.format(viewer=viewer))

    timer = QtCore.QTimer()
    timer.singleShot(1000, functools.partial(_make_timer, viewer, 1000, reload_layers))

    _INITITALIZED_STAGES.append(viewer.stage)
