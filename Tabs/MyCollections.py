from PyQt5 import QtWidgets, QtCore
from CustomWidgets import ScrollArea
from CustomWidgets.SearchScrollView import SearchScrollView
from Tiles.CollectionTile import CollectionTile


class MyCollection(QtWidgets.QWidget):

    playing = QtCore.pyqtSignal(object)
    reloadPlayList = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(MyCollection, self).__init__(*args, **kwargs)

        self._current_playing_collection = None

        self.setLayout(QtWidgets.QVBoxLayout())
        self.stack_view = QtWidgets.QStackedWidget()

        self.view = CollectionScrollView()
        self.view.playing.connect(self.setCurrentPlayingCollection)
        self.view.reloadPlaylist.connect(self.reloadPlayList.emit)

        self.search_bar = QtWidgets.QLineEdit()
        self.search_bar.setClearButtonEnabled(True)
        self.search_bar.setPlaceholderText("Search")
        self.search_bar.setMinimumWidth(350)
        self.search_bar.textChanged.connect(self.search)

        self.search_display_widget = SearchScrollView()

        self.stack_view.addWidget(self.view)
        self.stack_view.addWidget(self.search_display_widget)

        self.stack_view.setCurrentIndex(0)

        self.layout().addWidget(self.search_bar, alignment=QtCore.Qt.AlignRight)
        self.layout().addWidget(self.stack_view)

    def addTile(self, obj, collection_name):
        self.view.addCollectionTile(obj, collection_name)

    def removeTile(self, obj, collection_name):
        self.view.removeInnerCollectionTile(obj, collection_name)

    def getCollections(self):
        return self.view.getCollectionNames()

    def setCurrentPlayingCollection(self, obj):
        self._current_playing_collection = obj
        self.playing.emit(self._current_playing_collection)

    def playlist(self):
        return self._current_playing_collection.playlist() if self._current_playing_collection else None

    def search(self, string):
        if not string:
            self.stack_view.setCurrentIndex(0)
            return

        if self.stack_view.currentIndex() == 0:
            self.stack_view.setCurrentIndex(1)

        widgets = self.view.widgets()

        self.search_display_widget.removeTileParent()
        self.search_display_widget.deleteAll()
        for tile in widgets:
            if tile.getCollectionName().lower().startswith(string.lower()):
                self.search_display_widget.addCollectionTile(tile)


class CollectionScrollView(ScrollArea.ScrollView):

    playing = QtCore.pyqtSignal(object)
    reloadPlaylist = QtCore.pyqtSignal()

    def __init__(self, *args):
        super(CollectionScrollView, self).__init__(*args)

    def addCollectionTile(self, obj, name: str):
        if name not in self.getCollectionNames():
            tile = CollectionTile(name, (250, 250))
            tile.playing.connect(self.playing.emit)
            tile.reloadPlayList.connect(self.reloadPlaylist.emit)
            self.addWidget(tile)

        collection_tile = self.getWidgetByName(name)
        collection_tile.addToCollection(obj)

    def removeInnerCollectionTile(self, obj, collection_name):
        collection_tile = self.getWidgetByName(collection_name)
        collection_tile.removeFromCollection(obj)

    def getWidgetByName(self, name):
        for x in self.getWidgets():
            if x.getCollectionName() == name:
                return x

    def addWidget(self, widget):
        self.grid_layout.addWidget(widget, self._row, self._column)
        if self._column == 3:
            self._row += 1
            self._column = 0

        else:
            self._column += 1

    def getCollectionNames(self):
        wid = self.getWidgets()
        return [x.getCollectionName() for x in wid]

    def widgets(self):
        return self.getWidgets()

    def removeCollectionTile(self, obj):

        child = obj.getChildren().copy()

        for x in child:
            if isinstance(x, CollectionTile):
                self.grid_layout.removeCollectionTile(x)
                x.deleteLater()

        widgets = self.getWidgets()
        self.deleteAll()

        for widget in widgets:
            self.addCollectionTile(widget.parent)
            widget.parent.removeChild(widget)

        self.grid_layout.update()
