import io
import os

from io import BytesIO

import tinytag
from PIL import ImageQt, Image
from PyQt5 import QtWidgets, QtGui
from ScrollArea import ScrollView
from mutagen import File
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

        self.addSearchDir(r"C:\Users\Paul\Desktop\all folders\english albumsong\english songs")

        self.loadFiles()

    def addSearchDir(self, dir):
        self.dirs.add(dir)

    def deleteSearchDir(self, dir):
        self.dirs.remove(dir)

    def loadFiles(self):

        for path in self.dirs:
            for file in os.listdir(path):

                try:
                    music_file = TinyTag.get(os.path.join(path, file), image=True)
                    self.music_files.add(music_file)

                except tinytag.TinyTagException:
                    pass

        for music in self.music_files:
            image = music.get_image()
            title = music.title

            if not title:
                title = "Unknown"

            if not image:
                image = r"Resources/Music.png"
                self.view.addTile(Image.open(image), title)

            else:
                self.view.addTile(Image.open(BytesIO(image)), title)

    def notify(self):
        pass
