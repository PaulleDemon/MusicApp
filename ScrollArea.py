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

    def addTile(self, image: str=""):

        tile = Tile(image, (150, 150))
        # tile.setMinimumSize(100, 100)
        tile.setStyleSheet('background-color: red')
        self.grid_layout.addWidget(tile, self._row, self._column)
        print(self.grid_layout.rowCount()-1, self.grid_layout.columnCount()-1)

        if self._column == 3:
            self._row += 1
            self._column = 0

        else:
            self._column += 1