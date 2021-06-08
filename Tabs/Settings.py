import os
from PyQt5 import QtWidgets, QtGui, QtCore

import Paths
from Controller import Notifier


class Settings(QtWidgets.QWidget):  # settings tab has ability to add new local paths, enable/disable auto play

    path_added = QtCore.pyqtSignal(set)
    path_deleted = QtCore.pyqtSignal(str)

    autoPlayChecked = QtCore.pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super(Settings, self).__init__(*args, **kwargs)

        self.setLayout(QtWidgets.QVBoxLayout())

        self.setObjectName("Settings")

        widget = QtWidgets.QWidget()
        self.v_layout = QtWidgets.QVBoxLayout(widget)
        self.v_layout.addStretch(1)

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidget(widget)
        self.scroll_area.setWidgetResizable(True)

        self.header = QtWidgets.QLabel("Add Music Paths")
        self.header.setFixedHeight(30)

        self.add_btn = QtWidgets.QPushButton("Add Path")
        self.add_btn.clicked.connect(self.addRow)

        self.auto_play_check_btn = QtWidgets.QCheckBox("Auto play")
        self.auto_play_check_btn.clicked.connect(self.autoPlay)

        self.layout().addWidget(self.auto_play_check_btn)
        self.layout().addWidget(self.header)
        self.layout().addWidget(self.scroll_area)
        self.layout().addWidget(self.add_btn)

        self.notify = Notifier()

        self.addRow()

    def addRow(self):

        editable_label = PathEdit()
        editable_label.path_edited.connect(self._path_added)
        editable_label.path_deleted.connect(self._path_deleted)

        self.v_layout.insertWidget(self.v_layout.count() - 1, editable_label, alignment=QtCore.Qt.AlignTop)

        if self.scroll_area.verticalScrollBar().isVisible():
            QtCore.QTimer.singleShot(10,
                                     lambda: self.scroll_area.verticalScrollBar().setValue(
                                         self.scroll_area.verticalScrollBar().maximum()))

    def autoPlay(self, checked):
        self.autoPlayChecked.emit(checked)

    def _path_added(self):
        self.path_added.emit(self.directories())

    def _path_deleted(self, dir):
        self.path_deleted.emit(dir)

    def directories(self) -> set:
        paths = set()
        for x in range(self.v_layout.count()-1):
            path = self.v_layout.itemAt(x).widget()
            if path.valid():
                paths.add(path.getText())

        return paths


class PathEdit(QtWidgets.QWidget):

    path_edited = QtCore.pyqtSignal(str)
    path_deleted = QtCore.pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(PathEdit, self).__init__(*args, **kwargs)

        self._valid = False

        self.setObjectName("PathEdit")

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.path_edit = QtWidgets.QLineEdit()
        self.path_edit.setPlaceholderText("path")
        self.path_edit.setProperty("Valid", "false")
        self.path_edit.textChanged.connect(self.validate)

        self.select_folder_btn = QtWidgets.QPushButton(icon=QtGui.QIcon(Paths.FOLDER))
        self.select_folder_btn.setIconSize(QtCore.QSize(30, 30))
        self.select_folder_btn.clicked.connect(self.select_path)
        self.select_folder_btn.setToolTip("Select folder")

        self.delete_path_btn = QtWidgets.QPushButton("x")
        self.delete_path_btn.setToolTip("Remove")
        self.delete_path_btn.clicked.connect(self.remove_path)

        # self.select_folder_btn.setFixedWidth(30)
        # self.delete_path_btn.setFixedWidth(30)

        self.layout().addWidget(self.path_edit)
        self.layout().addWidget(self.select_folder_btn)
        self.layout().addWidget(self.delete_path_btn)

    def select_path(self):
        file = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Tabs"))
        self.path_edit.setText(file)

    def valid(self)->bool:
        return self._valid

    def getText(self):
        return self.path_edit.text()

    def remove_path(self):
        self.path_deleted.emit(self.path_edit.text())
        self.deleteLater()

    def validate(self, text):
        valid = os.path.isdir(text)

        if not valid:
            self.path_edit.setProperty("valid", "false")
            self.path_edit.style().unpolish(self.path_edit)
            self.path_edit.style().polish(self.path_edit)
            self.path_edit.setToolTip("Invalid Path")
            self._valid = False

        else:
            self.path_edit.setProperty("valid", "true")
            self.path_edit.style().unpolish(self.path_edit)
            self.path_edit.style().polish(self.path_edit)
            self.path_edit.setToolTip("path")
            self._valid = True

            self.path_edited.emit(self.path_edit.text())