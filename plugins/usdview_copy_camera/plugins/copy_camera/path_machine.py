#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A basic set of widgets for writing USD Prim paths."""

import functools

from PySide import QtCore, QtGui
from pxr import Sdf

from . import button_extended


_KNOWN_PATH_DELIMITERS = ("/", ".")
_PSEUDO_ROOT_PATH = Sdf.Path("/")
_STATE_STYLE_OPTIONS = {
    QtGui.QValidator.Acceptable: "acceptable",
    QtGui.QValidator.Intermediate: "warning",
    QtGui.QValidator.Invalid: "warning",
}


class _PathValidator(QtGui.QValidator):
    """A :class:`PySide.QtGui.QValidator` which checks if text is a valid Prim path.

    Attributes:
        validation_changed (:class:`PySide.QtCore.Signal`[:class:`PySide.QtGui.QValidator.State`]):
            Any time the validator state changes from something to
            something else, this signal gets fired.

    """

    validation_changed = QtCore.Signal(QtGui.QValidator.State)

    def __init__(self, allow_relative=False, parent=None):
        """Configure path options for this instance.

        Args:
            allow_relative (bool, optional):
                If False, only absolute paths are allowed. If True,
                relative paths are also okay. Default is False.
            parent (:class:`PySide.QtCore.QObject`, optional):
                Qt-based associated object. Default is None.

        """
        super(_PathValidator, self).__init__(parent=parent)

        self._allow_relative = allow_relative
        self._previous_state = None

    @staticmethod
    def _is_valid_intermediate(text):
        """If the user is in the middle of typing a path, return True.

        We do this so that, even if the given text is invalid, we trust that the user
        is about to make a valid path.

        e.g. they've typed "/foo/" because they are about to type "/foo/bar".

        Args:
            text (str): Some user-provided Prim path text.

        Returns:
            bool: If `text` is an intermediate path.

        """
        if not text.endswith(_KNOWN_PATH_DELIMITERS):
            return False

        return Sdf.Path.IsValidPathString(
            "".join(
                character
                for character in text
                if character not in _KNOWN_PATH_DELIMITERS
            )
        )

    def _emit_state_if_needed(self, state):
        """If a new state was found, emit :attr:`_PathValidator.validation_changed`.

        Args:
            state (:class:`PySide.QtGui.QValidator.State`):
                A state which may or may not be the same as this
                validator's most recent state.

        """
        if state == self._previous_state:
            return

        self._previous_state = state
        self.validation_changed.emit(state)

    def validate(self, text, position):  # pylint: disable=unused-argument
        """Check if `text` is a valid Prim path.

        Args:
            text (str):
                Some user-provided text. e.g. "/some/path".
            position (int or NoneType):
                The offset value for `text`. It is None whenever this
                instance validates the whole string.

        Returns:
            :class:`PySide.QtGui.QValidator.State`: The found state.

        """
        if not Sdf.Path.IsValidPathString(text):
            if self._is_valid_intermediate(text):
                self._emit_state_if_needed(QtGui.QValidator.Intermediate)

                return QtGui.QValidator.Intermediate

            self._emit_state_if_needed(QtGui.QValidator.Invalid)

            return QtGui.QValidator.Invalid

        if not self._allow_relative and not Sdf.Path(text).IsAbsolutePath():
            self._emit_state_if_needed(QtGui.QValidator.Invalid)

            return QtGui.QValidator.Invalid

        self._emit_state_if_needed(QtGui.QValidator.Acceptable)

        return QtGui.QValidator.Acceptable


class _PathChoiceValidator(_PathValidator):
    """A variation of :class:`_PathValidator` which checks for existing Prim paths."""

    def __init__(self, paths, parent=None):
        """Keep track of some Prim paths to exclude.

        If the user provides a path and it matches one of `paths`, it's
        considered at least a warning.

        Args:
            paths (container[:usd:`SdfPath`]):
                The paths to check for.
            parent (:class:`PySide.QtCore.QObject`, optional):
                Qt-based associated object. Default is None.

        """
        super(_PathChoiceValidator, self).__init__(parent=parent)

        self._paths = paths

    def validate(self, text, position):
        """Check if `text` is a valid Prim path which doesn't already exist.

        Args:
            text (str):
                Some user-provided text. e.g. "/some/path".
            position (int or NoneType):
                The offset value for `text`. It is None whenever this
                instance validates the whole string.

        Returns:
            :class:`PySide.QtGui.QValidator.State`: The found state.

        """
        state = super(_PathChoiceValidator, self).validate(text, position)

        if state != QtGui.QValidator.Acceptable:
            # Don't emit anything here because it was already emitted, in `super`
            return state

        path = Sdf.Path(text)
        path = path.GetPrimPath()

        for path_ in self._paths:
            if path == path_:
                self._emit_state_if_needed(QtGui.QValidator.Intermediate)

                return QtGui.QValidator.Intermediate

        self._emit_state_if_needed(QtGui.QValidator.Acceptable)

        return QtGui.QValidator.Acceptable


class _PathEdit(QtGui.QLineEdit):
    """A specialization of :class:`PySide.QtGui.QLineEdit` for writing absolute Prim paths.

    Pretty much, it exists just to make sure the user doesn't
    accidentally write a bad path.

    """

    def __init__(self, parent=None):
        """Add a default path for the user.

        Args:
            parent (:class:`PySide.QtCore.QObject`, optional):
                Qt-based associated object. Default is None.

        """
        super(_PathEdit, self).__init__(parent=parent)

        super(_PathEdit, self).setText("/")

    def setText(self, text):
        """Set this instance to use `text` unles it's invalid.

        Args:
            text (str): Some user-provided Prim path. e.g. "/foo/bar".

        Raises:
            ValueError: If `text` is empty or not absolute.

        """
        if not text:
            raise ValueError("Text cannot be empty.")

        if not Sdf.Path.IsValidPathString(text):
            raise ValueError(
                'Text "{text}" must be a valid Sdf Path.'.format(text=text)
            )

        super(_PathEdit, self).setText(text)


class PathWriter(QtGui.QWidget):
    """A small widget for writing Prim paths.

    Attributes:
        enter_pressed (:class:`PySide.QtCore.Signal`[:usd:`SdfPath`]):
            A signal which fires to let outside widgets know about the
            Prim path that the user wrote.

    """

    enter_pressed = QtCore.Signal(Sdf.Path)

    def __init__(self, paths=frozenset(), parent=None):
        """Keep track of some Prim paths to not allow as user input.

        Args:
            paths (container[:usd:`SdfPath`]):
                The paths to check for. If the user provides text
                which matches one of these paths, prevent them from
                accidentally overriding an existing Prim.
            parent (:class:`PySide.QtCore.QObject`, optional):
                Qt-based associated object. Default is None.

        """
        super(PathWriter, self).__init__(parent=parent)

        self.setLayout(QtGui.QHBoxLayout())

        self._label = QtGui.QLabel("Please write a Prim path:")
        self._line_edit = _PathEdit()
        self._cancel_button = QtGui.QPushButton("Cancel")
        self._enter_button = button_extended.ButtonWithMenu("Enter")

        self.layout().addWidget(self._label)
        self.layout().addWidget(self._line_edit)
        self.layout().addWidget(self._cancel_button)
        self.layout().addWidget(self._enter_button)

        self.populate(paths)
        self._initialize_default_settings()
        self._initialize_interactive_settings()

    def _initialize_default_settings(self):
        """Add default text and tool-tips for the children of this instance."""
        self._line_edit.setPlaceholderText("/some/unique/prim/path")

        widgets = [
            (self._cancel_button, "_cancel_button"),
            (self._enter_button, "_enter_button"),
            (self._label, "_label"),
            (self._line_edit, "_line_edit"),
        ]

        for widget, name in widgets:
            widget.setObjectName(name)

        self._cancel_button.setToolTip("Pressing this will close this widget.")
        self._enter_button.setToolTip("Press this to create the Prim.")
        tip = "Write a valid Prim path, here."
        self._label.setToolTip(tip)
        self._line_edit.setToolTip(tip)

    def _initialize_interactive_settings(self):
        """Wire button / typing functionality for this instance."""
        self._cancel_button.clicked.connect(self.close)
        self._enter_button.clicked.connect(self._enter_pressed)
        self._line_edit.textChanged.connect(self._refresh_enter_button)

    def _enter_pressed(self):
        """Emit :attr:`PathWriter.enter_pressed` with the user's provided text."""
        self.enter_pressed.emit(self.text())

    def _refresh_enter_button(self):
        """Update the enter button depending on if the user provided valid input."""
        is_valid = bool(Sdf.Path.IsValidPathString(self.text()))

        if is_valid:
            state = self._line_edit.validator().validate(self._line_edit.text(), None)

            if state != QtGui.QValidator.Acceptable:
                is_valid = False

        if not is_valid:
            self._enter_button.setToolTip(
                "This buttons is disabled because you must provide a valid, unique path."
            )
        else:
            self._enter_button.setToolTip("Press this to create the Prim.")

        self._enter_button.set_main_enabled(is_valid)

    def populate(self, paths=frozenset()):
        """Change the line edit so the user knows which paths are allowed and which aren't.

        Args:
            paths (container[:usd:`SdfPath`]):
                The paths to check for. If the user provides text
                which matches one of these paths, prevent them from
                accidentally overriding an existing Prim.

        """
        validator = _PathChoiceValidator(paths)
        validator.validation_changed.connect(
            functools.partial(_update_color_state, self._line_edit)
        )
        self._line_edit.setValidator(validator)

        self._refresh_enter_button()

    def text(self):
        """str: Get a cleaned-up version of whatever the user wrote."""
        return self._line_edit.text().strip()

    def set_side_menu(self, menu):
        """Add a selectable menu to this widget and display it, as a clickable button.

        Args:
            menu (:class:`PySide.QtGui.QMenu`): The object to add to this instance.

        """
        self._enter_button.set_side_menu(menu)

    def setText(self, text, raw=False):
        """Set this instance to use whatever text is provided.

        Args:
            text (str):
                A new Prim path to use for this instance.
            raw (bool, optional):
                If True, use `text` exactly as-is. If False,
                automatically try to make sure `text` is clean. Default
                is False.

        """
        if not raw:
            text = text.strip()

        self._line_edit.setText(text)


def _update_color_state(widget, state):
    """Update the colors on `widget`, depending on a given state.

    Args:
        widget (:class:`PySide.QtGui.QWidget`): The widget to change.
        state (:class:`PySide.QtGui.QValidator.State`): A state to display as a new color.

    Raises:
        ValueError: If `state` isn't a valid option for this function.

    """
    try:
        style = _STATE_STYLE_OPTIONS[state]
    except KeyError:
        raise ValueError(
            'State "{state}" was invalid. Options were, "{_STATE_STYLE_OPTIONS}".'
            "".format(state=state, _STATE_STYLE_OPTIONS=sorted(_STATE_STYLE_OPTIONS,))
        )

    widget.setProperty("state", style)
    style = widget.style()
    style.unpolish(widget)
    style.polish(widget)
