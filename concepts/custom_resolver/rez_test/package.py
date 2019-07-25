# -*- coding: utf-8 -*-

name = 'custom_resolver'

version = '1.0.0'


def commands():
    import os

    root = '/home/selecaoone/projects/usd_experiments/examples/concepts/custom_resolver/project/build/install'
    env.PXR_PLUGINPATH_NAME.append(os.path.join(root, 'resources'))
