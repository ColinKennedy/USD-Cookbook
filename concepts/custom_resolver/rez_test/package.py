# -*- coding: utf-8 -*-

name = 'custom_resolver'

version = '1.0.0'


def commands():
    import os

    env.PXR_PLUGINPATH_NAME.append(os.path.join('{root}', 'plugins', 'custom_resolver'))
    env.PYTHONPATH.append(os.path.join('{root}', /home/selecaoone/projects/usd_experiments/examples/concepts/custom_resolver/plugins'))

    # root = '/home/selecaoone/projects/usd_experiments/examples/concepts/custom_resolver/project/build/testout/resources'
    # env.PXR_PLUGINPATH_NAME.append(os.path.join(root, 'plugins', 'custom_resolver'))
    # # TODO : This line may not be needed
    # env.PYTHONPATH.append(root)
