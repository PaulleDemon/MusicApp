import os

import tinytag
from PyQt5 import QtWidgets, QtCore, QtGui

from CustomWidgets.Tile import MusicTile
from CustomWidgets.ScrollArea import ScrollView
from tinytag import TinyTag


class MyMusic(QtWidgets.QWidget):

    play = QtCore.pyqtSignal(bool, str, QtGui.QPixmap)  # path
    addFavourite = QtCore.pyqtSignal(bool)
    addToCollection = QtCore.pyqtSignal(bool)

    def __init__(self, notifier, *args, **kwargs):
        super(MyMusic, self).__init__(*args, **kwargs)

        self.notifier = notifier

        self.setLayout(QtWidgets.QVBoxLayout())

        self.view = MusicScrollView()
        self.view.play.connect(self.notifier.loadObject)
        self.view.addFavourite.connect(self.notifier.markFavourite)

        self.search_bar = QtWidgets.QLineEdit()
        self.search_bar.setPlaceholderText("Search")
        self.search_bar.setMinimumWidth(350)
        self.search_bar.textChanged.connect(self.search)

        self.search_display_widget = ScrollView()
        self.search_display_widget.setLayout(QtWidgets.QGridLayout())

        self.layout().addWidget(self.search_bar, alignment=QtCore.Qt.AlignRight)
        self.layout().addWidget(self.view)
        self.layout().insertWidget(1, self.search_display_widget, alignment=QtCore.Qt.AlignTop)

        self.dirs = set()
        self.music_files = list()
        self.file_path = list()

    def search(self, string):  # todo: complete search bar
        widgets = self.view.widgets()

        self.search_display_widget.show()
        if not string:
            for tile in widgets:
                tile.show()
                # self.search_display_widget.hide()
            return

        for tile in widgets:
            if not tile.getTitle().startswith(string):
                tile.hide()
                # new_tile = MusicTile(tile.getMusic(), tile.getFile())
                # self.search_display_widget.grid_layout.addWidget(new_tile)

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

    def widgets(self):
        _widgets = set()
        for x in range(self.grid_layout.count()):
            widget = self.grid_layout.itemAt(x)
            _widgets.add(widget.widget())

        return _widgets

    def addTile(self, music: tinytag.TinyTag, file=""):

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
