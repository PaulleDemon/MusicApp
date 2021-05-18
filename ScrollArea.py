from PyQt5 import QtWidgets
from Tile import Tile


class ScrollView(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(ScrollView, self).__init__(*args, **kwargs)

        self.setLayout(QtWidgets.QVBoxLayout())

        widget = QtWidgets.QWidget()

        self.grid_layout = QtWidgets.QGridLayout(widget)
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidget(widget)
        self.scrollArea.setWidgetResizable(True)

        self.grid_layout.setSpacing(50)

        self.row_width = 4

        self._row = 0
        self._column = 0

        self.layout().addWidget(self.scrollArea)

    def enterEvent(self, a0) -> None:
        super(ScrollView, self).enterEvent(a0)
        self.setFocus()

    def addTile(self, image, title):

        tile = Tile(image, title, (150, 150))

        self.grid_layout.addWidget(tile, self._row, self._column)

        if self._column == 3:
            self._row += 1
            self._column = 0

        else:
            self._column += 1
