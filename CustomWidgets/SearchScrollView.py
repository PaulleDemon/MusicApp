from Tiles.Music_FavouritesTile import MusicTile
from Tiles.SearchTile import SearchTile, CollectionSearchTile
from CustomWidgets.ScrollArea import ScrollView
from PyQt5 import QtCore, QtGui


class SearchScrollView(ScrollView):
    play = QtCore.pyqtSignal(bool, str, QtGui.QPixmap)  # path
    addFavourite = QtCore.pyqtSignal(bool, str, QtGui.QPixmap)
    addToCollection = QtCore.pyqtSignal(bool)

    def addMusicTile(self, obj: MusicTile):
        tile = SearchTile(obj, (250, 350))
        self.addWidget(tile)

    def addCollectionTile(self, obj):
        tile = CollectionSearchTile(obj, (250, 350))
        self.addWidget(tile)

    def addWidget(self, widget):
        self.grid_layout.addWidget(widget, self._row, self._column)
        if self._column == 3:
            self._row += 1
            self._column = 0

        else:
            self._column += 1

    def removeTileParent(self):
        for x in range(self.grid_layout.count()):
            searchTile = self.grid_layout.itemAt(x).widget()
            searchTile.deleteLater()


