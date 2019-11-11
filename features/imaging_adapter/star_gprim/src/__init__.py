#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module brings the compiled _star.so module into this package's namespace."""

from . import _star
from pxr import Tf
Tf.PrepareModule(_star, locals())
del Tf

try:
    import __DOC
    __DOC.Execute(locals())
    del __DOC
except Exception:
    try:
        import __tmpDoc
        __tmpDoc.Execute(locals())
        del __tmpDoc
    except:
        pass
