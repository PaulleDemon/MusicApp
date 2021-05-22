from PyQt5 import QtWidgets


class ScrollView(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(ScrollView, self).__init__(*args, **kwargs)
        self.setObjectName("ScrollView")

        self.setLayout(QtWidgets.QVBoxLayout())

        self.widget = QtWidgets.QWidget()
        self.grid_layout = QtWidgets.QGridLayout(self.widget)
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidget(self.widget)
        self.scrollArea.setWidgetResizable(True)

        self.grid_layout.setSpacing(50)

        self.row_width = 4

        self._row = 0
        self._column = 0

        self.layout().addWidget(self.scrollArea)

    def enterEvent(self, a0) -> None:
        super(ScrollView, self).enterEvent(a0)
        self.setFocus()

    def deleteAll(self):

        self.widget.deleteLater()

        self.widget = QtWidgets.QWidget()
        self.grid_layout = QtWidgets.QGridLayout(self.widget)
        self.grid_layout.setSpacing(50)
        self.scrollArea.setWidget(self.widget)