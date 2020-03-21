#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The Purpose-Swap plugin. Change between 2 preferred USD purposes with a single button.

Attributes:
    _PRIMARY_PURPOSE (str):
        The USD purpose which is swapped to whenever this plugin is
        "unsure" of which purpose to swap to.
    _SECONDARY_PURPOSE (str):
        The USD purpose which is only swapped onto if `_PRIMARY_PURPOSE`
        is on.

"""

# IMPORT STANDARD LIBRARIES
import functools
import os

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Tf
from pxr.Usdviewq import plugin

_BASE_MENU_NAME = "Swap Purposes"
_PRIMARY_PURPOSE = os.getenv("USDVIEW_PURPOSE_SWAP_PRIMARY_PURPOSE", "proxy")
_SECONDARY_PURPOSE = os.getenv("USDVIEW_PURPOSE_SWAP_SECONDARY_PURPOSE", "render")


class PurposeSwapContainer(plugin.PluginContainer):
    """The main registry class that initializes and runs the Purpose-Swap plugin."""

    def registerPlugins(self, _, __):
        """Check to make sure this plugin will work correctly.

        Raises:
            EnvironmentError: If the user selected an invalid pair of USD purposes.

        """
        if _PRIMARY_PURPOSE == _SECONDARY_PURPOSE:
            raise EnvironmentError(
                'Primary and secondary USD purposes are both "{_PRIMARY_PURPOSE}". '
                'Please set these values to something different.'.format(
                    _PRIMARY_PURPOSE=_PRIMARY_PURPOSE
                )
            )

    def configureView(self, registry, builder):
        """Add a QAction to the main menu of usdview.

        We use a couple private attributes in usdview's objects to get
        it done but oh well.

        Args:
            registry (:class:`pxr.Usdviewq.plugin.PluginRegistry`):
                The main class responsible for adding commands to
                usdview. We'll use this to access the current usdviewApi
                instance which usdview normally uses for its Python
                interpreter.
            builder (:class:`pxr.Usdviewq.plugin.PluginUIBuilder`):
                The object that has a reference to the main usdview
                window. We'll use this to add a custom QAction (which at
                the time of writing it looks like usdview doesn't have
                an API for).

        """
        action = builder._mainWindow.menuBar().addAction(_BASE_MENU_NAME)
        action.triggered.connect(
            functools.partial(_toggle_purposes, action, _ViewAdapter(registry._usdviewApi)),
        )


class _ViewAdapter(object):
    """A tiny convenience class for mapping USD purposes to attributes on usdview's model."""

    def __init__(self, usdview_api):
        """Store usdview's main interface object.

        Args:
            usdview_api (:class:`pxr.Usdviewq.usdviewApi.UsdviewApi`):
                The object that you'd normally use in the Python
                interpreter of usdview to modify the current stage.

        """
        super(_ViewAdapter, self).__init__()

        self._usdview_api = usdview_api

    def _view(self):
        """:class:`pxr.Usdviewq.viewSettingsDataModel.ViewSettingsDataModel: USD purpose switcher."""
        return self._usdview_api.dataModel.viewSettings

    def get(self, purpose):
        """Check if `purpose` is currently enabled in usdview.

        Args:
            purpose (str): Some USD purpose e.g. "guide", "proxy", or "render".

        Raises:
            ValueError: If `purpose` is not "guide", "proxy", or "render".

        Returns:
            bool: If the purpose is enabled.

        """
        options = {
            "guide": self._view().displayGuide,
            "proxy": self._view().displayProxy,
            "render": self._view().displayRender,
        }

        if purpose not in options:
            raise ValueError(
                'Purpose "{purpose}" is not supported. Options were, "{options}".'.format(
                    purpose=purpose, options=sorted(options.keys())
                )
            )

        return options[purpose]

    def set(self, purpose, value):
        """Change the given `purpose` to on or off.

        Args:
            purpose (str): Some USD purpose e.g. "guide", "proxy", or "render".
            value (bool): Turn `purpose` on or off.

        Raises:
            ValueError: If `purpose` is not "guide", "proxy", or "render".

        """
        options = {
            "guide": "displayGuide",
            "proxy": "displayProxy",
            "render": "displayRender",
        }

        if purpose not in options:
            raise ValueError(
                'Purpose "{purpose}" is not supported. Options were, "{options}".'.format(
                    purpose=purpose, options=sorted(options.keys())
                )
            )

        setattr(self._view(), options[purpose], value)


def _toggle_purposes(action, adapter):
    """Swap the USD purposes in the user's current usdview window.

    Args:
        action (:class:`Qt.QtWidgets.QAction`):
            A Qt object to modify after the USD purposes are swapped.
        adapter (:class:`_ViewAdapter`):
            A class to make swapping USD purposes easier.

    """
    if adapter.get(_SECONDARY_PURPOSE):
        adapter.set(_SECONDARY_PURPOSE, False)
        adapter.set(_PRIMARY_PURPOSE, True)

        text = _BASE_MENU_NAME + " [{_PRIMARY_PURPOSE}]".format(_PRIMARY_PURPOSE=_PRIMARY_PURPOSE)
    elif not adapter.get(_PRIMARY_PURPOSE):
        adapter.set(_PRIMARY_PURPOSE, True)
        text = _BASE_MENU_NAME + " [{_PRIMARY_PURPOSE}]".format(_PRIMARY_PURPOSE=_PRIMARY_PURPOSE)
    else:
        adapter.set(_PRIMARY_PURPOSE, False)
        adapter.set(_SECONDARY_PURPOSE, True)
        text = _BASE_MENU_NAME + " [{_SECONDARY_PURPOSE}]".format(_SECONDARY_PURPOSE=_SECONDARY_PURPOSE)

    action.setText(text)

Tf.Type.Define(PurposeSwapContainer)
