import os

from io import BytesIO
from PIL import ImageQt, Image
from PyQt5 import QtWidgets, QtGui
from ScrollArea import ScrollView
from mutagen import File


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

                music_file = File(os.path.join(path, file))
                if music_file is not None:
                    self.music_files.add(music_file)

                    if music_file.get('APIC:') is not None:
                        self.music_files_covr.append(music_file.get('APIC:').data)

                    else:
                        self.music_files_covr.append(None)

        for music, img in zip(self.music_files, self.music_files_covr):
            if img is not None:
                self.view.addTile(Image.open(BytesIO(img)))

            else:
                self.view.addTile(Image.open(r"Resources/Music.png"))

    def notify(self):
        pass
