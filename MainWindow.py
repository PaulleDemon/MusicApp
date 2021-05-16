from PyQt5 import QtWidgets
from VerticalTabs import TabWidget
from ScrollArea import ScrollView


class MainWindow(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        tabWidget = TabWidget()

        myMusic = ScrollView()
        for x in range(20):
            myMusic.addTile()
        favourites = ScrollView()
        musicCollections = ScrollView()
        settings = ScrollView()
        statistics = ScrollView()

        tabWidget.addTab(myMusic, "My Music")
        tabWidget.addTab(favourites, "Favorites")
        tabWidget.addTab(musicCollections, "Collections")
        tabWidget.addTab(settings, "Settings")
        tabWidget.addTab(statistics, "Statistics")

        self.layout().addWidget(tabWidget)

