import os

import tinytag

import PlayList
from PyQt5 import QtWidgets, QtCore, QtGui

from Tiles.CustomTile import MusicTile
from CustomWidgets.ScrollArea import ScrollView
from CustomWidgets.SearchScrollView import SearchScrollView

from tinytag import TinyTag


# todo: auto focus is taking away focus from the searchBar
class MyMusic(QtWidgets.QWidget):

    play = QtCore.pyqtSignal(bool, str, QtGui.QPixmap)  # path
    addFavourite = QtCore.pyqtSignal(bool)
    addToCollection = QtCore.pyqtSignal(bool)

    def __init__(self, notifier, *args, **kwargs):
        super(MyMusic, self).__init__(*args, **kwargs)

        self.notifier = notifier

        self.setLayout(QtWidgets.QVBoxLayout())

        self.stack_view = QtWidgets.QStackedWidget()

        self.view = MusicScrollView()
        self.view.play.connect(self.notifier.loadObject)
        self.view.addFavourite.connect(self.notifier.markFavourite)

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

        self.dirs = set()
        self.music_files = list()
        self.file_path = list()

        self.playlist = PlayList.PlayList()

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
            if tile.getTitle().lower().startswith(string.lower()):
                self.search_display_widget.addTile(tile)

    def pause(self):
        self.view.currently_playing_tile.pause()

    def playMusic(self):
        self.view.currently_playing_tile.playMusic()

    def addSearchDir(self, dir):
        self.dirs.add(dir)

    def deleteSearchDir(self, dirs):
        try:
            self.dirs.remove(dirs)

        except KeyError:
            pass

        self.loadFiles()

    def loadFiles(self):

        self.view.deleteAll()

        self.music_files = list()
        self.file_path = list()

        for path in self.dirs:
            for file in os.listdir(path):

                try:
                    music_file = TinyTag.get(os.path.join(path, file), image=True)
                    self.music_files.append(music_file)
                    self.file_path.append(os.path.join(path, file))

                except tinytag.TinyTagException:
                    pass

        for music, file in zip(self.music_files, self.file_path):
            self.view.addTile(music, file)

        for x in self.view.widgets():
            self.playlist.add_to_playlist(x)

    def getFilePaths(self)-> list:
        return self.file_path

    def getProperties(self):
        return self.view.getTileProperties()

    def notify(self, dirs):

        for dir in dirs:
            self.addSearchDir(dir)

        self.loadFiles()


class MusicScrollView(ScrollView):

    play = QtCore.pyqtSignal(object)  # path
    addFavourite = QtCore.pyqtSignal(object)
    addToCollection = QtCore.pyqtSignal(bool)

    def __init__(self, *args):
        super(MusicScrollView, self).__init__(*args)
        self.currently_playing_tile = None

    def currentlyPlaying(self):
        return self.currently_playing_tile

    def widgets(self):  # returns the tiles inside the QGridlayout
        _widgets = set()
        for x in range(self.grid_layout.count()):
            widget = self.grid_layout.itemAt(x)
            _widgets.add(widget.widget())

        return _widgets

    def addTile(self, music: tinytag.TinyTag, file=""):  # adds a new tile

        tile = MusicTile(music, file, (250, 250))
        tile.playing.connect(lambda obj: self.play.emit(obj))
        tile.addFavourite.connect(lambda obj: self.addFavourite.emit(obj))

        self.grid_layout.addWidget(tile, self._row, self._column)

        if self._column == 3:
            self._row += 1
            self._column = 0

        else:
            self._column += 1

    def getTileProperties(self):
        properties = set()
        row = 0
        while row < self.grid_layout.rowCount() - 1:
            column = 0
            while column < self.grid_layout.columnCount() -1:

                widget = self.grid_layout.itemAtPosition(row, column).widget()
                properties.add([widget.getFile(), widget.properties()])

                column += 1

            row += 1

        return properties
