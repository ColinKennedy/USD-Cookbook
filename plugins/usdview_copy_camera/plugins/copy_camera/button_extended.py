#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui


class ButtonWithMenu(QtGui.QWidget):
    """A QPushButton that has a side menu which you can use to have optional actions.

    Unlike a QToolButton, this widget has both a clickable action and
    side menu. And unlike a QPushButton with a menu, this widget can
    separately enable/disable the main button while keeping the side
    menu clickable.

    Attributes:
        clicked (:class:`PySide.QtCore.Signal`):
            Any time the main button is clicked, this signal is fired.

    """

    _allowed_options = frozenset((QtGui.QTabBar.LeftSide, QtGui.QTabBar.RightSide))
    clicked = QtCore.Signal()

    def __init__(self, text, menu=None, side=QtGui.QTabBar.RightSide, parent=None):
        """Add a clickable button and a side menu.

        Args:
            text (str):
                The display text that will go on the main button.
            menu (:class:`PySide.QtGui.QMenu`, optional):
                A menu which will be added to the side menu. If no side menu is given,
                the side button is hidden, by default. Default is None.
            side (:class:`PySide.QtGui.QTabBar.ButtonPosition`):
                The side to place the side menu on. Default:
                :attr:`PySide.QtGui.QTabBar.RightSide`.
            parent (:class:`PySide.QtCore.QObject`, optional):
                Qt-based associated object. Default is None.

        Raises:
            ValueError: If `side` is not a valid option.

        """
        if side not in self._allowed_options:
            raise ValueError(
                'Side "{side}" is invalid. Options were, "{options}".'
                "".format(side=side, options=sorted(self._allowed_options))
            )

        super(ButtonWithMenu, self).__init__(parent=parent)

        self.setLayout(QtGui.QHBoxLayout())

        self._main_button = QtGui.QPushButton(text)
        self._side_button = QtGui.QPushButton()

        if side == QtGui.QTabBar.LeftSide:
            self.layout().addWidget(self._side_button)

        self.layout().addWidget(self._main_button)

        if side == QtGui.QTabBar.RightSide:
            self.layout().addWidget(self._side_button)

        self._initialize_default_settings()
        self._initialize_interactive_settings()

        if menu:
            self.set_side_menu(menu)

    def _initialize_default_settings(self):
        """Set the default appearance of this instance."""
        self._side_button.setVisible(False)
        self._side_button.setMaximumWidth(35)

        self.setContentsMargins(0, 0, 0, 0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        self._main_button.setToolTip('The main, "do it" action.')
        self._side_button.setToolTip("Click this to show alternative actions.")

        self._main_button.setObjectName("_main_button")
        self._side_button.setObjectName("_side_button")

    def _initialize_interactive_settings(self):
        """Whenever the main button is clicked, emit :attr:`ButtonWithMenu.clicked`."""
        self._main_button.clicked.connect(self.clicked.emit)

    def set_main_enabled(self, value):
        """Enable or disable the main button (but don't touch the side menu button).

        Args:
            value (bool): If False, disable this button. Otherwise, enable it.

        """
        self._main_button.setEnabled(value)

    def set_side_menu(self, menu):
        """Add a selectable menu to this widget and display it, as a clickable button.

        Args:
            menu (:class:`PySide.QtGui.QMenu`): The object to add to this instance.

        Raises:
            RuntimeError: If `menu` has no actions.

        """
        self._side_button.setVisible(True)

        if _is_empty(menu):
            raise RuntimeError('Menu "{menu}" cannot be empty.'.format(menu=menu))

        self._side_button.setMenu(menu)

    def setToolTip(self, text):
        """Add a tool-tip for the main button if this instance.

        Args:
            text (str): Some text to display to the user, if they hover over a button.

        """
        self._main_button.setToolTip(text)


def _is_empty(menu):
    """Check if `menu` is empty.

    Args:
        menu (:class:`PySide.QtGui.QMenu`): A widget which may or may not have actions.

    Returns:
        bool: Return True if `menu` is empty. Otherwise, return False.

    """
    actions = menu.actions()

    if not actions or actions == [menu.menuAction()]:
        return True

    return False
