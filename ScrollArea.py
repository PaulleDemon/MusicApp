from PyQt5 import QtWidgets, QtCore
from Tile import MusicTile
import tinytag


class ScrollView(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(ScrollView, self).__init__(*args, **kwargs)

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
        self.scrollArea.setStyleSheet('background-color: red;')

    def enterEvent(self, a0) -> None:
        super(ScrollView, self).enterEvent(a0)
        self.setFocus()

    def deleteAll(self):

        self.widget.deleteLater()

        self.widget = QtWidgets.QWidget()
        self.grid_layout = QtWidgets.QGridLayout(self.widget)
        self.grid_layout.setSpacing(50)
        self.scrollArea.setWidget(self.widget)


    def addTile(self, music: tinytag.TinyTag):

        tile = MusicTile(music, (250, 250))
        self.grid_layout.addWidget(tile, self._row, self._column)

        if self._column == 3:
            self._row += 1
            self._column = 0

        else:
            self._column += 1
