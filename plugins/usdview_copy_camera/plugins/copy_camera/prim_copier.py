#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools

from PySide import QtCore, QtGui
from pxr import Sdf

_PSEUDO_ROOT_PATH = Sdf.Path("/")


class _PathValidator(QtGui.QValidator):
    validation_changed = QtCore.Signal(QtGui.QValidator.State)

    def __init__(self, allow_relative=False, parent=None):
        super(_PathValidator, self).__init__(parent=parent)

        self._allow_relative = allow_relative
        self._previous_state = None

    def _emit_state_if_needed(self, state):
        if state == self._previous_state:
            return

        self._previous_state = state
        self.validation_changed.emit(state)

    def validate(self, text, position):
        if not Sdf.Path.IsValidPathString(text):
            self._emit_state_if_needed(QtGui.QValidator.Invalid)

            return QtGui.QValidator.Invalid

        if not self._allow_relative and not Sdf.Path(text).IsAbsolutePath():
            self._emit_state_if_needed(QtGui.QValidator.Invalid)

            return QtGui.QValidator.Invalid

        self._emit_state_if_needed(QtGui.QValidator.Acceptable)

        return QtGui.QValidator.Acceptable


class _PathChoiceValidator(_PathValidator):
    def __init__(self, paths, parent=None):
        super(_PathChoiceValidator, self).__init__(parent=parent)

        self._paths = paths

    def validate(self, text, position):
        state = super(_PathChoiceValidator, self).validate(text, position)

        if state != QtGui.QValidator.Acceptable:
            # Don't emit anything here because it was already emitted, in `super`
            return state

        path = Sdf.Path(text)

        for path_ in self._paths:
            if path == path_:
                self._emit_state_if_needed(QtGui.QValidator.Intermediate)

                return QtGui.QValidator.Intermediate

        self._emit_state_if_needed(QtGui.QValidator.Acceptable)

        return QtGui.QValidator.Acceptable


class _PathEdit(QtGui.QLineEdit):
    def __init__(self, parent=None):
        super(_PathEdit, self).__init__(parent=parent)

        super(_PathEdit, self).setText("/")

    def setText(self, text):
        if not text:
            raise ValueError("Text cannot be empty.")

        if not Sdf.Path.IsValidPathString(text):
            raise ValueError('Text "{text}" must be a valid Sdf Path.'.format(text=text))

        super(_PathEdit, self).setText(text)


class PathWriter(QtGui.QWidget):
    enter_pressed = QtCore.Signal(Sdf.Path)

    def __init__(self, paths=frozenset(), parent=None):
        super(PathWriter, self).__init__(parent=parent)

        self.setLayout(QtGui.QHBoxLayout())

        self._label = QtGui.QLabel("Please write a Prim path:")
        self._line_edit = _PathEdit()
        self._enter_button = QtGui.QPushButton("Enter")
        self._cancel_button = QtGui.QPushButton("Cancel")

        self.layout().addWidget(self._label)
        self.layout().addWidget(self._line_edit)
        self.layout().addWidget(self._enter_button)
        self.layout().addWidget(self._cancel_button)

        self.populate(paths)
        self._initialize_default_settings()
        self._initialize_interactive_settings()
        self._refresh_enter_button()

    def _initialize_default_settings(self):
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
        self._cancel_button.clicked.connect(self.close)
        self._enter_button.clicked.connect(self._enter_pressed)
        self._line_edit.textChanged.connect(self._refresh_enter_button)

    def _enter_pressed(self):
        self.enter_pressed.emit(self.get_text())

    def _refresh_enter_button(self):
        is_valid = bool(Sdf.Path.IsValidPathString(self.get_text()))

        if is_valid:
            state = self._line_edit.validator().validate(self._line_edit.text(), None)

            if state != QtGui.QValidator.Acceptable:
                is_valid = False

        if not is_valid:
            self._enter_button.setToolTip("This buttons is disabled because you must provide a valid, unique path.")
        else:
            self._enter_button.setToolTip("Press this to create the Prim.")

        self._enter_button.setEnabled(is_valid)

    def populate(self, paths=frozenset()):
        validator = _PathChoiceValidator(paths)
        validator.validation_changed.connect(functools.partial(_update_color_state, self._line_edit))
        self._line_edit.setValidator(validator)

    def get_text(self):
        return self._line_edit.text().strip()

    def set_text(self, text):
        return self._line_edit.setText(text)


def _update_color_state(widget, state):
    options = {
        QtGui.QValidator.Acceptable: "acceptable",
        QtGui.QValidator.Intermediate: "warning",
        QtGui.QValidator.Invalid: "warning",

    }

    try:
        style = options[state]
    except KeyError:
        raise RuntimeError('State "{state}" was invalid. Options were, "{options}".'.format(state=state, options=sorted(options)))

    widget.setProperty("state", style)
    style = widget.style()
    style.unpolish(widget)
    style.polish(widget)
