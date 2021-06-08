from PyQt5 import QtWidgets


class ScrollView(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(ScrollView, self).__init__(*args, **kwargs)
        self.setObjectName("ScrollView")

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.widget = QtWidgets.QWidget()
        self.grid_layout = QtWidgets.QGridLayout(self.widget)
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidget(self.widget)
        self.scrollArea.setWidgetResizable(True)

        self.grid_layout.setSpacing(50)

        self._row = 0
        self._column = 0

        self.layout().addWidget(self.scrollArea)

    def enterEvent(self, a0) -> None:
        super(ScrollView, self).enterEvent(a0)

        if not isinstance(QtWidgets.QApplication.focusWidget(), QtWidgets.QLineEdit):
            self.setFocus()

    def getWidgets(self):
        _widgets = list()

        for x in range(self.grid_layout.count()):
            _widgets.append(self.grid_layout.itemAt(x).widget())

        return _widgets

    def removeAll(self):
        for x in self.getWidgets():
            self.grid_layout.removeWidget(x)

    def deleteAll(self):

        self.widget.deleteLater()

        self.widget = QtWidgets.QWidget()
        self.grid_layout = QtWidgets.QGridLayout(self.widget)
        self.grid_layout.setSpacing(50)
        self.scrollArea.setWidget(self.widget)

        self._row = 0
        self._column = 0

    @property
    def row(self):
        return self._row

    @property
    def column(self):
        return self._column
