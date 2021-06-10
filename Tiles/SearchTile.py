import Paths
from PyQt5 import QtWidgets, QtGui, QtCore
from .Tile import Tile
from .Music_FavouritesTile import MusicTile


class SearchTile(Tile):  # Music search tile

    def __init__(self, parent: MusicTile, *args, **kwargs):
        super(SearchTile, self).__init__(*args, **kwargs)

        self.setObjectName("Tile")
        self.setLayout(QtWidgets.QVBoxLayout())
        self.parent = parent
        self.parent.addChild(self)

        self.thumb_nail = QtWidgets.QLabel()
        self.thumb_nail.setScaledContents(True)
        self.thumb_nail.setPixmap(self.parent.getThumbnail())
        self.thumb_nail.setLayout(QtWidgets.QVBoxLayout())

        self.title = QtWidgets.QLabel(self.parent.getTitle())
        self.title.setMaximumHeight(30)

        btns = QtWidgets.QButtonGroup(self)

        self.play_btn = QtWidgets.QPushButton(objectName="PlayButton")
        self.play_btn.setFixedSize(50, 50)
        self.play_btn.setIcon(QtGui.QIcon(Paths.PLAY))

        self.favourite = QtWidgets.QPushButton(objectName="Favourite")
        self.favourite.setFixedSize(50, 50)
        self.checkFavourite()

        if self.parent.isPlaying():
            self.update_play()

        btns.addButton(self.play_btn)
        btns.addButton(self.favourite)
        btns.buttonClicked.connect(self.clicked)

        self.btns = QtWidgets.QWidget()
        self.btns.setLayout(QtWidgets.QHBoxLayout())
        self.btns.hide()

        self.btns.layout().addWidget(self.favourite, alignment=QtCore.Qt.AlignBottom)
        self.btns.layout().addWidget(self.play_btn, alignment=QtCore.Qt.AlignBottom)

        self.shadow_effect = QtWidgets.QGraphicsDropShadowEffect()
        self.shadow_effect.setBlurRadius(5)
        self.shadow_effect.setOffset(3, 3)
        self.shadow_effect.setColor(QtGui.QColor(255, 255, 255))

        self.play_btn.setGraphicsEffect(self.shadow_effect)
        self.favourite.setGraphicsEffect(self.shadow_effect)
        self.btns.setGraphicsEffect(self.shadow_effect)

        self.thumb_nail.layout().addWidget(self.btns, alignment=QtCore.Qt.AlignBottom)
        self.layout().addWidget(self.thumb_nail)
        self.layout().addWidget(self.title)


    def update_play(self):
        self.play_btn.setIcon(QtGui.QIcon(Paths.PAUSE))

    def update_pause(self):
        self.play_btn.setIcon(QtGui.QIcon(Paths.PLAY))

    def pause(self):
        self.update_pause()
        self.play_btn.setToolTip("Play")
        self.parent.clicked(self.play_btn)

    def play(self):
        self.update_play()
        self.play_btn.setToolTip("Pause")
        self.parent.clicked(self.play_btn)

    def clicked(self, btn):

        if btn == self.play_btn:
            if self.parent.isPlaying():
                self.pause()

            else:
                self.play()

        elif btn == self.favourite:
            self.parent.clicked(btn)
            self.checkFavourite()

    def checkFavourite(self):
        _, favourite, _ = self.parent.properties()

        if favourite:
            self.favourite.setToolTip("Remove From Favourite")
            self.favourite.setIcon(QtGui.QIcon(Paths.STAR_FILLED))

        else:
            self.favourite.setToolTip("Add Favourite")
            self.favourite.setIcon(QtGui.QIcon(Paths.STAR_UNFILLED))

    def deleteLater(self) -> None:
        self.parent.removeChild(self)
        super(SearchTile, self).deleteLater()


class CollectionSearchTile(Tile): # Collection Search Tile

    def __init__(self, parent, *args, **kwargs):
        super(CollectionSearchTile, self).__init__(*args, **kwargs)

        self.setObjectName("Tile")
        self.setLayout(QtWidgets.QVBoxLayout())
        self.parent = parent
        self.parent.addChild(self)

        self.thumb_nail = QtWidgets.QLabel()
        self.thumb_nail.setScaledContents(True)
        self.thumb_nail.setPixmap(self.parent.getCurrentThumbnail())
        self.thumb_nail.setLayout(QtWidgets.QVBoxLayout())

        self.title = QtWidgets.QLabel(self.parent.getCollectionName())
        self.title.setMaximumHeight(30)

        btns = QtWidgets.QButtonGroup(self)

        self.play_btn = QtWidgets.QPushButton(objectName="PlayButton")
        self.play_btn.setIcon(QtGui.QIcon(Paths.PLAY))

        if self.parent.isPlaying():
            self.update_play()

        btns.addButton(self.play_btn)
        btns.buttonClicked.connect(self.clicked)

        self.btns = QtWidgets.QWidget(objectName="ButtonGroup")
        self.btns.setLayout(QtWidgets.QHBoxLayout())
        self.btns.hide()

        self.btns.layout().addWidget(self.play_btn, alignment=QtCore.Qt.AlignBottom)

        self.shadow_effect = QtWidgets.QGraphicsDropShadowEffect()
        self.shadow_effect.setBlurRadius(5)
        self.shadow_effect.setOffset(3, 3)
        self.shadow_effect.setColor(QtGui.QColor(255, 255, 255))

        self.play_btn.setGraphicsEffect(self.shadow_effect)
        self.btns.setGraphicsEffect(self.shadow_effect)

        self.thumb_nail.layout().addWidget(self.btns, alignment=QtCore.Qt.AlignBottom)
        self.layout().addWidget(self.thumb_nail)
        self.layout().addWidget(self.title)

    def update_play(self):
        self.play_btn.setIcon(QtGui.QIcon(Paths.PAUSE))

    def update_pause(self):
        self.play_btn.setIcon(QtGui.QIcon(Paths.PLAY))

    def pause(self):
        self.update_pause()
        self.play_btn.setToolTip("Play")
        self.parent.clicked(self.play_btn)

    def play(self):
        self.update_play()
        self.play_btn.setToolTip("Pause")
        self.parent.clicked(self.play_btn)

    def clicked(self, btn):

        if btn == self.play_btn:
            if self.parent.isPlaying():
                self.pause()

            else:
                self.play()