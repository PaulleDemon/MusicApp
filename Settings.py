from PyQt5 import QtWidgets, QtGui, QtCore
import os


class Settings(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(Settings, self).__init__(*args, **kwargs)

        self.setLayout(QtWidgets.QVBoxLayout())

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

        self.layout().addWidget(self.header)
        self.layout().addWidget(self.scroll_area)
        self.layout().addWidget(self.add_btn)

        self.addRow()

    def addRow(self):

        self.v_layout.insertWidget(self.v_layout.count() - 1, EditableLabel(), alignment=QtCore.Qt.AlignTop)

        if self.scroll_area.verticalScrollBar().isVisible():
            QtCore.QTimer.singleShot(10,
                                     lambda: self.scroll_area.verticalScrollBar().setValue(
                                         self.scroll_area.verticalScrollBar().maximum()))


class EditableLabel(QtWidgets.QWidget):

    validPathEntered = QtCore.pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(EditableLabel, self).__init__(*args, **kwargs)

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.path_edit = QtWidgets.QLineEdit()
        self.path_edit.setPlaceholderText("path")
        self.path_edit.setProperty("Valid", "false")
        self.path_edit.textChanged.connect(self.validate)

        self.select_folder_btn = QtWidgets.QPushButton(icon=QtGui.QIcon(r"Resources/Folder.png"))
        self.select_folder_btn.clicked.connect(self.select_path)
        self.select_folder_btn.setToolTip("Select folder")

        self.delete_path_btn = QtWidgets.QPushButton("x")
        self.delete_path_btn.setToolTip("Remove")
        self.delete_path_btn.clicked.connect(self.deleteLater)
        self.delete_path_btn.setFixedWidth(25)

        self.layout().addWidget(self.path_edit)
        self.layout().addWidget(self.select_folder_btn)
        self.layout().addWidget(self.delete_path_btn)

        self.path_edit.setStyleSheet("QLineEdit[valid='false']{border: 2px solid red;}")

    def select_path(self):
        file = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.path_edit.setText(file)

    def validate(self, text):
        valid = os.path.isdir(text)
        print(valid)
        if not valid:
            self.path_edit.setProperty("valid", "false")
            self.path_edit.style().unpolish(self.path_edit)
            self.path_edit.style().polish(self.path_edit)
            self.path_edit.setToolTip("Invalid Path")

        else:
            self.path_edit.setProperty("valid", "true")
            self.path_edit.style().unpolish(self.path_edit)
            self.path_edit.style().polish(self.path_edit)
            self.path_edit.setToolTip("path")

            self.validPathEntered.emit(self.path_edit.text())