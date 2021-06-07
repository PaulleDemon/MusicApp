from PyQt5 import QtWidgets, QtGui

import Paths
import Controller
import DB_Operations

from CustomWidgets.VerticalTabs import TabWidget
from CustomWidgets.ScrollArea import ScrollView
from Tabs import Settings, MyMusic, Favourites, MyCollections


class MainWindow(QtWidgets.QWidget):
    # This is the main window contains all the tabs

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.showMaximized()

        with open(r"Resources/DarkTheme.qss") as file:
            self.setStyleSheet(file.read())

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.db_handler = DB_Operations.DBHandler()

        self.notifier = Controller.Notifier()

        self.tabWidget = TabWidget()

        self.myMusic = MyMusic.MyMusic()
        self.favourites = Favourites.Favourite()
        self.musicCollections = MyCollections.MyCollection()
        self.settings = Settings.Settings()
        self.statistics = ScrollView()

        self.notifier.setPlayer(self.tabWidget.player_object())
        self.notifier.setMusicTab(self.myMusic)
        self.notifier.setFavouriteTab(self.favourites)
        self.notifier.setCollectionTab(self.musicCollections)

        self.settings.path_added.connect(self.myMusic.notify)
        self.settings.autoPlayChecked.connect(self.notifier.enableAutoPlay)
        self.settings.path_deleted.connect(lambda x: self.myMusic.deleteSearchDir(x))

        self.tabWidget.addTab(self.myMusic, "My Music", QtGui.QIcon(Paths.MUSIC))
        self.tabWidget.addTab(self.favourites, "Favourites", QtGui.QIcon(Paths.STAR_FILLED))
        self.tabWidget.addTab(self.musicCollections, "Collections", QtGui.QIcon(Paths.LIBRARY))
        self.tabWidget.addTab(self.settings, "Settings", QtGui.QIcon(Paths.SETTINGS))
        self.tabWidget.addTab(self.statistics, "Statistics", QtGui.QIcon(Paths.STATISTICS))

        self.layout().addWidget(self.tabWidget)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:  # todo: save files before closing

        # directories = self.settings.directories()
        # files = self.myMusic.getFilePaths()
        #
        # self.db_handler.insertToPaths(directories)
        # self.db_handler.insertToFiles(files)
        #
        # print("Files: ", self.db_handler.getFiles())
        # print(self.db_handler.getPaths())

        super(MainWindow, self).closeEvent(a0)
