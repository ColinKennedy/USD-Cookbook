#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import collections
import datetime

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Tf, Usd

_INITIALIZED_STAGE = collections.defaultdict(set)


def _is_initialized(stage):
    return stage in _INITIALIZED_STAGE


def enable_auto_reload(viewer):
    if _is_initialized(viewer.stage):
        print('Stage "{viewer.stage}" is already registered.'.format(viewer=viewer))
        return

    print('Stage "{viewer.stage}" will now auto-load'.format(viewer=viewer))

    listener = Tf.Notice.Register(
        Usd.Notice.ObjectsChanged, reload_layers, viewer.stage
    )
    _INITIALIZED_STAGE[viewer.stage].add(listener)


def reload_layers(notice, _):
    layers = notice.GetStage().GetUsedLayers()
    reloaded = [layer.Reload() for layer in layers if not layer.anonymous]
    if not any(reloaded):
        return

    print("reload_layers: Reloaded at " + datetime.datetime.now().strftime("%X"))

    for (layer, reloaded) in zip(layers, reloaded):
        if reloaded:
            print("    " + layer.identifier)
