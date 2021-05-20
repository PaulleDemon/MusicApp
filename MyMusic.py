import os

import tinytag
from PyQt5 import QtWidgets, QtCore
from ScrollArea import ScrollView
from tinytag import TinyTag


class MyMusic(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(MyMusic, self).__init__(*args, **kwargs)

        self.setLayout(QtWidgets.QVBoxLayout())

        self.view = ScrollView()
        self.layout().addWidget(self.view)

        self.dirs = set()
        self.music_files = set()
        self.music_files_covr = list()

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
        print("DIRS: ", self.dirs)
        self.music_files = set()

        for path in self.dirs:
            for file in os.listdir(path):

                try:
                    music_file = TinyTag.get(os.path.join(path, file), image=True)
                    self.music_files.add(music_file)

                except tinytag.TinyTagException:
                    pass

        for music in self.music_files:  # you gotta clear music files dumb
            self.view.addTile(music)

    def notify(self, dirs):

        for dir in dirs:
            self.addSearchDir(dir)

        self.loadFiles()
