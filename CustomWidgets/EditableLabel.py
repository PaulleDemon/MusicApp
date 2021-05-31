from PyQt5 import QtWidgets, QtCore


class EditableLabel(QtWidgets.QWidget):
    textChanged = QtCore.pyqtSignal(str)

    def __init__(self, text="", placeHolder="class name", defaultText: str = "", alignment=QtCore.Qt.AlignLeft,
                 *args, **kwargs):
        super(EditableLabel, self).__init__(*args, **kwargs)

        self._text = text
        self.defaultText = defaultText
        self._toolTipHeading = ""

        self.hlayout = QtWidgets.QHBoxLayout(self)
        self.hlayout.setContentsMargins(0, 0, 0, 0)

        self.vlayout = QtWidgets.QVBoxLayout()
        self.vlayout.setContentsMargins(0, 0, 0, 0)

        self._label = QtWidgets.QLabel(text, alignment=alignment)
        self._label.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)

        self._edit_label = QtWidgets.QLineEdit()
        self._edit_label.textChanged.connect(self._textChanged)
        self._edit_label.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self._edit_label.editingFinished.connect(self.showLabel)
        self._edit_label.setText(self._text) if self._text else self._edit_label.setText(self.defaultText)
        self._edit_label.setPlaceholderText(placeHolder)

        self.vlayout.addWidget(self._label)
        self.vlayout.addWidget(self._edit_label)
        self.showLabel()

        self.hlayout.addLayout(self.vlayout)
        self.setMinimumSize(20, 10)

    def _textChanged(self, text):
        self._text = text
        self.textChanged.emit(text)

    def showLabel(self):
        self._label.setText(self._edit_label.text())
        self._edit_label.hide()
        self._label.show()

    def mouseDoubleClickEvent(self, event, pos=None):

        pos = event.pos()
        if self._label.geometry().contains(pos):

            self._label.hide()
            self._edit_label.show()
            self._edit_label.setText(self._label.text())
            self._edit_label.selectAll()

            if self._edit_label.text() == self.defaultText:
                self._edit_label.selectAll()

            self._edit_label.setFocus()
            super(EditableLabel, self).mouseDoubleClickEvent(event)

    def setText(self, text):
        self._label.setText(text)
        self._edit_label.setText(text)
        self._text = text

    def getText(self):
        return self._text
