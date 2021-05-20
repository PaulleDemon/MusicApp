from PyQt5 import QtWidgets
from VerticalTabs import TabWidget
from ScrollArea import ScrollView
from Settings import Settings
from MyMusic import MyMusic

from Controller import Notifier


class MainWindow(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        tabWidget = TabWidget()

        notify = Notifier()

        myMusic = MyMusic()

        favourites = ScrollView()
        musicCollections = ScrollView()
        settings = Settings()
        statistics = ScrollView()

        # notify.register(myMusic)
        # notify.register(settings)

        settings.path_added.connect(myMusic.notify)
        settings.path_deleted.connect(lambda x: myMusic.deleteSearchDir(x))

        tabWidget.addTab(myMusic, "My Music")
        tabWidget.addTab(favourites, "Favorites")
        tabWidget.addTab(musicCollections, "Collections")
        tabWidget.addTab(settings, "Settings")
        tabWidget.addTab(statistics, "Statistics")

        self.layout().addWidget(tabWidget)

