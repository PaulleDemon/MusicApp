from PyQt5 import QtWidgets, QtCore, QtGui


class Favourite(QtWidgets.QWidget):

    play = QtCore.pyqtSignal(bool, str, QtGui.QPixmap)  # path
    addFavourite = QtCore.pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super(Favourite, self).__init__(*args, **kwargs)

        self.setLayout(QtWidgets.QVBoxLayout())

        self.view = MusicScrollView()
        self.view.play.connect(lambda x, path, pixmap: self.play.emit(x, path, pixmap))

        self.layout().addWidget(self.view)

        self.dirs = set()
        self.music_files = list()
        self.file_path = list()

    def pause(self):
        print(self.view.currently_playing_tile)
        self.view.currently_playing_tile.pause()

    def playMusic(self):
        print(self.view.currently_playing_tile)
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
        pass

    def getFilePaths(self):
        return self.file_path

    def getProperties(self):
        return self.view.getTileProperties()

    def notify(self, dirs):

        for dir in dirs:
            self.addSearchDir(dir)

        self.loadFiles()


class MusicScrollView(ScrollView):

    play = QtCore.pyqtSignal(bool, str, QtGui.QPixmap)  # path
    addFavourite = QtCore.pyqtSignal(bool, str, QtGui.QPixmap)
    addToCollection = QtCore.pyqtSignal(bool)

    def __init__(self, *args):
        super(MusicScrollView, self).__init__(*args)
        self.currently_playing_tile = None

    def currentlyPlaying(self):
        return self.currently_playing_tile

    def _play(self, x, path, pixmap, obj):

        if self.currently_playing_tile:
            self.currently_playing_tile.playMusic()

        self.currently_playing_tile = obj
        self.play.emit(x, path, pixmap)

    def addTile(self, music: tinytag.TinyTag, file=""):

        tile = MusicTile(music, file, (250, 250))
        tile.playing.connect(self._play)

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