import os.path

from PyQt5 import QtWidgets, QtGui, QtCore

import Paths
import Controller
import DB_Operations
import json

from CustomWidgets.VerticalTabs import TabWidget
from CustomWidgets.ScrollArea import ScrollView
from Tabs import Settings, MyMusic, Favourites, MyCollections, Statistics


class MainWindow(QtWidgets.QWidget):
    # This is the main window contains all the tabs

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowState(QtCore.Qt.WindowMaximized)

        with open(r"Resources/DarkTheme.qss") as file:
            self.setStyleSheet(file.read())

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.db_handler = DB_Operations.DBHandler()

        self.notifier = Controller.Notifier()

        self.windowFrame = QtWidgets.QWidget(objectName="WindowFrame")
        self.windowFrame.setLayout(QtWidgets.QHBoxLayout())
        self.windowFrame.setFixedHeight(30)
        self.windowFrame.layout().setSpacing(20)

        self.close_btn = QtWidgets.QPushButton(clicked=self.close, objectName="CloseButton")
        self.close_btn.setFixedSize(20, 20)
        self.max_min = QtWidgets.QPushButton(icon=QtGui.QIcon(Paths.MINIMIZE), clicked=self.showMinimized)
        self.max_min.setFixedSize(20, 20)

        self.tabWidget = TabWidget()

        self.myMusic = MyMusic.MyMusic()
        self.favourites = Favourites.Favourite()
        self.musicCollections = MyCollections.MyCollection()
        self.settings = Settings.Settings()
        self.statistics = Statistics.Statics()

        self.notifier.setPlayer(self.tabWidget.player_object())
        self.notifier.setMusicTab(self.myMusic)
        self.notifier.setFavouriteTab(self.favourites)
        self.notifier.setCollectionTab(self.musicCollections)
        self.notifier.setStatisticsTab(self.statistics)

        self.settings.path_added.connect(self.myMusic.notify)
        self.settings.autoPlayChecked.connect(self.notifier.enableAutoPlay)
        self.settings.path_deleted.connect(lambda x: self.myMusic.deleteSearchDir(x))

        self.tabWidget.addTab(self.myMusic, "My Music", QtGui.QIcon(Paths.MUSIC))
        self.tabWidget.addTab(self.favourites, "Favourites", QtGui.QIcon(Paths.STAR_FILLED))
        self.tabWidget.addTab(self.musicCollections, "Collections", QtGui.QIcon(Paths.LIBRARY))
        self.tabWidget.addTab(self.settings, "Settings", QtGui.QIcon(Paths.SETTINGS))
        self.tabWidget.addTab(self.statistics, "Statistics", QtGui.QIcon(Paths.STATISTICS))
        # QtWidgets.QHBoxLayout().insertWidget()

        self.windowFrame.layout().insertWidget(1, self.max_min, alignment=QtCore.Qt.AlignRight)
        self.windowFrame.layout().insertWidget(2, self.close_btn, alignment=QtCore.Qt.AlignRight)
        self.windowFrame.layout().setStretch(0, 1)

        self.layout().addWidget(self.windowFrame)
        self.layout().addWidget(self.tabWidget)

        self.deSerialize()

    def serialize(self):
        paths, checked = self.settings.serialize()

        self.db_handler.insertToPaths(paths)

        music_count = self.tabWidget.musicCount()
        print(music_count)

        json_dict = {"auto_play": checked, "music_count": music_count}

        with open(r"UserResources\save.json", 'w') as j_obj:
            json.dump(json_dict, j_obj)

        print("Paths: ", paths)
        print("Checked: ", checked)

    def deSerialize(self):

        paths = self.db_handler.getPaths()

        print("Paths", paths)
        if os.path.isfile(r"UserResources\save.json"):
            with open(r"UserResources\save.json") as j_obj:
                json_dict = json.load(j_obj)

                checked, music_count = json_dict['auto_play'], json_dict['music_count']

        else:
            checked = False
            music_count = {}

        self.settings.deSerialize(paths, checked)
        self.tabWidget.setMusicCount(music_count)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:  # todo: save files before closing

        self.serialize()
        super(MainWindow, self).closeEvent(a0)
