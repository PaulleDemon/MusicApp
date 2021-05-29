from Tiles.CustomTile import MusicTile
from Tiles.SearchTile import SearchTile
from .ScrollArea import ScrollView
from PyQt5 import QtCore, QtGui


class SearchScrollView(ScrollView):
    play = QtCore.pyqtSignal(bool, str, QtGui.QPixmap)  # path
    addFavourite = QtCore.pyqtSignal(bool, str, QtGui.QPixmap)
    addToCollection = QtCore.pyqtSignal(bool)

    def __init__(self, *args):
        super(SearchScrollView, self).__init__(*args)

    def addTile(self, obj: MusicTile):
        tile = SearchTile(obj, (250, 250))
        self.addWidget(tile)

    def addWidget(self, widget):
        print("Adding: ")
        self.grid_layout.addWidget(widget, self._row, self._column)
        if self._column == 3:
            self._row += 1
            self._column = 0

        else:
            self._column += 1

    def removeTileParent(self):
        print("Starting removing....", self.grid_layout.count())
        print(self.getWidgets())
        for x in range(self.grid_layout.count()):
            searchTile = self.grid_layout.itemAt(x)

            if searchTile:
                tile = searchTile.widget()
                tile.deleteLater()

