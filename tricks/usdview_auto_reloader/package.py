# -*- coding: utf-8 -*-

name = 'auto_reloader'

version = '1.0.0'


def commands():
    import os

    env.PXR_PLUGINPATH_NAME.append(os.path.join('{root}', 'plugins', 'auto_reloader'))
    env.PYTHONPATH.append(os.path.join('{root}', 'plugins'))
